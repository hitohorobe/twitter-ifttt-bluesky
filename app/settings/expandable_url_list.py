T_CO_HOST = "t.co"

# 転送が発生しなくなるまで再帰的に展開を続ける対象ドメイン
# (将来「展開しないと不都合が起こるドメイン」が増えた場合はここに追加する)
TWITTER_INTERNAL_HOSTS = {"twitter.com", "x.com"}

EXPANDABLE_HOSTS = {T_CO_HOST} | TWITTER_INTERNAL_HOSTS
