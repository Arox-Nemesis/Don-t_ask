from hashlib import sha256


def generate_hash(text: str) -> str:
    return sha256(
        text.encode("utf-8")
    ).hexdigest()


def safe_get(dictionary, key, default=None):
    return dictionary.get(key, default)


def truncate(text, length=300):

    if not text:
        return ""

    if len(text) <= length:
        return text

    return text[: length - 3] + "..."
