#!/usr/bin/env python3
"""
AWS What's New RSS Feed Parser

Usage:
    python3 parse_aws_news_feed.py [--days DAYS]

Arguments:
    --days DAYS     Number of days to look back (default: 7)

Output:
    JSON array of items to stdout
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path


def parse_feed(feed_path: str, days: int = 7) -> list[dict]:
    """Parse AWS What's New RSS feed and filter by date.

    Args:
        feed_path: Path to the RSS feed XML file
        days: Number of days to look back

    Returns:
        List of feed items as dictionaries
    """
    tree = ET.parse(feed_path)
    root = tree.getroot()

    # Calculate cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    items = []
    for item in root.findall('.//item'):
        title_elem = item.find('title')
        link_elem = item.find('link')
        pubdate_elem = item.find('pubDate')
        desc_elem = item.find('description')
        category_elem = item.find('category')

        if title_elem is None or link_elem is None or pubdate_elem is None:
            continue

        title = title_elem.text or ""
        link = link_elem.text or ""
        pubdate_str = pubdate_elem.text or ""
        description = desc_elem.text if desc_elem is not None else ""
        category = category_elem.text if category_elem is not None else ""

        # Parse date (e.g., "Mon, 05 Jan 2026 18:55:00 GMT")
        try:
            pubdate = datetime.strptime(pubdate_str, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
        except ValueError as e:
            print(f"Warning: Failed to parse date '{pubdate_str}': {e}", file=sys.stderr)
            continue

        # Filter by date
        if pubdate < cutoff_date:
            continue

        # Extract slug from URL
        slug = link.split('/')[-1] if link else ""

        # Format date for filename
        date_str = pubdate.strftime("%Y-%m-%d")

        items.append({
            'title': title,
            'link': link,
            'pubDate': pubdate_str,
            'pubDateISO': pubdate.isoformat(),
            'description': description,
            'category': category,
            'slug': slug,
            'filename': f"{date_str}-{slug}.md",
            'year': pubdate.year
        })

    return items


def main():
    parser = argparse.ArgumentParser(
        description='Parse AWS What\'s New RSS feed',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--days',
        type=int,
        default=3,
        help='Number of days to look back (default: 3)'
    )
    parser.add_argument(
        '--feed',
        type=str,
        default='/tmp/aws_news_feed.xml',
        help='Path to the RSS feed XML file (default: /tmp/aws_news_feed.xml)'
    )

    args = parser.parse_args()

    feed_path = Path(args.feed)
    if not feed_path.exists():
        print(f"Error: Feed file not found: {feed_path}", file=sys.stderr)
        sys.exit(1)

    items = parse_feed(str(feed_path), days=args.days)

    # Output as JSON
    print(json.dumps(items, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
