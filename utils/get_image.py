from supabase_client import SUPABASE_URL

def get_image_url(path:str, name:str):
    return (
        f"{SUPABASE_URL}/storage/v1/object/KBucket/{path}/{name}.jpg"
    )