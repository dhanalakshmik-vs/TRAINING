
import unittest

from transformer import transform_users
from validators import validate_users


class TestValidateUsers(unittest.TestCase):
    """Tests for API user data validation."""

    def setUp(self) -> None:
        """Create sample data used by validation tests."""
        self.valid_users = [
            {
                "id": 1,
                "name": "Leanne Graham",
                "email": "leanne@example.com",
            }
        ]

    def test_valid_users(self) -> None:
        """Valid user data should produce no errors."""
        errors = validate_users(self.valid_users)

        self.assertEqual(errors, [])

    def test_response_must_be_a_list(self) -> None:
        """A non-list API response should be rejected."""
        errors = validate_users({"id": 1})

        self.assertTrue(errors)

    def test_empty_user_list(self) -> None:
        """An empty list should produce a validation error."""
        errors = validate_users([])

        self.assertTrue(errors)

    def test_missing_required_field(self) -> None:
        """A user missing a required field should be rejected."""
        users = [{"id": 1, "name": "Leanne Graham"}]

        errors = validate_users(users)

        self.assertTrue(
            any("email" in error for error in errors)
        )

    def test_invalid_user_id(self) -> None:
        """A string ID should be rejected when an integer is required."""
        users = [
            {
                "id": "one",
                "name": "Leanne Graham",
                "email": "leanne@example.com",
            }
        ]

        errors = validate_users(users)

        self.assertTrue(
            any("invalid 'id'" in error for error in errors)
        )

    def test_invalid_name_type(self) -> None:
        """A non-string name should be rejected."""
        users = [
            {
                "id": 1,
                "name": 123,
                "email": "leanne@example.com",
            }
        ]

        errors = validate_users(users)

        self.assertTrue(
            any("invalid 'name'" in error for error in errors)
        )


class TestTransformUsers(unittest.TestCase):
    """Tests for API user data transformation."""

    def setUp(self) -> None:
        """Create sample API data for transformation tests."""
        self.api_users = [
            {
                "id": 1,
                "name": "Leanne Graham",
                "email": "leanne@example.com",
                "address": {"city": "Gwenborough"},
                "phone": "123-456",
            }
        ]

    def test_transform_user_fields(self) -> None:
        """Transformation should extract only the required fields."""
        result = transform_users(self.api_users)

        expected = [
            {
                "id": 1,
                "name": "Leanne Graham",
                "email": "leanne@example.com",
                "city": "Gwenborough",
            }
        ]

        self.assertEqual(result, expected)

    def test_transform_multiple_users(self) -> None:
        """Transformation should preserve all user records."""
        second_user = {
            "id": 2,
            "name": "Ervin Howell",
            "email": "ervin@example.com",
            "address": {"city": "Wisokyburgh"},
        }
        users = self.api_users + [second_user]

        result = transform_users(users)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["city"], "Wisokyburgh")


if __name__ == "__main__":
    unittest.main()