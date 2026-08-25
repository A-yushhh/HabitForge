from datetime import datetime
from zoneinfo import ZoneInfo


def to_user_timezone(
    dt: datetime,
    timezone: str,
) -> datetime:
    return dt.astimezone(ZoneInfo(timezone))