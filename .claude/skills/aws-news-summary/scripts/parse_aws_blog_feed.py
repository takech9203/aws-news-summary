#!/usr/bin/env python3
"""
AWS Blog Atom Feed Parser

Usage:
    python3 parse_aws_blog_feed.py [--days DAYS]

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
    """Parse AWS Blog Atom feed and filter by date.

    Args:
        feed_path: Path to the Atom feed XML file
        days: Number of days to look back

    Returns:
        List of feed items as dictionaries
    """
    tree = ET.parse(feed_path)
    root = tree.getroot()

    # Atom namespace
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    # Calculate cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    items = []
    for entry in root.findall('.//atom:entry', ns):
        title_elem = entry.find('atom:title', ns)
        link_elem = entry.find('atom:link[@rel="alternate"]', ns)
        published_elem = entry.find('atom:published', ns)
        summary_elem = entry.find('atom:summary', ns)

        if title_elem is None or link_elem is None or published_elem is None:
            continue

        title = title_elem.text or ""
        link = link_elem.get('href', '') if link_elem is not None else ""
        published_str = published_elem.text or ""
        summary = summary_elem.text if summary_elem is not None else ""

        # Parse date: "2025-12-23T18:11:00Z"
        try:
            published = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
        except ValueError as e:
            print(f"Warning: Failed to parse date '{published_str}': {e}", file=sys.stderr)
            continue

        # Filter by date
        if published.replace(tzinfo=timezone.utc) < cutoff_date:
            continue

        items.append({
            'title': title,
            'link': link,
            'summary': summary,
            'published': published_str,
            'publishedISO': published.isoformat()
        })

    return items


def main():
    parser = argparse.ArgumentParser(
        description='Parse AWS Blog Atom feed',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to look back (default: 7)'
    )
    parser.add_argument(
        '--feed',
        type=str,
        default='/tmp/aws_blog_feed.xml',
        help='Path to the Atom feed XML file (default: /tmp/aws_blog_feed.xml)'
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
