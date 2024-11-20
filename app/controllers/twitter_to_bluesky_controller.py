import os
from logging import getLogger
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from app.models.bluesky_models import CreateRecordPayload
from app.models.exception_models import (
    LoginError,
    LoginErrorMessage,
    MessageBlankError,
    MessageBlankErrorMessage,
    PostFailedError,
    PostFailedErrorMessage,
)
from app.models.ifttt_models import IftttRequestBody
from app.utils.bluesky_utils import Bluesky

log_level = os.getenv("LOG_LEVEL", "INFO")
logger = getLogger("uvicorn.app")
logger.setLevel(log_level)

router = APIRouter()


@router.post(
    "/twitter_to_bluesky",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": LoginErrorMessage},
        status.HTTP_400_BAD_REQUEST: {"model": PostFailedErrorMessage},
        status.HTTP_400_BAD_REQUEST: {"model": MessageBlankErrorMessage},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
)
def twitter_to_bluesky(body: IftttRequestBody) -> Optional[CreateRecordPayload]:
    """TwitterからBlueskyへの投稿"""
    try:
        handle = body.handle
        app_password = body.app_password
        text = body.text
        link_to_tweet = body.link_to_tweet

        bluesky = Bluesky()
        login_response = bluesky.login(handle, app_password)
        if login_response is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=LoginError.message,
            )
        record = bluesky.make_record(login_response, text, link_to_tweet)
        logger.info(
            f"handle: {handle}, record: {record}, link_to_tweet: {link_to_tweet}"
        )

        post_record = bluesky.post_record(login_response, record)
        return post_record

    except LoginError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=LoginError.message,
        )

    except PostFailedError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PostFailedError.message,
        )

    except MessageBlankError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=MessageBlankError.message,
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
