from app.utils.ogp_utils import get_ogp


def test_get_ogp():
    # OGPを取得する
    url = "https://github.com/hitohorobe"
    ogp = get_ogp(url)
    assert ogp.title
    assert ogp.description
    assert ogp.image
    assert ogp.url


def test_get_ogp_twitter():
    # TwitteからOGPを取得する
    url = "https://x.com/hito_horobe2/status/1805572107662934083"
    ogp = get_ogp(url)
    # センシティブ判定があるときは画像が返ってこない
    # サイト名とタイトルは必ず返ってくる
    assert ogp.title
    assert ogp.site_name


def test_get_opg_error():
    # 存在しないURLの場合はNoneを返す
    url = "https://notexist.url/"
    ogp = get_ogp(url)
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
