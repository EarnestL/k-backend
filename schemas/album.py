from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class AlbumBase(BaseModel):
    release_id: str
    album_image: Optional[str] = None
    release_title: str
    artist_banner: str
    artist_name: str
    artist_n_name: str
    release_date: Optional[date] = None
    product_count: int = 0

class ProductBase(BaseModel):
    name: str

class AlbumDetails(AlbumBase):
    products: List[ProductBase] = []

