from typing import Optional

from pydantic import BaseModel, HttpUrl


class OGP(BaseModel):
    """Open Graph Protocol Model"""

    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[HttpUrl] = None
    url: Optional[HttpUrl] = None
    site_name: Optional[str] = None
    type: Optional[str] = None
