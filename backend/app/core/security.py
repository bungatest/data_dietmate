"""Token akses bertanda tangan HMAC-SHA256 (format setara JWT HS256, tanpa dependency tambahan)."""

import base64
import hashlib
import hmac
import json
import time

from app.core.config import settings

_HEADER = {"alg": "HS256", "typ": "JWT"}


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(message: bytes) -> str:
    key = settings.SECRET_KEY.encode("utf-8")
    return _b64encode(hmac.new(key, message, hashlib.sha256).digest())


def create_access_token(user_id: str, expires_minutes: int | None = None) -> str:
    """Membuat token akses untuk user_id dengan masa berlaku tertentu."""
    ttl = expires_minutes if expires_minutes is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    now = int(time.time())
    payload = {"sub": user_id, "iat": now, "exp": now + ttl * 60}
    header_part = _b64encode(json.dumps(_HEADER, separators=(",", ":")).encode("utf-8"))
    payload_part = _b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    return f"{header_part}.{payload_part}.{_sign(signing_input)}"


def decode_access_token(token: str) -> str:
    """Memverifikasi token dan mengembalikan user_id. Raise ValueError jika tidak valid/kedaluwarsa."""
    try:
        header_part, payload_part, signature = token.split(".")
    except ValueError as exc:
        raise ValueError("Format token tidak valid.") from exc

    expected = _sign(f"{header_part}.{payload_part}".encode("ascii"))
    if not hmac.compare_digest(expected, signature):
        raise ValueError("Tanda tangan token tidak valid.")

    try:
        payload = json.loads(_b64decode(payload_part))
    except (ValueError, json.JSONDecodeError) as exc:
        raise ValueError("Payload token tidak valid.") from exc

    if int(payload.get("exp", 0)) < int(time.time()):
        raise ValueError("Sesi telah berakhir. Silakan login kembali.")

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise ValueError("Token tidak memiliki identitas pengguna.")
    return user_id
