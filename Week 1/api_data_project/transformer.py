
def transform_users(data: list[dict]) -> list[dict]:
    """Extract the required fields from API user data."""
    transformed_users = []

    for user in data:
        transformed_user = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "city": user["address"]["city"],
        }

        transformed_users.append(transformed_user)

    return transformed_users
