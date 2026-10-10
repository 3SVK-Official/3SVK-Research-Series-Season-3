import hashlib
import hmac
import json


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical_json(value)).hexdigest()


def sign_body(secret, body):
    if not secret:
        raise RuntimeError("FIELDRELAY_SHARED_SECRET is not configured")
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()


def verify_signature(secret, body, supplied):
    if not secret or not supplied:
        return False
    expected = sign_body(secret, body)
    return hmac.compare_digest(expected, supplied)
