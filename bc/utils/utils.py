from typing import List


def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def get_pk_list(queryset, field="pk") -> List[int]:
    """Returns the only the PKs from the queryset, as a list."""
    return list(queryset.order_by(field).values_list(field, flat=True))
