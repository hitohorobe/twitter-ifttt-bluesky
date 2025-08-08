import os
from logging import getLogger
from typing import Optional

from fastapi import HTTPException, status

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
from app.services.bluesky_service import BlueskyService

log_level = os.getenv("LOG_LEVEL", "INFO")
logger = getLogger("uvicorn.app")
logger.setLevel(log_level)


class BlueskyUsecase:
    """
    Use case for handling Bluesky operations.
    """

    @classmethod
    def twitter_to_bluesky(cls, body: IftttRequestBody) -> Optional[CreateRecordPayload]:
        """Handles the conversion of Twitter posts to Bluesky."""
        try:
            handle = body.handle
            app_password = body.app_password
            text = body.text
            link_to_tweet = body.link_to_tweet

            bluesky = BlueskyService()
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
        except MessageBlankError as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=MessageBlankError.message,
            )
        except PostFailedError as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=PostFailedError.message,
            )

        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )