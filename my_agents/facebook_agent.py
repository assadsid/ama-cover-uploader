import requests
from my_config.facebook_config import ACCESS_TOKEN, PAGE_ID

def upload_facebook_cover(image_path: str) -> dict:
    try:
        # Upload photo (unpublished)
        upload_url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"
        with open(image_path, "rb") as image_file:
            response = requests.post(
                upload_url,
                files={"source": image_file},
                data={"published": "false", "access_token": ACCESS_TOKEN}
            )

        if response.status_code != 200:
            return {"success": False, "error": response.text}

        photo_id = response.json().get("id")

        # Set it as cover
        cover_url = f"https://graph.facebook.com/v18.0/{PAGE_ID}"
        response2 = requests.post(
            cover_url,
            data={"cover": photo_id, "access_token": ACCESS_TOKEN}
        )

        if response2.status_code == 200:
            return {"success": True, "response": response2.json()}
        else:
            return {"success": False, "error": response2.text}

    except Exception as e:
        return {"success": False, "error": str(e)}
