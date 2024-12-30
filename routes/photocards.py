from supabase_client import supabase
from fastapi import APIRouter, HTTPException, Query
from schemas.photocards import PhotocardSet

from datetime import date
from utils import get_image_url

router = APIRouter()

#return list of photocard sets of a specific album release
@router.get("/release/{release_id}")
def get_photocards_of_release(
    release_id: str
):
    #data query
    query = (
        "title:product_ver, photocards: product_id(*, ...idols(idol_name, idol_id)), ...releases(...groups(group_name), release_title, release_date)"
    )

    response = None
    if release_id:
        response = supabase.table("products").select(query).eq('release_id',release_id).execute()
    else:
        raise HTTPException(status_code=400, detail="release_id null")

    #post processing
    data = []
    for set in response.data:
        set['release_img'] = get_image_url('AlbumCovers', f"{release_id}_albumcover")
        for j, pc in enumerate(set['photocards']):
            set['photocards'][j]['pc_img'] = get_image_url("Photocards", f"{set['photocards'][j]['pc_id']}_pc")
        data.append(PhotocardSet(**set))

    return data