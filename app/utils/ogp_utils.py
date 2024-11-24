import json
import os
from logging import getLogger
from typing import Optional

import requests
from bs4 import BeautifulSoup

from app.models.ogp_models import OGP
from app.settings.bluesky_settings import BLUESKY_REQUEST_TIMEOUT

log_level = os.getenv("LOG_LEVEL", "INFO")
logger = getLogger("uvicorn.app")
logger.setLevel(log_level)


def _get_ogp_from_requests(url: str, user_agent: str) -> Optional[OGP]:
    """Retrieve OGP using requests"""
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=BLUESKY_REQUEST_TIMEOUT)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        og_title = soup.find("meta", attrs={"property": "og:title"})
        og_description = soup.find("meta", attrs={"name": "description"})
        og_image = soup.find("meta", attrs={"property": "og:image"})
        og_url = soup.find("meta", attrs={"property": "og:url"})
        og_site_name = soup.find("meta", attrs={"property": "og:site_name"})
        og_type = soup.find("meta", attrs={"property": "og:type"})

        if og_title or og_description or og_image or og_url or og_site_name or og_type:
            ogp = OGP(
                title=og_title.get("content") if og_title else None,  # type: ignore
                description=og_description.get("content") if og_description else None,  # type: ignore
                image=og_image.get("content") if og_image else None,  # type: ignore
                url=og_url.get("content") if og_url else None,  # type: ignore
                site_name=og_site_name.get("content") if og_site_name else None,  # type: ignore
                type=og_type.get("content") if og_type else None,  # type: ignore
            )
            return ogp
        else:
            return None
    except Exception as e:
        logger.error(e)
        return None


def _get_ogp_from_bluesky(url: str, user_agent: str) -> Optional[OGP]:
    """Retrieve OGP using cardyb.bsky.app"""
    headers = {"User-Agent": user_agent}
    request_url = f"https://cardyb.bsky.app/v1/extract?url={url}"
    try:
        response = requests.get(
            request_url, headers=headers, timeout=BLUESKY_REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            return None

        response_obj = json.loads(response.text)
        if response_obj["error"]:
            return None

        return OGP(
            title=response_obj["title"],
            description=response_obj["description"],
            image=response_obj["image"] if response_obj["image"] else None,
            url=response_obj["url"] if response_obj["url"] else None,
        )
    except Exception as e:
        logger.error(e)
        return None


def _get_ogp_from_amazon(url: str, user_agent: str) -> Optional[OGP]:
    """Retrieve OGP from Amazon and if it's not available return mock ogp data"""
    ogp = _get_ogp_from_amazon(url, user_agent)

    if not ogp.title or not ogp.description:
        try:
            res = requests.get(url, headers={"User-Agent": user_agent})
            if res.status_code != 200:
                return None
            soup = BeautifulSoup(res.text, "html.parser")
            title = soup.find("head").find("title").text

            return OGP(
                title=title,
                description=title,
                url=url,
            )
        except Exception as e:
            logger.error(e)
            return None

    if ogp:
        return ogp


def get_ogp(url: str) -> Optional[OGP]:
    """Get OGP data from the specified URL."""

    # if x.com or twitter.com -> use requests
    if url.find("x.com") != -1 or url.find("twitter.com") != -1:
        user_agent = "facebookexternalhit/1.1"
        return _get_ogp_from_requests(url, user_agent)
    if url.find("amazon.co.jp") != -1:
        user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
        return _get_ogp_from_bluesky(url, user_agent)
    if url.find("amzn.to") != -1:
        user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
        return _get_ogp_from_bluesky(url, user_agent)
    # elif url.find("amazon.co.jp") != -1:
    #    user_agent = "facebookexternalhit"
    #    return _get_ogp_from_requests(url, user_agent)
    else:
        user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
        return _get_ogp_from_bluesky(url, user_agent)
