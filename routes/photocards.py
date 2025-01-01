from supabase_client import supabase
from fastapi import APIRouter, HTTPException, Query
from schemas.photocards import PhotocardSet, PhotocardsRelease, PhotocardBase

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
        "title:product_ver, photocards: product_id(*, ...idols(idol_name, idol_id)), ...releases(...groups(group_name, group_normalized_name), release_title, release_date)"
    )
    response = None
    newResponse = None
    if release_id:
        response = supabase.table("products").select(query).eq('release_id',release_id).execute()
        newResponse = supabase.table("photocards"). select('*, ...products(product_ver), ...idols(idol_name), ...releases(release_title, release_date, ...groups(group_name))').eq('release_id', release_id).execute()
    else:
        raise HTTPException(status_code=400, detail="release_id null")

    #post processing
    data = {}
    if response.data:
        #mapping the release information
        data = PhotocardsRelease(**newResponse.data[0], release_img=get_image_url('AlbumCovers', f"{release_id}_albumcover"))

        standard_sets = {}
        special_sets = {}

        standard_set_names = []
        special_set_names = []

        #mapping the pc sets
        for card in newResponse.data:
            card['pc_img'] = get_image_url('Photocards', f"{card['pc_id']}_pc")
            if card['source_type'] == 'product':
                if card['product_ver'] not in standard_sets:
                    standard_sets[f"{card['product_ver']}"] = [card]
                    standard_set_names.append(card['product_ver'])
                else:
                    standard_sets[f"{card['product_ver']}"].append(card)
            elif card['source_type'] == 'other':
                if card['source_description'] not in special_sets:
                    special_sets[f"{card['source_description']}"] = [card]
                    special_set_names.append(card['source_description'])
                else:
                    special_sets[f"{card['source_description']}"].append(card)

        #mapping card sets
        for set_name in standard_set_names:
            data.photocard_sets.append(PhotocardSet(title=set_name, photocards=standard_sets[set_name]))

        #combine and map the special card sets
        for name in special_set_names:
            for card in special_sets[name]:
                data.special_photocard_sets.append(PhotocardBase(**card))
        
        return data
    else:
        response = supabase.table("releases").select("*, ...groups(group_name)").eq('release_id',release_id).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="release not found")
        data = PhotocardsRelease(**response.data[0], release_img=get_image_url('AlbumCovers', f"{release_id}_albumcover"))

    return data