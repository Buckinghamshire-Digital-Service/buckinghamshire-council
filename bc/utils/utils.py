def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False
