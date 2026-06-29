import unittest
from unittest.mock import MagicMock
from src.core.skill_registry import SkillRegistry
from src.agents.office.office_agent import OfficeAgent


class TestOfficeAgentIntegration(unittest.TestCase):
    """Integration tests checking OfficeAgent integration with SkillRegistry."""

    def test_compare_excel_integration_routing(self):
        mock_registry = MagicMock(spec=SkillRegistry)
        mock_comparator = MagicMock()
        mock_registry.get.return_value = mock_comparator
        mock_registry.execute.return_value = True

        agent = OfficeAgent(mock_registry)

        # Run
        success = agent.execute("compare excel old.xlsx new.xlsx Site_ID")
        self.assertTrue(success)

        # Assert SkillRegistry matches
        mock_registry.get.assert_called_with("excel_comparator")
        mock_registry.execute.assert_called_with(
            "excel_comparator",
            "compare",
            file_path_old="old.xlsx",
            file_path_new="new.xlsx",
            key_column="Site_ID",
            sheet_name="Sheet1",
            export_path="data/comparison_report.xlsx",
        )


if __name__ == "__main__":
    unittest.main()
