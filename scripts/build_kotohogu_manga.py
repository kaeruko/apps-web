#!/usr/bin/env python3
"""Generate Kotohogu's static manga listing before website deployment.

Root-level image: one manga story per image.
Subdirectory: one manga story, images ordered by natural filename order.
titles.json: optional {"file:filename.png": "Title", "folder:directory": "Title"}.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
MANGA = ROOT / "public" / "kotohogu" / "manga"
PAGE = ROOT / "public" / "kotohogu" / "manga.html"
TITLES = MANGA / "titles.json"
START = "<!-- MANGA_INDEX_START -->"
END = "<!-- MANGA_INDEX_END -->"
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"}


def natural_sort(text: str):
    return [(1, int(part)) if part.isdigit() else (0, part.casefold())
            for part in re.split(r"(\d+)", text)]


def safe_name(name: str):
    if not name or name in {".", ".."} or any(c in name for c in ("?", "#", "%", "\\", "/")):
        raise ValueError("Unsupported manga filename: " + repr(name))


def filename_title(stem: str) -> str:
    title = re.sub(r"^\d+[\s._-]+", "", stem)
    return re.sub(r"[_-]+", " ", title).strip()


def image_files(folder: Path):
    return sorted(
        (p for p in folder.iterdir() if p.is_file()
         and not p.is_symlink() and not p.name.startswith(".")
         and p.suffix.lower() in EXTENSIONS),
        key=lambda item: natural_sort(item.name)
    )


def find_stories():
    if not MANGA.is_dir():
        raise FileNotFoundError("Manga folder is missing: " + str(MANGA))
    custom = json.loads(TITLES.read_text(encoding="utf-8-sig")) if TITLES.is_file() else {}
    if not isinstance(custom, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in custom.items()):
        raise ValueError("titles.json must map image/folder IDs to title strings")

    found, stories = set(), []
    for entry in sorted(MANGA.iterdir(), key=lambda p: natural_sort(p.name)):
        if entry.name.startswith(".") or entry.name in {"README.txt", "titles.json"}:
            continue
        if entry.is_symlink():
            raise ValueError("Symlinks are not supported: " + str(entry))
        if entry.is_file():
            if entry.suffix.lower() not in EXTENSIONS:
                continue
            key, pages, fallback = "file:" + entry.name, [entry], entry.stem
        elif entry.is_dir():
            safe_name(entry.name)
            if any(child.is_dir() for child in entry.iterdir()):
                raise ValueError("Nested story folders are not supported: " + str(entry))
            pages = image_files(entry)
            if not pages:
                continue
            key, fallback = "folder:" + entry.name, entry.name
        else:
            raise ValueError("Unexpected manga entry: " + str(entry))

        for p in pages:
            safe_name(p.name)
        if key in found:
            raise ValueError("Duplicate manga ID: " + key)
        found.add(key)
        title = custom.get(key, filename_title(fallback))
        if not title or len(title) > 100 or title != title.strip() or "\n" in title or "\r" in title:
            raise ValueError("Invalid title: " + key)
        stories.append((title, pages))

    unused = set(custom) - found
    if unused:
        raise ValueError("Manga titles refer to files that are missing: " + ", ".join(sorted(unused)))
    return stories


def story_html(title: str, pages: list[Path], number: int) -> str:
    title_attr = html.escape(title, quote=True)
    all_pages = []
    for i, page in enumerate(pages, 1):
        url = "./" + "/".join(quote(segment, safe="") for segment in page.relative_to(MANGA.parent).parts)
        all_pages.append(
            '<figure class="story-page"><img loading="lazy" src="' + url
            + '" alt="' + title_attr + "・" + str(i)
            + 'ページ目"><figcaption>' + str(i) + " / " + str(len(pages))
            + "</figcaption></figure>"
        )
    first_url = "./" + "/".join(quote(segment, safe="") for segment in pages[0].relative_to(MANGA.parent).parts)
    sub = "読み切りまんが" if len(pages) == 1 else "全" + str(len(pages)) + "ページ"
    return (
        '<details class="story" id="manga-' + str(number).zfill(3) + '"><summary>'
        '<span class="story-cover"><img loading="lazy" src="' + first_url + '" alt="" width="140" height="180"></span>'
        '<span class="story-caption"><strong>' + title_attr + '</strong><small>' + sub
        + '</small><span class="story-cta">まんがを読む ↓</span></span></summary>'
        '<div class="story-pages">' + "\n".join(all_pages) + "</div></details>"
    )


def main():
    stories = find_stories()
    document = PAGE.read_text(encoding="utf-8")
    if document.count(START) != 1 or document.count(END) != 1:
        raise ValueError("Manga HTML index markers missing or duplicated")
    prefix, tail = document.split(START, 1)
    _, suffix = tail.split(END, 1)
    if not stories:
        middle = '<p class="empty">まんがはただいま準備中。新しいお話を楽しみにしていてね。</p>'
    else:
        middle = "\n".join(story_html(title, pages, i) for i, (title, pages) in enumerate(stories, 1))
    updated = prefix + START + "\n" + middle + "\n" + END + suffix
    if document != updated:
        PAGE.write_text(updated, encoding="utf-8", newline="\n")
    print("Kotohogu manga index:", len(stories), "stories")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print("Kotohogu manga index generation failed:", exc, file=sys.stderr)
        sys.exit(1)
