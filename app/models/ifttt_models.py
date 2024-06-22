import os

from pydantic import BaseModel, Field

TEST_HANDLE = os.getenv("TEST_HANDLE", "@hitohorobe.bsky.social")
TEST_APP_PASSWORD = os.getenv("TEST_APP_PASSWORD", "password")

class IftttRequestBody(BaseModel):
    """IFTTTのリクエストボディ"""
    handle: str = Field(description="Blueskyのハンドル", examples=[TEST_HANDLE])
    app_password: str = Field(description="Blueskyのアプリパスワード", examples=[TEST_APP_PASSWORD])
    text: str = Field(description="投稿内容", examples=["test https://hito-horobe.net/ です"])
    link_to_tweet: str = Field(description="ツイートへのリンクURL")

