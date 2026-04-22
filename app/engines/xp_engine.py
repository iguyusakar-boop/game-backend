def calculate_xp(action_type: str, value: int) -> int:
    base_map = {
        "study": 10,
        "workout": 15,
        "meditation": 8
    }

    base = base_map.get(action_type, 5)
    return base * value