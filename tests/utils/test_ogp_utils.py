import pytest

from app.models.ogp_models import OGP
from app.utils import ogp_utils
from app.utils.ogp_utils import _get_ogp_from_requests, get_ogp


class TestOgpUtils:
    def test_get_ogp(self, mocker):
        # OGPを取得する
        mock_response = OGP(
            title="hitohorobe - Overview",
            description="hitohorobe has 70 repositories available. Follow their code on GitHub.",
            image="https://avatars.githubusercontent.com/u/52458640?v=4?s=400",
            url="https://github.com/hitohorobe",
            site_name="GitHub",
            type="profile",
        )
        mocker.patch.object(ogp_utils, "_get_ogp_from_bluesky", return_value=mock_response)
        url = "https://github.com/hitohorobe"
        ogp = get_ogp(url)
        assert ogp.title
        assert ogp.description
        assert ogp.image
        assert ogp.url


    def test_get_ogp_twitter(self, mocker):
        # TwitteからOGPを取得する
        # mockの設定
        mock_response = OGP(
            title="X",
            site_name="X",
        )
        mocker.patch.object(ogp_utils, "_get_ogp_from_requests", return_value=mock_response)
        url = "https://x.com/hito_horobe2/status/1805572107662934083"
        ogp = get_ogp(url)
        # センシティブ判定があるときは画像が返ってこない
        # サイト名とタイトルは必ず返ってくる
        assert ogp.title
        assert ogp.site_name


    def test_get_ogp_error(self, mocker):
        # 存在しないURLの場合はNoneを返す
        url = "https://notexist.url/"
        ogp = get_ogp(url)
        assert ogp is None


    def test_get_ogp_dmm(self, mocker):
        # DMMのURLはcardyb.bsky.appではなく直接取得し、
        # 年齢確認Cookieを付与して取得する
        mock_response = OGP(title="DMMブックス", site_name="DMM.com")
        mock = mocker.patch.object(
            ogp_utils, "_get_ogp_from_requests", return_value=mock_response
        )
        url = "https://al.dmm.com/?lurl=https%3A%2F%2Fbook.dmm.com%2F&af_id=dmmg-001"
        ogp = get_ogp(url)
        assert ogp.title
        mock.assert_called_once_with(
            url, "Mozilla/5.0 (Windows NT 6.1; Win64; x64)", cookies={"age_check_done": "1"}
        )


    def test_get_ogp_fanza(self, mocker):
        # FANZAのURLはcardyb.bsky.appではなく直接取得し、
        # 年齢確認Cookieを付与して取得する
        mock_response = OGP(title="FANZA同人", site_name="FANZA")
        mock = mocker.patch.object(
            ogp_utils, "_get_ogp_from_requests", return_value=mock_response
        )
        url = "https://al.fanza.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2F&af_id=dmmg-002"
        ogp = get_ogp(url)
        assert ogp.title
        mock.assert_called_once_with(
            url, "Mozilla/5.0 (Windows NT 6.1; Win64; x64)", cookies={"age_check_done": "1"}
        )


    def test_get_ogp_rakuten(self, mocker):
        # 楽天のURLはcardyb.bsky.appではなく直接取得する
        # (DMM用の年齢確認Cookieは付与しない)
        mock_response = OGP(title="楽天ブックス", site_name="Rakuten")
        mock = mocker.patch.object(
            ogp_utils, "_get_ogp_from_requests", return_value=mock_response
        )
        url = "https://a.r10.to/hgWJRV"
        ogp = get_ogp(url)
        assert ogp.title
        mock.assert_called_once_with(url, "Mozilla/5.0 (Windows NT 6.1; Win64; x64)")


    def test_get_ogp_from_requests_follows_redirect(self, mocker):
        # 3xxで止まらず、Locationヘッダーを辿って最終的にOGPを取得する
        redirect_response = mocker.Mock(status_code=301, headers={"Location": "https://example.com/final"})
        final_response = mocker.Mock(
            status_code=200,
            text='<html><head><meta property="og:title" content="Final Page"></head></html>',
        )
        mocker.patch.object(
            ogp_utils.requests, "get", side_effect=[redirect_response, final_response]
        )
        ogp = _get_ogp_from_requests("https://short.example/abc", "UA")
        assert ogp.title == "Final Page"


    def test_get_ogp_from_requests_redirect_without_location(self, mocker):
        # Locationヘッダーの無い3xxの場合は、本当にアクセス不能なのでNoneを返す
        redirect_response = mocker.Mock(status_code=302, headers={})
        mocker.patch.object(ogp_utils.requests, "get", return_value=redirect_response)
        ogp = _get_ogp_from_requests("https://short.example/abc", "UA")
        assert ogp is None


    # GithubからCI実施時、AmazonにブロックされてCIでのテストが通らないため一旦コメントアウトする
    # def test_get_ogp_from_prime_video():
    #     # Prime VideoのOGPを取得する
    #     url = "https://www.amazon.co.jp/dp/B0CJQR5LG7"
    #     ogp = get_ogp(url)
    #     assert ogp.title
    #     assert ogp.description
    #     assert ogp.image
    #     assert ogp.url
    #     assert ogp.site_name
    #     assert ogp.type
    #
    #
    # def test_get_ogp_from_amazon_shorten_url():
    #     # Amazonの短縮URLからOGPを取得する
    #     url = "https://amzn.to/3OlWOgM"
    #     ogp = get_ogp(url)
    #     assert ogp.title
    #     assert ogp.description
    #     assert ogp.image
    #     assert ogp.url
    #     assert ogp.site_name
    #     assert ogp.type
    #
    #
    # def test_get_ogp_from_amazon_no_ogp_page():
    #     # AmazonのOGPがないページから疑似的なOGPを作成する
    #     url = "https://www.amazon.co.jp/kindle-dbs/storefront"
    #     ogp = get_ogp(url)
    #     assert ogp.title
    #     assert ogp.description
    #     assert ogp.url
