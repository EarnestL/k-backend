from supabase_client import supabase
from fastapi import APIRouter, HTTPException, Query
from schemas.photocards import PhotocardSet, PhotocardsRelease, PhotocardBase
from typing import Optional

from datetime import date
from utils import get_image_url

router = APIRouter()

#return list of photocard sets of a specific album release
@router.get("/release/{release_id}")
def get_photocards_of_release(
    release_id: str
):
    #data query
    response = None
    if release_id:
        response = supabase.table("photocards").select('*, ...products(product_ver), ...idols(idol_name), ...releases(release_title, release_type, release_date, ...groups(group_name))').eq('release_id', release_id).order("products(product_ver)", desc=False).order("idol_id", desc=True).execute()
    else:
        raise HTTPException(status_code=400, detail="release_id null")

    #post processing
    data = {}
    if response.data:
        #mapping the release information
        artist_name = response.data[0]['group_name'] if response.data[0]['release_type']=='group' else response.data[0]['idol_name']
        data = PhotocardsRelease(**response.data[0], artist_name=artist_name, release_img=get_image_url('AlbumCovers', f"{release_id}_albumcover"), present_members=['all'])

        standard_sets = {}
        special_sets = {}

        standard_set_names = []
        special_set_names = []

        #mapping the pc sets
        for card in response.data:
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
            
            #storing members
            if card['idol_name'] and card['idol_name'] not in data.present_members:
                data.present_members.append(card['idol_name'])
        
        #mapping card sets
        for set_name in standard_set_names:
            data.photocard_sets.append(PhotocardSet(title=set_name, photocards=standard_sets[set_name]))
        
        #combine and map the special card sets
        for name in special_set_names:
            for card in special_sets[name]:
                data.special_photocard_sets.append(PhotocardBase(**card))
        
        return data
    else:
        response = supabase.table("releases").select("*, ...groups(group_name), ...idols(idol_name)").eq('release_id',release_id).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="release not found")
        response.data[0]['artist_name'] = response.data[0]['group_name'] if response.data[0]['release_type']=='group' else response.data[0]['idol_name']
        data = PhotocardsRelease(**response.data[0], release_img=get_image_url('AlbumCovers', f"{release_id}_albumcover"))

    return data

@router.post("/photocards/")
async def insert_photocard(idol_id:Optional[str] = None, source_type:str = None, product_id:str = None, description:str = None, source_description:str = None, release_id:str = None):
    try:
        # Insert row into the Supabase table
        response = None
        if source_description:
            response = supabase.table("photocards").insert({
            "idol_id": str(idol_id),
            "source_type": source_type,
            "description": description,
            "source_description": source_description,
            "release_id": str(release_id),
            }).execute()
        else:
            response = supabase.table("photocards").insert({
            "idol_id": str(idol_id),
            "source_type": source_type,
            "product_id": str(product_id),
            "description": description,
            "release_id": str(release_id),
            }).execute()

        # Check if the insertion was successful
        if response.status_code == 200:
            return {"message": "Photocard inserted successfully", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail=f"Error: {response.json()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))