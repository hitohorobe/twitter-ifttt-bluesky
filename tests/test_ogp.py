from app.utils.ogp_utils import get_ogp


def test_get_ogp():
    # OGPを取得する
    url = "https://github.com/hitohorobe"
    ogp = get_ogp(url)
    assert ogp.title
    assert ogp.description
    assert ogp.image
    assert ogp.url
