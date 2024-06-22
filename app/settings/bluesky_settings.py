import os
from datetime import timedelta, timezone

BLUESKY_API_DOMAIN = os.getenv("BLUESKY_DOMAIN_NAME", "bsky.social")
TZ = timezone(timedelta(hours=+9), "JST")
LIMIT_MESSAGE_LENGTH = 300