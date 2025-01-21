from pydantic import BaseModel
from typing import Optional, List

class PhotocardBase(BaseModel):
    pc_id: str
    pc_img: str
    group_photo: bool
    idol_id: Optional[str] = None
    idol_name: Optional[str] = None
    description: Optional[str] = None
    source_description: Optional[str] = None

class PhotocardSet(BaseModel):
    title: str
    photocards: List[PhotocardBase] = []

class PhotocardsRelease(BaseModel):
    artist_name: str
    release_title: str
    release_date: Optional[str] = None
    release_img: str
    release_type: Optional[str] = None
    present_members: List[str] = []
    photocard_sets: List[PhotocardSet] = []
    special_photocard_sets: List[PhotocardBase] = []


