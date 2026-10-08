"""
File storage for user uploads (profile photos).

Uses Supabase Storage when SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set,
otherwise falls back to the local backend/uploads/ folder (served at /uploads).
"""
import os
import logging
import requests

logger = logging.getLogger("ammachi.storage")

_bucket_ready = False


def _config():
    url = (os.getenv("SUPABASE_URL") or "").rstrip("/")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or ""
    bucket = os.getenv("SUPABASE_STORAGE_BUCKET", "avatars")
    return url, key, bucket


def is_supabase_storage_enabled() -> bool:
    url, key, _ = _config()
    return bool(url and key)


def _headers(key: str) -> dict:
    return {"Authorization": f"Bearer {key}", "apikey": key}


def _ensure_bucket(url: str, key: str, bucket: str):
    """Create the public bucket on first use if it does not exist yet."""
    global _bucket_ready
    if _bucket_ready:
        return
    r = requests.get(f"{url}/storage/v1/bucket/{bucket}", headers=_headers(key), timeout=15)
    if r.status_code != 200:
        r = requests.post(
            f"{url}/storage/v1/bucket",
            headers=_headers(key),
            json={
                "id": bucket,
                "name": bucket,
                "public": True,
                "file_size_limit": 5 * 1024 * 1024,
                "allowed_mime_types": ["image/*"],
            },
            timeout=15,
        )
        if r.status_code not in (200, 201) and "already exists" not in r.text.lower():
            raise RuntimeError(f"Could not create storage bucket '{bucket}': {r.status_code} {r.text[:200]}")
        logger.info("Created Supabase storage bucket '%s'", bucket)
    _bucket_ready = True


def upload_file(content: bytes, path: str, content_type: str) -> str:
    """Store a file and return the URL the frontend should use to display it."""
    if is_supabase_storage_enabled():
        url, key, bucket = _config()
        _ensure_bucket(url, key, bucket)
        r = requests.post(
            f"{url}/storage/v1/object/{bucket}/{path}",
            headers={**_headers(key), "Content-Type": content_type, "x-upsert": "true"},
            data=content,
            timeout=30,
        )
        if r.status_code not in (200, 201):
            raise RuntimeError(f"Supabase upload failed: {r.status_code} {r.text[:200]}")
        return f"{url}/storage/v1/object/public/{bucket}/{path}"

    local_path = os.path.join("uploads", *path.split("/"))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(content)
    return f"/uploads/{path}"


def delete_file(file_url: str):
    """Best-effort removal of a previously stored file (old profile photos)."""
    if not file_url:
        return
    try:
        url, key, bucket = _config()
        marker = f"/storage/v1/object/public/{bucket}/"
        if is_supabase_storage_enabled() and marker in file_url:
            path = file_url.split(marker, 1)[1]
            requests.delete(f"{url}/storage/v1/object/{bucket}/{path}", headers=_headers(key), timeout=15)
        elif file_url.startswith("/uploads/"):
            local_path = os.path.join("uploads", *file_url[len("/uploads/"):].split("/"))
            if os.path.isfile(local_path):
                os.remove(local_path)
    except Exception as e:
        logger.warning("Could not delete old file %s: %s", file_url, e)
