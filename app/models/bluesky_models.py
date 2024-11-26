from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class LoginResponse(BaseModel):
    """ログイン時のdidとアクセストークン"""

    access_jwt: str
    did: str


class Index(BaseModel):
    """リッチテキストでリンクを表現する際、リンクを貼る位置を開始バイトと終了バイトで表現する"""

    byte_start: int = Field(serialization_alias="byteStart")
    byte_end: int = Field(serialization_alias="byteEnd")


class Feature(BaseModel):
    """マークアップの内容を表現する"""

    types: str = Field(
        serialization_alias="$type", default="app.bsky.richtext.facet#link"
    )
    uri: Optional[HttpUrl] = None
    tag: Optional[str] = None


class Facet(BaseModel):
    """リッチテキストの装飾位置と種別を指定する"""

    index: Index
    features: list[Feature]


class Ref(BaseModel):
    """画像をアップロードした際に返される参照情報
    この参照情報を使って、アップロード済み画像をポストから参照することで画像を投稿する
    """

    link: str = Field(serialization_alias="$link")


class Image(BaseModel):
    """画像の情報"""

    types: str = Field(serialization_alias="$type", default="blob")
    ref: Ref
    mime_type: str = Field(serialization_alias="mimeType")
    size: int


class Thumb(BaseModel):
    """サムネイルを表現するモデル"""

    image: Image
    alt: Optional[str] = None


class Blob(BaseModel):
    """画像ファイルのバイナリ情報。画像投稿やリンクカード作成時に用いる"""

    types: str = Field(serialization_alias="$type", default="blob")
    ref: Ref
    mime_type: str = Field(serialization_alias="mimeType")
    size: int


class External(BaseModel):
    """リンクカードの情報を表現する。画像があれば画像付きカード、ない場合はテキストのみのリンクカードになる"""

    uri: HttpUrl
    title: str
    description: str
    thumb: Optional[Blob]


class Embed(BaseModel):
    """リンクカードまたは画像を埋め込む際の情報を表現する
    画像(images)とリンクカード(external)の片方しか投稿できない
    """

    types: str = Field(serialization_alias="$type", default="app.bsky.embed.external")
    external: Optional[External]
    images: Optional[list[Image]] = None

    @field_validator("external", "images")
    @classmethod
    def select_one(cls, values: Any):
        if "external" in values and "images" in values:
            raise ValueError("You can only embed either external or images")
        return values


class LabelEnum(StrEnum):
    """センシティブなコンテンツに付与するラベルの値
    - sexual: 性的な表現
    - nudity: ヌード
    - porn: ポルノ
    """

    sexual = "sexual"
    nudity = "nudity"
    porn = "porn"
    sexually_suggestive = "sexual-figurative"


class LabelValue(BaseModel):
    """適用されるラベルの値"""

    val: LabelEnum


class Labels(BaseModel):
    """センシティブなコンテンツに付与するラベル"""

    types: str = Field(
        serialization_alias="$type", default="com.atproto.label.defs#selfLabels"
    )
    values: list[LabelValue]


class Record(BaseModel):
    """新規ポストの情報"""

    text: str
    created_at: str = Field(serialization_alias="createdAt")
    facets: list[Facet]
    types: str = Field(serialization_alias="$type", default="app.bsky.feed.post")
    embed: Optional[Embed]
    labels: Optional[Labels] = None
    via: Optional[str] = None


class CreateRecordPayload(BaseModel):
    """新規ポストする際のリクエストボディ"""

    repo: str
    collection: str = "app.bsky.feed.post"
    record: Record

    class Config:
        use_enum_values = True


class ImageUploadResponse(BaseModel):
    """画像アップロード時のレスポンス"""

    blob: Blob
