from app.utils.url_utils import expand_url, extract_url, ommit_long_url


def test_extract_url():
    # テキストからURLをすべて抽出する
    text = f"Githubはhttps://github.com/hitohorobe です。ウェブサイトはhttps://hitohorobe.com です。"
    urls = extract_url(text)
    assert urls == ["https://github.com/hitohorobe", "https://hitohorobe.com"]


def test_expand_url():
    # 短縮URLを展開する
    # t.coの場合は展開して返す
    original_url = "https://t.co/GraXSTDt9n"
    expanded_url = expand_url(original_url)
    assert expanded_url == "https://github.com/hitohorobe"


def test_expand_url_amazon():
    # Amazonの短縮URLでOGPを持っているページの場合は展開しない
    # AmazonのURLはすべて展開するとOGP画像がなくなるため
    original_url = "https://amzn.to/3RFJ2HN"
    expanded_url = expand_url(original_url)
    assert expanded_url == "https://amzn.to/3RFJ2HN"


def test_expand_url_twitter():
    # TwitterのURLをx.comになるまで再帰的に展開する
    original_url = "https://t.co/BfZI5kTpvq"
    expanded_url = expand_url(original_url)
    assert expanded_url == "https://x.com/hito_horobe2/status/1805572107662934083"


def test_ommit_long_url():
    # URLを省略表示する
    url = "https://ja.wikipedia.org/wiki/GitHub"
    omitted_url = ommit_long_url(url)
    assert omitted_url == "https://ja.wikipedia.org/wiki..."
    assert len(omitted_url) == 32


def test_ommit_long_url_short():
    # 32文字以下のURLはそのまま返す
    url = "https://x.com/"
    omitted_url = ommit_long_url(url)
    assert omitted_url == url


def get_byte_length():
    # バイト長を取得する
    text = "https://ja.wikipedia.org/wiki/GitHub"
    byte_length = get_byte_length(text)
    assert byte_length == 38


def get_byte_length_japanese():
    # マルチバイト文字の場合
    text = "日本語の文字列です"
    byte_length = get_byte_length(text)
    assert byte_length == 27