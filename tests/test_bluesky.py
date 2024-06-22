import os

from app.models.bluesky_models import LabelEnum
from app.settings.bluesky_settings import LIMIT_MESSAGE_LENGTH
from app.utils.bluesky_utils import Bluesky

TEST_HANDLE = os.getenv("TEST_HANDLE")
TEST_APP_PASSWORD = os.getenv("TEST_APP_PASSWORD")


def test_login():
    response = Bluesky.login(
        handle=TEST_HANDLE, app_password=TEST_APP_PASSWORD
    )
    assert response
    assert response.access_jwt
    assert response.did


def test_upload_image():
    login_response = Bluesky.login(
        handle=TEST_HANDLE, app_password=TEST_APP_PASSWORD
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


def test_make_record():
    login_response = Bluesky.login(
        handle=TEST_HANDLE, app_password=TEST_APP_PASSWORD
    )
    assert login_response
    text = f"test https://hito-horobe.net/ です"
    link_to_tweet = "https://x.com/hito_horobe2/status/1801101262727037180"
    record = Bluesky.make_record(login_response, text, link_to_tweet)
    assert record


def test_post_record():
    login_response = Bluesky.login(
        handle=TEST_HANDLE, app_password=TEST_APP_PASSWORD
    )
    assert login_response
    text = f"test https://hito-horobe.net/ です" * 20
    link_to_tweet = "https://x.com/hito_horobe2/status/1801101262727037180"
    record = Bluesky.make_record(login_response, text, link_to_tweet)
    assert len(record.record.text) >= LIMIT_MESSAGE_LENGTH
    post_record = Bluesky.post_record(login_response, record)
    assert post_record