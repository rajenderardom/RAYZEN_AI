"""
RAYZEN AI
Browser Workflow Runner

Version : 0.2.0
"""

import time
from typing import List, Dict, Any
from src.browser.playwright_engine import PlaywrightEngine
from src.browser.element_engine import ElementEngine
from src.browser.page_controller import PageController
from src.core.logger import RayzenLogger


class WorkflowRunner:
    """Executes generic browser automation workflows driven by JSON step definitions."""

    def __init__(
        self,
        playwright_engine: PlaywrightEngine,
        element_engine: ElementEngine,
        page_controller: PageController,
    ):
        """Initialize WorkflowRunner.

        Args:
            playwright_engine (PlaywrightEngine): The active Playwright browser instance.
            element_engine (ElementEngine): Element interaction engine.
            page_controller (PageController): Tab and page controller.
        """
        self.playwright = playwright_engine
        self.element = element_engine
        self.page_control = page_controller
        self.logger = RayzenLogger()


    def validate(self, step: Dict[str, Any]) -> bool:
        """Validate if a step definition contains a valid action and required parameters.

        Args:
            step (Dict[str, Any]): Step definition details.

        Returns:
            bool: True if step is valid, False otherwise.
        """
        if not isinstance(step, dict):
            self.logger.error("Step validation failed: Step definition must be a dictionary.")
            return False

        action = step.get("action")
        if not action:
            self.logger.error("Step validation failed: 'action' key is missing.")
            return False

        required_params = {
            "open_url": ["url"],
            "click": ["selector"],
            "type": ["selector", "text"],
            "press": ["key"],
            "wait": ["duration"],
            "wait_for_selector": ["selector"],
            "screenshot": ["path"],
            "upload": ["selector", "path"],
            "download": ["selector", "path"],
            "hover": ["selector"],
            "scroll": ["selector"],
            "verify": ["selector"],
        }

        no_param_actions = {"refresh", "back", "forward", "new_tab", "close_tab"}

        if action not in required_params and action not in no_param_actions:
            self.logger.error(f"Step validation failed: Unknown action name '{action}'.")
            return False

        for param in required_params.get(action, []):
            if param not in step:
                self.logger.error(
                    f"Step validation failed: Action '{action}' requires parameter '{param}'."
                )
                return False

        return True

    def run(self, workflow: List[Dict[str, Any]]) -> bool:
        """Execute a list of steps sequentially.

        Args:
            workflow (List[Dict[str, Any]]): The list of workflow step definitions.

        Returns:
            bool: True if the entire workflow finishes successfully, False if any step fails.
        """
        if not isinstance(workflow, list):
            self.logger.error(
                "Workflow execution failed: Workflow must be a list of step definitions."
            )
            return False

        self.logger.info(f"Starting browser workflow execution. Total steps: {len(workflow)}")

        for idx, step in enumerate(workflow, 1):
            self.logger.info(f"Validating step {idx}/{len(workflow)}: {step.get('action')}")
            if not self.validate(step):
                self.logger.error(f"Workflow halted: Invalid step definition at index {idx}.")
                return False

            self.logger.info(f"Executing step {idx}/{len(workflow)}: {step.get('action')}")
            success = self.execute_step(step)
            if not success:
                self.logger.error(
                    f"Workflow halted: Step {idx} ({step.get('action')}) failed to execute."
                )
                return False

        self.logger.info("Browser workflow executed successfully.")
        return True

    def execute_step(self, step: Dict[str, Any]) -> bool:
        """Execute a single workflow step.

        Args:
            step (Dict[str, Any]): The validated step dictionary.

        Returns:
            bool: True on success, False on failure.
        """
        action = step["action"]

        try:
            # 1. Page control and Navigation actions
            if action == "open_url":
                return self.playwright.open_url(step["url"])

            elif action == "new_tab":
                return self.page_control.new_tab()

            elif action == "close_tab":
                return self.page_control.close_current_tab()

            elif action == "refresh":
                return self.page_control.refresh_page()

            elif action == "back":
                return self.page_control.go_back()

            elif action == "forward":
                return self.page_control.go_forward()

            # 2. Element interactions
            elif action == "click":
                return self.element.click(step["selector"])

            elif action == "type":
                return self.element.type_text(step["selector"], step["text"])

            elif action == "press":
                return self.element.press_key(step["key"])

            elif action == "hover":
                return self.element.hover(step["selector"])

            elif action == "scroll":
                return self.element.scroll_to(step["selector"])

            elif action == "wait_for_selector":
                timeout = step.get("timeout", 10000)
                return self.element.wait_for(step["selector"], timeout=timeout)

            # 3. Delays
            elif action == "wait":
                duration_ms = step["duration"]
                self.logger.info(f"Sleeping for {duration_ms}ms")
                time.sleep(duration_ms / 1000.0)
                return True

            # 4. Advanced Playwright Specifics (screenshot, upload, download, verify)
            elif action == "screenshot":
                path = step["path"]
                if not self.playwright.is_browser_running() or not self.playwright._page:
                    raise RuntimeError("Browser not running or page not initialized.")
                self.logger.info(f"Capturing page screenshot to: '{path}'")
                self.playwright._page.screenshot(path=path)
                return True

            elif action == "upload":
                path = step["path"]
                selector = step["selector"]
                if not self.playwright.is_browser_running() or not self.playwright._page:
                    raise RuntimeError("Browser not running or page not initialized.")
                self.logger.info(f"Uploading file '{path}' via input element '{selector}'")
                self.playwright._page.locator(selector).set_input_files(path)
                return True

            elif action == "download":
                path = step["path"]
                selector = step["selector"]
                if not self.playwright.is_browser_running() or not self.playwright._page:
                    raise RuntimeError("Browser not running or page not initialized.")
                self.logger.info(f"Waiting for download triggered by click on '{selector}'")
                with self.playwright._page.expect_download() as download_info:
                    click_ok = self.element.click(selector)
                    if not click_ok:
                        raise RuntimeError(
                            f"Failed to click download trigger selector '{selector}'"
                        )
                download = download_info.value
                self.logger.info(f"Saving downloaded file to: '{path}'")
                download.save_as(path)
                return True

            elif action == "verify":
                selector = step["selector"]
                expected_text = step.get("text")
                if expected_text is not None:
                    self.logger.info(
                        f"Verifying text of element '{selector}' contains expected '{expected_text}'"
                    )
                    actual_text = self.element.get_text(selector)
                    if expected_text not in actual_text:
                        self.logger.error(
                            f"Verification failed: Expected '{expected_text}' to be in actual '{actual_text}'"
                        )
                        return False
                    return True
                else:
                    self.logger.info(f"Verifying existence of element: '{selector}'")
                    if not self.element.exists(selector):
                        self.logger.error(f"Verification failed: Element '{selector}' does not exist.")
                        return False
                    return True

            else:
                self.logger.error(f"Unmapped action execution logic: '{action}'")
                return False

        except Exception as e:
            self.logger.error(f"Exception occurred executing step '{action}': {e}")
            return False
