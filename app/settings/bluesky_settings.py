import os
from datetime import timedelta, timezone

BLUESKY_API_DOMAIN = os.getenv("BLUESKY_DOMAIN_NAME", "bsky.social")
BLUESKY_REQUEST_TIMEOUT = int(os.getenv("BLUESKY_REQUEST_TIMEOUT", 30))
TZ = timezone(timedelta(hours=+9), "JST")
LIMIT_MESSAGE_LENGTH = 300
DEFAULT_CLIENT_NAME = "twitter-ifttt-bluesky by @hito-horobe.net"
