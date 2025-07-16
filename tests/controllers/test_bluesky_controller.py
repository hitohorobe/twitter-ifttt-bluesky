
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.models.bluesky_models import (
    CreateRecordPayload,
    LoginResponse,
    Record,
)
from app.models.ifttt_models import IftttRequestBody
from app.usecases.bluesky_usecase import BlueskyUsecase
from main import app

client = TestClient(app)


def test_post_to_bluesky(mocker: MockerFixture):
    mock_login_response = LoginResponse(
        access_jwt="test_access_jwt",
        did="test_did"
    )
    mock_login = mocker.patch(
        "app.services.bluesky_service.BlueskyService.login",
        return_value=mock_login_response
    )
    mock_record = Record(
          text="test_record_text",
          facets=[],
          created_at="2023-10-01T00:00:00Z",
          types="app.bsky.feed.post",
          embed=None,
          labels=None,
          via=None
    )
    mock_create_record_payload = CreateRecordPayload(
        repo=mock_login_response.did,
        collection="app.bsky.feed.post",
        record=mock_record
    )
    mock_make_record = mocker.patch(
          "app.services.bluesky_service.BlueskyService.make_record",
          return_value=mock_create_record_payload
    )
    mock_post_record = mocker.patch(
          "app.services.bluesky_service.BlueskyService.post_record",
          return_value=mock_create_record_payload
    )
    test_payload = IftttRequestBody(
        handle="test_handle",
        app_password="test_app_password",
        text="test_text",
        link_to_tweet="http://example.com/test_tweet"
    )
    response = client.post("/twitter_to_bluesky", json=test_payload.model_dump())

    assert response.status_code == 200
    assert response.json() == mock_create_record_payload.model_dump(by_alias=True)

