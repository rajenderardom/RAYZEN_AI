import unittest
from unittest.mock import MagicMock
from src.core.skill_registry import SkillRegistry
from src.brain.skill_selector import SkillSelector


class TestSkillSelector(unittest.TestCase):
    """Test cases for SkillSelector."""

    def setUp(self):
        self.mock_registry = MagicMock(spec=SkillRegistry)
        self.mock_registry.list_skills.return_value = ["browser", "desktop", "excel_comparator"]
        self.selector = SkillSelector(self.mock_registry)

    def test_select_skill_direct_match(self):
        result = self.selector.select_skill("browser.open", 0.95)
        self.assertEqual(result["skill"], "browser")
        self.assertEqual(result["confidence"], 0.95)

    def test_select_skill_mapped_match(self):
        self.selector.register_mapping("excel", "excel_comparator")

        result = self.selector.select_skill("excel.analyze", 1.0)
        self.assertEqual(result["skill"], "excel_comparator")
        self.assertEqual(result["confidence"], 1.0)

    def test_select_skill_substring_fallback(self):
        result = self.selector.select_skill("excel_comparator.run", 1.0)
        self.assertEqual(result["skill"], "excel_comparator")
        self.assertEqual(result["confidence"], 1.0)

        result = self.selector.select_skill("analyze_excel", 0.8)
        self.assertEqual(result["skill"], "excel_comparator")
        self.assertEqual(result["confidence"], 0.72)  # 0.8 * 0.9 = 0.72

    def test_select_skill_unknown(self):
        result = self.selector.select_skill("unsupported_intent.action")
        self.assertEqual(result["skill"], "unknown")
        self.assertEqual(result["confidence"], 0.0)

    def test_select_skill_invalid_type(self):
        result = self.selector.select_skill(None)  # type: ignore
        self.assertEqual(result["skill"], "unknown")
        self.assertEqual(result["confidence"], 0.0)


if __name__ == "__main__":
    unittest.main()
