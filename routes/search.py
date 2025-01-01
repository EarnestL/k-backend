from supabase_client import supabase
from fastapi import APIRouter, HTTPException
from schemas.search import SearchBase
from utils import get_image_url

router = APIRouter()

#return list of recent albums
@router.get("")
def general_search(search_query: str = None):

    limit = 5
    data = []

    ################################################# release search
    response = []
    if limit:
        response = supabase.table("releases").select(
            "id:release_id, name:release_title, release_type, ...groups(normalized_group_name), ...idols(normalized_idol_name)"
        ).ilike("release_title", f"%{search_query}%").limit(limit).execute()

    #post processing
    if limit and response.data:
        for release in response.data:
            image_uri = get_image_url("AlbumCovers", f"{release['id']}_albumcover")
            obj_type = "release"
            n_name = release['normalized_group_name'] if release['release_type']=='group' else release['normalized_idol_name']
            data.append(SearchBase(**release, image_uri=image_uri, obj_type=obj_type, n_name=n_name))
        limit -= len(data)

    ################################################# group search
    response = []
    if limit:
        response = supabase.table("groups").select(
            "id:group_id, name:group_name, n_name:normalized_group_name"
        ).ilike("group_name", f"%{search_query}%").execute()

    #post processing
    if limit and response.data:
        for group in response.data:
            image_uri = get_image_url("ArtistProfiles", f"{group['id']}_profile")
            obj_type = "group"
            data.append(SearchBase(**group, image_uri=image_uri, obj_type=obj_type))
        limit -= len(data)

    ################################################# idol search
    response = []
    if limit:
        response = supabase.table("idols").select(
            "id:idol_id, name:idol_name"
        ).ilike("idol_name", f"%{search_query}%").execute()

    #post processing
    if limit and response.data:
        for idol in response.data:
            image_uri = get_image_url("ArtistProfiles", f"{idol['id']}_profile")
            obj_type = "idol"
            data.append(SearchBase(**idol, image_uri=image_uri, obj_type=obj_type))
        limit -= len(data)

    return data