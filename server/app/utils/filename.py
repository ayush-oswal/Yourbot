from datetime import datetime, UTC

def generate_unique_filename(prefix: str, extension: str) -> str:
    """Generate a unique filename using the current timestamp."""
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}/{timestamp}.{extension}"