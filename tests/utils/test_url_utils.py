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
    # t.coの場合は1回展開し、展開先がTwitter/X内部ドメインでなければそのまま返す
    original_url = "https://t.co/GraXSTDt9n"
    expanded_url = expand_url(original_url)
    assert expanded_url == "https://github.com/hitohorobe"


def test_expand_url_amazon():
    # Amazonの短縮URLでOGPを持っているページの場合は展開しない
    # AmazonのURLはすべて展開するとOGP画像がなくなるため
    # (amzn.to は t.co でも Twitter/X 内部ドメインでもないため、
    #  expand_url のガードによりリクエストすら送らずそのまま返る)
    original_url = "https://amzn.to/3RFJ2HN"
    expanded_url = expand_url(original_url)
    assert expanded_url == "https://amzn.to/3RFJ2HN"


def test_expand_url_twitter():
    # t.co経由でリダイレクトされた先がTwitter/X内部ドメイン(x.com)の場合は、
    # リダイレクトが発生しなくなるまで再帰的に展開する
    original_url = "https://t.co/BfZI5kTpvq"
    expanded_url = expand_url(original_url)
    assert expanded_url == "https://x.com/hito_horobe2/status/1805572107662934083"


def test_expand_url_al_dmm_com():
    # DMM.comのアフィリエイトURLは展開しない
    # (t.co でも Twitter/X 内部ドメインでもないため展開されない)
    original_url = "https://al.dmm.com/?lurl=https%3A%2F%2Fbook.dmm.com%2F&af_id=dmmg-001&ch=toolbar&ch_id=link"
    expanded_url = expand_url(original_url)
    assert expanded_url == original_url


def test_expand_url_al_dmm_co_jp():
    # DMM.co.jpのアフィリエイトURLは展開しない
    # (t.co でも Twitter/X 内部ドメインでもないため展開されない)
    original_url = "https://al.dmm.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdc%2Fdoujin%2F&af_id=dmmg-001&ch=toolbar&ch_id=link"
    expanded_url = expand_url(original_url)
    assert expanded_url == original_url


def test_expand_url_al_fanza_com():
    # FanzaのアフィリエイトURLは展開しない
    # (t.co でも Twitter/X 内部ドメインでもないため展開されない)
    original_url = "https://al.fanza.com/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdc%2Fdoujin%2F-%2Fdetail%2F%3D%2Fcid%3Dd_065917%2F&af_id=dmmg-002&ch=link_tool&ch_id=link"
    expanded_url = expand_url(original_url)
    assert expanded_url == original_url


def test_expand_url_al_fanza_co_jp():
    # Fanza.co.jpのアフィリエイトURLは展開しない
    # (t.co でも Twitter/X 内部ドメインでもないため展開されない)
    original_url = "https://al.fanza.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdc%2Fdoujin%2F-%2Fdetail%2F%3D%2Fcid%3Dd_065917%2F&af_id=dmmg-002&ch=link_tool&ch_id=link"
    expanded_url = expand_url(original_url)
    assert expanded_url == original_url


def test_expand_url_rakuten():
    # 楽天アフィリエイトのURLは展開しない
    # (t.co経由でこのURLにリダイレクトされた場合、アフィリエイトのリダイレクトを
    #  壊さないよう、これ以上展開してはいけない。楽天のドメインは t.co でも
    #  Twitter/X 内部ドメインでもないため、expand_url のガードにより
    #  リクエストすら送らずそのまま返る)
    original_url = "https://hb.afl.rakuten.co.jp/ichiba/2cd96950.92086c80.2cd96951.9968d295/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fbook%2F977831%2F&link_type=hybrid_url&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJoeWJyaWRfdXJsIiwic2l6ZSI6IjI0MHgyNDAiLCJuYW0iOjEsIm5hbXAiOiJyaWdodCIsImNvbSI6MSwiY29tcCI6ImRvd24iLCJwcmljZSI6MSwiYm9yIjoxLCJjb2wiOjEsImJidG4iOjEsInByb2QiOjAsImFtcCI6ZmFsc2V9"
    expanded_url = expand_url(original_url)
    assert expanded_url == original_url


def test_expand_url_a_r10():
    # 楽天アフィリエイトの短縮URLは展開しない
    # (t.co経由でこのURLにリダイレクトされた場合、アフィリエイトのリダイレクトを壊さないよう、
    # これ以上展開してはいけない。楽天のドメインは t.co でも
    #  Twitter/X 内部ドメインでもないため、expand_url のガードにより
    # リクエストすら送らずそのまま返る)
    original_url = "https://a.r10.to/hgWJRV"
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
