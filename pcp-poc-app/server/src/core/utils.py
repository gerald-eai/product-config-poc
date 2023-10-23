import uuid


def generate_audit_uuid() -> str:
    """Creates a hex based UUID string

    Returns:
        str: the UUID string
    """
    full_uuid = uuid.uuid4()
    hex_uuid = full_uuid.hex

    short_hex = hex_uuid[:10]
    return short_hex
