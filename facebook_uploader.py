import requests


def upload_video_to_facebook(
    file_path: str,
    description: str,
    page_id: str,
    access_token: str,
) -> dict:
    url = f"https://graph-video.facebook.com/v19.0/{page_id}/videos"
    data = {
        "description": description or "Video from bot",
        "access_token": access_token,
    }
    with open(file_path, "rb") as video_file:
        files = {"source": video_file}
        response = requests.post(url, data=data, files=files, timeout=120)

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("Invalid response from Facebook API") from exc

    if not response.ok or "error" in payload:
        error_message = payload.get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Facebook upload failed: {error_message}")

    return payload
