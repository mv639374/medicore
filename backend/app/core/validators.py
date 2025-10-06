# What & Why: This file holds functions for validating user input. This helps prevent bad data from entering our system and protects against common vulnerabilities like Cross-Site Scripting (XSS) by sanitizing input.

import re


def validate_email(email: str) -> bool:
    """Validate email format using a simple regex."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Check password strength requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain a digit."
    return True, "Password is strong."
