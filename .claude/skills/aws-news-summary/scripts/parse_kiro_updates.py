#!/usr/bin/env python3
"""
Kiro Updates Parser

Parses Kiro blog and changelog pages to extract update entries.
Since kiro.dev is a Next.js SPA, this script extracts content from
the server-rendered HTML text nodes.

Usage:
    # Parse blog entries
    curl -sL "https://kiro.dev/blog/" | python3 parse_kiro_updates.py --source blog --days 7

    # Parse changelog entries
    curl -sL "https://kiro.dev/changelog/" | python3 parse_kiro_updates.py --source changelog --days 7

    # Read from file
    python3 parse_kiro_updates.py --source blog --days 7 --feed /tmp/kiro_blog.html

Output: JSON array of entries with title, date, url, description, source fields.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone


MONTH_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
}


def parse_date(date_str: str) -> datetime | None:
    """Parse date strings like 'Feb 5, 2026' or 'November 24, 2025'."""
    date_str = date_str.strip()
    # Pattern: "Mon DD, YYYY" or "Month DD, YYYY"
    match = re.match(r"(\w+)\s+(\d{1,2}),?\s*(\d{4})", date_str)
    if match:
        month_str, day, year = match.groups()
        month = MONTH_MAP.get(month_str)
        if month:
            return datetime(int(year), month, int(day), tzinfo=timezone.utc)
    return None


def parse_blog(html: str, days: int) -> list[dict]:
    """Parse Kiro blog page HTML to extract blog entries."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    entries = []

    # Extract blog post URLs
    urls = re.findall(r'href="(/blog/[^"]+)"', html)
    seen_urls = []
    for u in urls:
        if u not in seen_urls and u != "/blog/":
            seen_urls.append(u)

    # Extract visible text content
    texts = re.findall(r">([^<]{3,500})<", html)
    clean_texts = []
    for t in texts:
        t = t.strip()
        if (t and not t.startswith("{") and not t.startswith("self.")
                and not t.startswith("//") and not t.startswith("(self")
                and not t.startswith("function")
                and "requestAnimationFrame" not in t
                and "configureAnalytics" not in t
                and "stylesheet" not in t
                and "next_" not in t
                and len(t) > 3):
            clean_texts.append(t)

    # Parse blog entries: pattern is "Date", "Title", "Author(s)"
    # Find date patterns and match with subsequent title
    i = 0
    url_idx = 0
    while i < len(clean_texts):
        text = clean_texts[i]
        date = parse_date(text)
        if date and i + 1 < len(clean_texts):
            title = clean_texts[i + 1]
            # Skip navigation/footer items
            if title in ("Loading image...", "Follow us:", "Loading..."):
                i += 1
                continue

            # Decode HTML entities
            title = title.replace("&#x27;", "'").replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")

            if date >= cutoff:
                url = ""
                if url_idx < len(seen_urls):
                    url = f"https://kiro.dev{seen_urls[url_idx]}"
                    url_idx += 1

                entries.append({
                    "title": title,
                    "date": date.strftime("%Y-%m-%d"),
                    "url": url,
                    "source": "kiro-blog",
                })
            else:
                url_idx += 1

            i += 2  # Skip date + title
            continue
        i += 1

    return entries


def parse_changelog(html: str, days: int) -> list[dict]:
    """Parse Kiro changelog page HTML to extract changelog entries."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    entries = []

    # Extract visible text content
    texts = re.findall(r">([^<]{3,500})<", html)
    clean_texts = []
    for t in texts:
        t = t.strip()
        if (t and not t.startswith("{") and not t.startswith("self.")
                and not t.startswith("//") and not t.startswith("(self")
                and not t.startswith("function")
                and "requestAnimationFrame" not in t
                and "configureAnalytics" not in t
                and "stylesheet" not in t
                and "next_" not in t
                and len(t) > 3):
            clean_texts.append(t)

    # Parse changelog entries
    # Pattern: date, optional version/tags, title, description sections
    current_date = None
    current_title = None
    current_descriptions = []
    skip_nav = True  # Skip navigation items at the top

    for text in clean_texts:
        # Decode HTML entities
        text = text.replace("&#x27;", "'").replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")

        date = parse_date(text)
        if date:
            skip_nav = False
            # Save previous entry if exists
            if current_date and current_title and current_date >= cutoff:
                entries.append({
                    "title": current_title,
                    "date": current_date.strftime("%Y-%m-%d"),
                    "url": "https://kiro.dev/changelog/",
                    "description": " ".join(current_descriptions[:3]),
                    "source": "kiro-changelog",
                })
            current_date = date
            current_title = None
            current_descriptions = []
            continue

        if skip_nav:
            continue

        if current_date and not current_title:
            # Skip tags like "Models", "Autonomous agent", version numbers
            if re.match(r"^\d+\.\d+\.\d+$", text):
                continue
            if text in ("Models", "Autonomous agent", "Improvements", "Fixes",
                        "Loading...", "Loading image...", "Follow us:"):
                continue
            current_title = text
        elif current_date and current_title:
            if text not in ("Learn more ->", "Improvements", "Fixes"):
                current_descriptions.append(text)

    # Save last entry
    if current_date and current_title and current_date >= cutoff:
        entries.append({
            "title": current_title,
            "date": current_date.strftime("%Y-%m-%d"),
            "url": "https://kiro.dev/changelog/",
            "description": " ".join(current_descriptions[:3]),
            "source": "kiro-changelog",
        })

    return entries


def main():
    parser = argparse.ArgumentParser(description="Parse Kiro blog/changelog updates")
    parser.add_argument("--source", choices=["blog", "changelog"], required=True,
                        help="Source to parse: blog or changelog")
    parser.add_argument("--days", type=int, default=7,
                        help="Number of days to look back (default: 7)")
    parser.add_argument("--feed", type=str, default=None,
                        help="Path to HTML file (reads from stdin if not specified)")
    args = parser.parse_args()

    if args.feed:
        with open(args.feed, encoding="utf-8") as f:
            html = f.read()
    else:
        html = sys.stdin.read()

    if not html.strip():
        print(json.dumps({"error": "Empty input", "items": []}))
        sys.exit(1)

    if args.source == "blog":
        entries = parse_blog(html, args.days)
    else:
        entries = parse_changelog(html, args.days)

    output = {
        "source": f"kiro-{args.source}",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "days": args.days,
        "total_items": len(entries),
        "items": entries,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
