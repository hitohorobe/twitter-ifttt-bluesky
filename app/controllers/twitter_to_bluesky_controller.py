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
from app.services.bluesky_service import BlueskyService
from app.usecases.bluesky_usecase import BlueskyUsecase

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
def post_to_bluesky(body: IftttRequestBody) -> Optional[CreateRecordPayload]:
    """TwitterからBlueskyへの投稿"""
    try:
        bluesky_usecase = BlueskyUsecase()
        response = bluesky_usecase.twitter_to_bluesky(body)
        return response

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
