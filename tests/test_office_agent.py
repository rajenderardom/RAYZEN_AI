import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock
from src.core.skill_registry import SkillRegistry
from src.agents.office.office_models import TaskRecord
from src.agents.office.office_context import OfficeContext
from src.agents.office.office_history import OfficeHistory
from src.agents.office.office_task_router import OfficeTaskRouter
from src.agents.office.office_agent import OfficeAgent


class TestOfficeAgent(unittest.TestCase):
    """Unit test cases for the Office Agent framework."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.mock_registry = MagicMock(spec=SkillRegistry)
        self.agent = OfficeAgent(self.mock_registry)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_context_thread_safety(self):
        context = OfficeContext()
        context.set("key1", "value1")
        self.assertEqual(context.get("key1"), "value1")
        self.assertEqual(context.get_all(), {"key1": "value1"})

    def test_history_logging(self):
        history = OfficeHistory()
        record = TaskRecord(task_id="t1", description="Test task")
        history.add_record(record)

        self.assertEqual(len(history.get_all_records()), 1)
        self.assertEqual(history.get_all_records()[0].task_id, "t1")

    def test_router_parsing(self):
        router = OfficeTaskRouter()

        method, args = router.route("compare spreadsheets old.xlsx new.xlsx site_id")
        self.assertEqual(method, "compare_excel")
        self.assertEqual(args["old_file"], "old.xlsx")
        self.assertEqual(args["new_file"], "new.xlsx")

        method, args = router.route("draft email to john@example.com")
        self.assertEqual(method, "draft_email")
        self.assertEqual(args["recipient"], "john@example.com")

        method, args = router.route("perform unknown complex math")
        self.assertIsNone(method)

    def test_draft_email_action(self):
        export_path = os.path.join(self.test_dir, "drafts", "email.txt")
        result = self.agent.draft_email(
            recipient="client@test.com",
            subject="Test subject",
            body="Email body content",
            export_path=export_path,
        )
        self.assertTrue(result)
        self.assertTrue(os.path.exists(export_path))
        with open(export_path, "r") as f:
            content = f.read()
        self.assertIn("client@test.com", content)
        self.assertIn("Test subject", content)

    def test_archive_reports_action(self):
        src_dir = os.path.join(self.test_dir, "src_data")
        os.makedirs(src_dir, exist_ok=True)
        with open(os.path.join(src_dir, "report1.xlsx"), "w") as f:
            f.write("excel contents")

        zip_path = os.path.join(self.test_dir, "archives", "backup.zip")
        result = self.agent.archive_reports(src_dir, zip_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(zip_path))


if __name__ == "__main__":
    unittest.main()
