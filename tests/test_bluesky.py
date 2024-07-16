import os

from pytest_mock import MockerFixture

from app.models.bluesky_models import (
    Blob,
    ImageUploadResponse,
    LabelEnum,
    LoginResponse,
    Ref,
)
from app.settings.bluesky_settings import LIMIT_MESSAGE_LENGTH
from app.utils.bluesky_utils import Bluesky

TEST_HANDLE = os.getenv("TEST_HANDLE")
TEST_APP_PASSWORD = os.getenv("TEST_APP_PASSWORD")


def test_login(mocker: MockerFixture):
    mock_login = mocker.patch(
        "app.utils.bluesky_utils.Bluesky.login",
        return_value = LoginResponse(
            access_jwt="test_access_jwt",
            did="test_did"
        )
    )
    response = Bluesky.login(
        handle=TEST_HANDLE, app_password=TEST_APP_PASSWORD #type: ignore
    )
    assert response
    assert response.access_jwt
    assert response.did


def test_upload_image(mocker: MockerFixture):
    mock_login = mocker.patch(
        "app.utils.bluesky_utils.Bluesky.login",
        return_value = LoginResponse(
            access_jwt="test_access_jwt",
            did="test_did"
        )
    )

    mock_upload_images = mocker.patch(
        "app.utils.bluesky_utils.Bluesky.upload_image",
        return_value = ImageUploadResponse(
            blob=Blob(
                types="blob",
                ref=Ref(link="test_link"),
                mime_type="image/jpeg",
                size=1000
            )
        )
    )

    login_response = Bluesky.login(
        handle=TEST_HANDLE, app_password=TEST_APP_PASSWORD #type: ignore
    )
    assert login_response
    image_url = "https://pbs.twimg.com/ad_img/1422896111061061637/_k-yEm5a?format=jpg&name=small"
    response = Bluesky.upload_image(login_response, image_url)
    assert response


def test_sensitive_url_check_true():
    url = "https://www.dlsite.com/home/work/=/product_id/RJ01128034.html"
    response = Bluesky.sensitive_url_check(url)
    assert response == LabelEnum.porn


def test_sensitive_url_check_false():
    url = "https://www.google.com/"
    response = Bluesky.sensitive_url_check(url)
    assert response == None


def test_make_record(mocker: MockerFixture):
    mock_login = mocker.patch(
        "app.utils.bluesky_utils.Bluesky.login",
        return_value = LoginResponse(
            access_jwt="test_access_jwt",
            did="test_did"
        )
    )

    mock_upload_images = mocker.patch(
        "app.utils.bluesky_utils.Bluesky.upload_image",
        return_value = ImageUploadResponse(
            blob=Blob(
                types="blob",
                ref=Ref(link="test_link"),
                mime_type="image/jpeg",
                size=1000
            )
        )
    )

    login_response = Bluesky.login(
        handle=TEST_HANDLE, app_password=TEST_APP_PASSWORD #type: ignore
    )
    assert login_response
    text = "test https://hito-horobe.net/ です"
    link_to_tweet = "https://x.com/hito_horobe2/status/1801101262727037180"
    record = Bluesky.make_record(login_response, text, link_to_tweet)
    assert record
