import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse , parse_qs


def main():
    file_path = Path(
        "data/raw/Linh Đan_90.json"
    )

    if not file_path.exists():
        print(
            f"Không tìm thấy file: {file_path}"
        )
        return

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    messages = data.get(
        "messages",
        []
    )

    raw_type_counter = Counter()
    media_type_counter = Counter()

    # ============================
    # 1. ĐẾM RAW MESSAGE TYPE
    # ============================

    for message in messages:

        raw_type = message.get(
            "type",
            "NO_TYPE"
        )

        raw_type_counter[
            raw_type
        ] += 1

    print(
        "===== RAW MESSAGE TYPES ====="
    )

    for raw_type, count in raw_type_counter.items():

        print(
            f"{raw_type}: {count}"
        )

    # ============================
    # 2. KIỂM TRA MEDIA TYPE
    # ============================

    for message in messages:

        media = message.get(
            "media",
            []
        )

        if not media:
            continue

        for item in media:

            if isinstance(item, dict):

                media_type = (
                    item.get("type")
                    or item.get("mediaType")
                    or item.get("mimeType")
                    or item.get("mime_type")
                    or item.get("contentType")
                    or "UNKNOWN"
                )

                media_type_counter[
                    media_type
                ] += 1

            else:

                media_type_counter[
                    "NON_DICT_MEDIA"
                ] += 1

    print()
    print(
        "===== MEDIA TYPES ====="
    )

    if media_type_counter:

        for media_type, count in media_type_counter.items():

            print(
                f"{media_type}: {count}"
            )

    else:

        print(
            "Không tìm thấy media."
        )

    # ============================
    # 3. XEM CẤU TRÚC MEDIA
    # ============================

    print()
    print(
        "===== MEDIA STRUCTURE ====="
    )

    shown = 0

    for message in messages:

        media = message.get(
            "media",
            []
        )

        if not media:
            continue

        for item in media:

            if not isinstance(
                item,
                dict
            ):
                continue

            print()
            print(
                f"--- Media sample {shown + 1} ---"
            )

            print(
                "Media keys:",
                list(item.keys())
            )

            print(
                "type:",
                item.get("type")
            )

            print(
                "mediaType:",
                item.get("mediaType")
            )

            print(
                "mimeType:",
                item.get("mimeType")
            )

            print(
                "mime_type:",
                item.get("mime_type")
            )

            print(
                "contentType:",
                item.get("contentType")
            )

            shown += 1

            if shown >= 5:
                break

        if shown >= 5:
            break

    if shown == 0:

        print(
            "Không tìm thấy media object dạng dict."
        )
    # ============================
    # 4. ĐẾM ĐUÔI FILE MEDIA
    # ============================

    extension_counter = Counter()

    for message in messages:

        media = message.get(
            "media",
            []
        )

        for item in media:

            if not isinstance(item, dict):
                continue

            uri = item.get("uri")

            if not uri:
                extension_counter[
                    "NO_EXTENSION"
                ] += 1
                continue

            extension = Path(uri).suffix.lower()

            if extension:
                extension_counter[
                    extension
                ] += 1
            else:
                extension_counter[
                    "NO_EXTENSION"
                ] += 1

    print()
    print(
        "===== MEDIA FILE EXTENSIONS ====="
    )

    for extension, count in extension_counter.items():

        print(
            f"{extension}: {count}"
        )


    # ============================
    # 5. KIỂM TRA CẤU TRÚC URI
    # ============================

    scheme_counter = Counter()
    query_key_counter = Counter()
    uri_keyword_counter = Counter()

    keywords = [
        "image",
        "photo",
        "video",
        "audio",
        "voice",
        "gif",
        "sticker"
    ]

    for message in messages:

        media = message.get(
            "media",
            []
        )

        for item in media:

            if not isinstance(item, dict):
                continue

            uri = item.get("uri")

            if not uri:
                continue

            parsed = urlparse(uri)

            scheme = parsed.scheme or "NO_SCHEME"

            scheme_counter[scheme] += 1

            query = parse_qs(
                parsed.query
            )

            for key in query.keys():
                query_key_counter[key] += 1

            uri_lower = uri.lower()

            for keyword in keywords:

                if keyword in uri_lower:
                    uri_keyword_counter[
                        keyword
                    ] += 1

    print()
    print(
        "===== URI SCHEMES ====="
    )

    for scheme, count in scheme_counter.items():
        print(
            f"{scheme}: {count}"
        )

    print()
    print(
        "===== URI QUERY KEYS ====="
    )

    if query_key_counter:

        for key, count in query_key_counter.items():
            print(
                f"{key}: {count}"
            )

    else:
        print(
            "Không có query parameters"
        )

    print()
    print(
        "===== URI KEYWORDS ====="
    )

    if uri_keyword_counter:

        for keyword, count in uri_keyword_counter.items():
            print(
                f"{keyword}: {count}"
            )

    else:
        print(
            "Không tìm thấy keyword media"
        )        

if __name__ == "__main__":
    main()