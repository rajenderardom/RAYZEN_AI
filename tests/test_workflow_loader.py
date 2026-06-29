import os
import shutil
import tempfile
import unittest
from src.workflows.workflow_loader import WorkflowLoader


class TestWorkflowLoader(unittest.TestCase):
    """Test cases for WorkflowLoader."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.loader = WorkflowLoader()
        self.valid_workflow = {
            "name": "Search Google",
            "version": "1.0.0",
            "steps": [
                {"action": "open_url", "url": "https://google.com"},
                {"action": "type", "selector": "[name='q']", "text": "playwright"},
                {"action": "press", "key": "Enter"},
            ],
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_validate_valid_workflow(self):
        self.assertTrue(self.loader.validate(self.valid_workflow))

    def test_validate_missing_root_key(self):
        invalid = self.valid_workflow.copy()
        del invalid["version"]
        self.assertFalse(self.loader.validate(invalid))

    def test_validate_invalid_steps_type(self):
        invalid = self.valid_workflow.copy()
        invalid["steps"] = "not-a-list"
        self.assertFalse(self.loader.validate(invalid))

    def test_validate_step_missing_action(self):
        invalid = self.valid_workflow.copy()
        invalid["steps"] = [{"url": "https://example.com"}]  # missing 'action'
        self.assertFalse(self.loader.validate(invalid))

    def test_save_and_load_success(self):
        file_path = os.path.join(self.test_dir, "search.json")

        save_ok = self.loader.save(file_path, self.valid_workflow)
        self.assertTrue(save_ok)
        self.assertTrue(os.path.exists(file_path))

        loaded = self.loader.load(file_path)
        self.assertEqual(loaded["name"], "Search Google")
        self.assertEqual(loaded["version"], "1.0.0")
        self.assertEqual(len(loaded["steps"]), 3)

    def test_load_nonexistent_file(self):
        loaded = self.loader.load(os.path.join(self.test_dir, "nonexistent.json"))
        self.assertEqual(loaded, {})

    def test_load_malformed_json(self):
        file_path = os.path.join(self.test_dir, "bad.json")
        with open(file_path, "w") as f:
            f.write("{invalid-json:")

        loaded = self.loader.load(file_path)
        self.assertEqual(loaded, {})


if __name__ == "__main__":
    unittest.main()
