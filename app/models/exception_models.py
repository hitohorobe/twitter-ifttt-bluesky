from pydantic import BaseModel, Field

# 例外クラスを作成する

class LoginError(Exception):
    """ログインエラー"""
    message = "ログインに失敗しました。ハンドルまたはパスワードを確認してください"

    def __str__(self) -> str:
        return LoginError.message      


class MessageBlankError(Exception):
    """文字数が0文字の場合のエラー"""
    message = "0文字の投稿はできません"

    def __str__(self) -> str:
        return MessageBlankError.message


class MessageLengthOverError(Exception):
    """文字数が300文字を超える場合のエラー"""
    message = "300文字を超える投稿はできません"

    def __str__(self) -> str:
        return MessageLengthOverError.message


class ImageUploadError(Exception):
    """画像アップロードエラー"""
    message = "画像のアップロードに失敗しました"

    def __str__(self) -> str:
        return ImageUploadError.message


class PostFailedError(Exception):
    """投稿失敗エラー"""
    message = "投稿に失敗しました"

    def __str__(self) -> str:
        return PostFailedError.message


class BlueskyDomainError(Exception):
    """PDSのドメインエラー"""
    message = "PDSのドメイン名(例: bsky.social)が不正です"

    def __str__(self) -> str:
        return BlueskyDomainError.message


class LoginErrorMessage(BaseModel):
    """ログインエラーメッセージ"""
    detail: str = Field(examples=[LoginError.message])


class MessageBlankErrorMessage(BaseModel):
    """文字数が0文字の場合のエラーメッセージ"""
    detail: str = Field(examples=[MessageBlankError.message])


class MessageLengthOverErrorMessage(BaseModel):
    """文字数が300文字を超える場合のエラーメッセージ"""
    detail: str = Field(examples=[MessageLengthOverError.message])


class ImageUploadErrorMessage(BaseModel):
    """画像アップロードエラーメッセージ"""
    detail: str = Field(examples=[ImageUploadError.message])


class PostFailedErrorMessage(BaseModel):
    """投稿失敗エラーメッセージ"""
    detail: str = Field(examples=[PostFailedError.message])


class BlueskyDomainErrorMessage(BaseModel):
    """Blueskyのドメインエラーメッセージ"""
    detail: str = Field(examples=[BlueskyDomainError.message])
