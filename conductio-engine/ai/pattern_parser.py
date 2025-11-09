def validate_pattern(data: dict) -> dict:
    """Ensure AI output follows Conductio pattern schema."""
    if "pattern" not in data:
        raise ValueError("Invalid AI response: missing 'pattern'")
    for ev in data["pattern"]:
        ev.setdefault("velocity", 90)
        ev.setdefault("duration", 480)
        ev.setdefault("beat", 1.0)
        ev.setdefault("bar", 1)
    return data