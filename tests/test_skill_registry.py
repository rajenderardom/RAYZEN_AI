import unittest
from src.core.skill_registry import SkillRegistry


class DummySkill:
    """Mock skill class for testing."""

    def test_action(self, arg1, arg2="default"):
        return f"{arg1}-{arg2}"


class TestSkillRegistry(unittest.TestCase):
    """Test cases for SkillRegistry."""

    def setUp(self):
        self.registry = SkillRegistry()
        self.dummy = DummySkill()

    def test_register_and_get(self):
        self.registry.register("dummy", self.dummy)

        # Check casing and whitespace ignore
        self.assertEqual(self.registry.get("DUMMY "), self.dummy)

    def test_unregister(self):
        self.registry.register("dummy", self.dummy)
        self.registry.unregister("dummy")

        self.assertIsNone(self.registry.get("dummy"))

    def test_list_skills(self):
        self.registry.register("b_skill", self.dummy)
        self.registry.register("a_skill", self.dummy)

        # Should be returned sorted
        self.assertEqual(self.registry.list_skills(), ["a_skill", "b_skill"])

    def test_execute_success(self):
        self.registry.register("dummy", self.dummy)

        # Call execute with parameters
        result = self.registry.execute("dummy", "test_action", arg1="value", arg2="custom")
        self.assertEqual(result, "value-custom")

    def test_execute_unknown_skill(self):
        result = self.registry.execute("nonexistent", "action")
        self.assertFalse(result)

    def test_execute_unknown_action(self):
        self.registry.register("dummy", self.dummy)
        result = self.registry.execute("dummy", "invalid_action")
        self.assertFalse(result)

    def test_execute_exception_handling(self):
        class BadSkill:
            def fail(self):
                raise ValueError("Action failed")

        self.registry.register("bad", BadSkill())
        result = self.registry.execute("bad", "fail")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
