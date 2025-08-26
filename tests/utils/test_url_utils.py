from app.utils.url_utils import (
    expand_url,
    extract_hashtags,
    extract_url,
    ommit_long_url,
)


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


def test_expand_url_al_dmm_com():
    # DMM.comのアフィリエイトURLは展開しない
    original_url = "https://al.dmm.com/?lurl=https%3A%2F%2Fbook.dmm.com%2F&af_id=dmmg-001&ch=toolbar&ch_id=link"
    expanded_url = expand_url(original_url)
    assert expanded_url == original_url


def test_expand_url_al_dmm_co_jp():
    # DMM.co.jpのアフィリエイトURLは展開しない
    original_url = "https://al.dmm.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdc%2Fdoujin%2F&af_id=dmmg-001&ch=toolbar&ch_id=link"
    expanded_url = expand_url(original_url)
    assert expanded_url == original_url


def test_expand_url_al_fanza_com():
    # FanzaのアフィリエイトURLは展開しない
    original_url = "https://al.fanza.com/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdc%2Fdoujin%2F-%2Fdetail%2F%3D%2Fcid%3Dd_065917%2F&af_id=dmmg-002&ch=link_tool&ch_id=link"
    expanded_url = expand_url(original_url)
    assert expanded_url == original_url


def test_expand_url_al_fanza_co_jp():
    # Fanza.co.jpのアフィリエイトURLは展開しない
    original_url = "https://al.fanza.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdc%2Fdoujin%2F-%2Fdetail%2F%3D%2Fcid%3Dd_065917%2F&af_id=dmmg-002&ch=link_tool&ch_id=link"
    expanded_url = expand_url(original_url)
    assert expanded_url == original_url


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


def test_extract_hashtags():
    # テキストからハッシュタグを抽出する
    text = "これはテストです。#テスト #Python #GitHub"
    hashtags = extract_hashtags(text)
    assert hashtags == ["#テスト", "#Python", "#GitHub"]
    text2 = "これはハッシュタグを含まないテキストです https://example.com#top"
    hashtags2 = extract_hashtags(text2)
    assert hashtags2 == []
    text3 = "#ハッシュタグ これはハッシュタグが文頭のパターン"
    hashtags3 = extract_hashtags(text3)
    assert hashtags3 == ["#ハッシュタグ"]
    text4 = "これはハッシュタグが文末のパターン #ハッシュタグ"
    hashtags4 = extract_hashtags(text4)
    assert hashtags4 == ["#ハッシュタグ"]
    text5 = "これは改行後にハッシュタグがあるパターン\n#ハッシュタグ"
    hashtags5 = extract_hashtags(text5)
    assert hashtags5 == ["#ハッシュタグ"]


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
