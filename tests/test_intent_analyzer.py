import unittest
from unittest.mock import MagicMock
from src.core.interpreter import NaturalLanguageInterpreter
from src.brain.intent_analyzer import IntentAnalyzer


class TestIntentAnalyzer(unittest.TestCase):
    """Test cases for IntentAnalyzer."""

    def setUp(self):
        self.mock_interpreter = MagicMock(spec=NaturalLanguageInterpreter)
        self.analyzer = IntentAnalyzer(self.mock_interpreter)

    def test_analyze_browser_open(self):
        self.mock_interpreter.interpret.return_value = "open google"
        result = self.analyzer.analyze("open google")
        expected = {"intent": "browser.open", "target": "google", "confidence": 1.0}
        self.assertEqual(result, expected)

    def test_analyze_desktop_open_kholo(self):
        self.mock_interpreter.interpret.return_value = "open calculator"
        result = self.analyzer.analyze("calculator kholo")
        expected = {"intent": "desktop.open", "target": "calculator", "confidence": 1.0}
        self.assertEqual(result, expected)

    def test_analyze_excel_file(self):
        result = self.analyzer.analyze("analyze report.xlsx")
        expected = {"intent": "excel.analyze", "file": "report.xlsx", "confidence": 0.95}
        self.assertEqual(result, expected)

    def test_analyze_excel_file_case_preservation(self):
        result = self.analyzer.analyze("ANALYZE ImportantData.csv")
        expected = {"intent": "excel.analyze", "file": "ImportantData.csv", "confidence": 0.95}
        self.assertEqual(result, expected)

    def test_analyze_download_workflow(self):
        result = self.analyzer.analyze("download latest electricity bill")
        expected = {
            "intent": "browser.workflow",
            "task": "download electricity bill",
            "confidence": 0.80,
        }
        self.assertEqual(result, expected)

    def test_analyze_download_workflow_without_latest(self):
        result = self.analyzer.analyze("download invoice.pdf")
        expected = {"intent": "browser.workflow", "task": "download invoice.pdf", "confidence": 0.80}
        self.assertEqual(result, expected)

    def test_analyze_unknown(self):
        self.mock_interpreter.interpret.side_effect = lambda x: x
        result = self.analyzer.analyze("unsupported action command")
        expected = {"intent": "unknown", "confidence": 0.0}
        self.assertEqual(result, expected)

    def test_analyze_invalid_type(self):
        result = self.analyzer.analyze(None)  # type: ignore
        expected = {"intent": "unknown", "confidence": 0.0}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
