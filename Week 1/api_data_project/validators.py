
def validate_users(data: object) -> list[str]:
    """Validate API user data and return any validation errors."""
    errors: list[str] = []

    if not isinstance(data, list):
        return ["API response must be a list."]

    if not data:
        return ["API response contains no users."]

    required_fields = ["id", "name", "email"]

    for index, user in enumerate(data):
        if not isinstance(user, dict):
            errors.append(
                f"User at index {index} must be a dictionary."
            )
            continue

        for field in required_fields:
            if field not in user:
                errors.append(
                    f"User at index {index} is missing '{field}'."
                )
                continue

            value = user[field]

            if value is None or (
                isinstance(value, str) and not value.strip()
            ):
                errors.append(
                    f"User at index {index} has an empty '{field}' value."
                )

        if "id" in user and (
            isinstance(user["id"], bool)
            or not isinstance(user["id"], int)
        ):
            errors.append(
                f"User at index {index} has an invalid 'id'; "
                "expected an integer."
            )

        for field in ["name", "email"]:
            if field in user and not isinstance(user[field], str):
                errors.append(
                    f"User at index {index} has an invalid '{field}'; "
                    "expected a string."
                )

    return errors
