from pydantic import BaseModel
from typing import Optional

class SearchBase(BaseModel):
    id: str
    name: str
    n_name: Optional[str] = None
    image_uri: Optional[str] = None
    obj_type: str
    release_type: Optional[str] = None