from supabase_client import supabase
from fastapi import APIRouter, HTTPException, Query
from schemas.album import AlbumBase

from datetime import date
from utils import get_image_url

router = APIRouter()

#return list of recent albums
@router.get("/releases")
def get_recent_albums(
    group_id: str = Query(None),
    group_n_name: str = Query(None)
):
    #query    
    query = (
        "release_id, release_title, release_type, release_date, product_count,"
        "...idols(idol_id, idol_name, normalized_idol_name), ...groups(group_id, group_name, normalized_group_name)"
    )
    if group_id:
        response = supabase.table("releases").select(query).eq('group_id',group_id).order('release_date', desc=True).execute()
    elif group_n_name:
        response = supabase.table("releases").select(query).order('release_date', desc=True).execute()
    else:
        response = supabase.table("releases").select(query).lte('release_date',date.today()).order('release_date', desc=True).limit(20).execute()

    #post processing
    data = []
    if response.data:
        for release in response.data:
            #additional processing for dealing with normalized name query
            if group_n_name and release['normalized_group_name'] != group_n_name:
                continue

            artist_name = ''
            artist_banner = ''
            artist_n_name = release['normalized_idol_name'] if not release['normalized_group_name'] else release['normalized_group_name']
            album_image = get_image_url("AlbumCovers", f"{release['release_id']}_albumcover")
            if release['release_type'] == 'solo':
                artist_banner = get_image_url("ArtistBanners", f"{release['idol_id']}_banner")
                artist_name = release['idol_name']
            elif release['release_type'] == 'group':
                artist_banner = get_image_url("ArtistBanners", f"{release['group_id']}_banner")
                artist_name = release['group_name']

            data.append(AlbumBase(**release, album_image=album_image, artist_name=artist_name, artist_n_name=artist_n_name, artist_banner=artist_banner)) 
    return data

#return release details
@router.get("/release/{release_id}")
def get_recent_albums(
    release_id: str
):
    query = (
        "*"
    )
    response = supabase.table("releases").select(query).eq('release_id',release_id).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="album not found")

    data = response.data[0]
    return data
    