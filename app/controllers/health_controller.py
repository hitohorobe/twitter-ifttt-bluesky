from fastapi import APIRouter

router = APIRouter()


@router.get("/health")

def get_health():
    """GET のヘルスチェック用エンドポイント
    """
    return {"status": "get alive"}


@router.post("/health")
def post_health():
    """POST のヘルスチェック用エンドポイント
    """
    return {"status": "post alive"}
