from pydantic import BaseModel
from typing import Optional, List

class PhotocardBase(BaseModel):
    pc_id: str
    pc_img: str
    idol_id: str
    idol_name: str
    description: Optional[str] = None
    source_description: Optional[str] = None

class PhotocardSet(BaseModel):
    title: str
    photocards: List[PhotocardBase] = []

class PhotocardsRelease(BaseModel):
    group_name: str
    release_title: str
    release_date: Optional[str] = None
    release_img: str
    photocard_sets: List[PhotocardSet] = []
    special_photocard_sets: List[PhotocardBase] = []


