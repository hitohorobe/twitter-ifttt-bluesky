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
    # 以前は画像が取得できたが、今はできずタイトルとサイト名しか取れない
    assert ogp.title
    assert ogp.site_name


def test_get_opg_error():
    # 存在しないURLの場合はNoneを返す
    url = "https://notexist.url/"
    ogp = get_ogp(url)
    assert ogp is None


