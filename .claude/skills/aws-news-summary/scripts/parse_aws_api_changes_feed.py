#!/usr/bin/env python3
"""
AWS API Changes RSS Feed Parser

Usage:
    python3 parse_aws_api_changes_feed.py [--days DAYS] [--details]

Arguments:
    --days DAYS     Number of days to look back (default: 7)
    --feed PATH     Path to the RSS feed XML file
    --details       Fetch detailed API method information from each page
    --service NAME  Filter by service name (partial match)

Output:
    JSON array of items to stdout
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path


class APIChangesHTMLParser(HTMLParser):
    """Parse AWS API Changes detail page to extract method information."""

    def __init__(self):
        super().__init__()
        self.methods = []
        self.current_method = None
        self.in_details = False
        self.in_summary = False
        self.in_pre = False
        self.capture_text = False
        self.current_text = ""
        self.current_change_type = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "details":
            self.in_details = True
            method_id = attrs_dict.get("id", "")
            if method_id:
                self.current_method = {
                    "name": method_id,
                    "type": "",  # new, updated, removed
                    "changes": [],
                    "request_changes": None,
                    "response_changes": None
                }

        elif tag == "summary" and self.in_details:
            self.in_summary = True
            self.capture_text = True
            self.current_text = ""

        elif tag == "span" and self.in_summary:
            class_name = attrs_dict.get("class", "")
            if "has-text-info" in class_name:
                self.capture_text = True
                self.current_text = ""

        elif tag == "em" and self.in_details:
            class_name = attrs_dict.get("class", "")
            if "is-danger" in class_name or "is-success" in class_name:
                self.capture_text = True
                self.current_text = ""

        elif tag == "pre" and self.in_details:
            self.in_pre = True
            self.capture_text = True
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag == "details":
            if self.current_method and self.current_method["name"]:
                self.methods.append(self.current_method)
            self.current_method = None
            self.in_details = False

        elif tag == "summary":
            self.in_summary = False
            self.capture_text = False
            # Extract method type from summary text
            if self.current_method and self.current_text:
                text = self.current_text.strip()
                if "(new)" in text.lower():
                    self.current_method["type"] = "new"
                elif "(updated)" in text.lower():
                    self.current_method["type"] = "updated"
                elif "(removed)" in text.lower():
                    self.current_method["type"] = "removed"

        elif tag == "span" and self.in_summary:
            self.capture_text = False

        elif tag == "em" and self.in_details:
            if self.current_text:
                self.current_change_type = self.current_text.strip().lower()
            self.capture_text = False

        elif tag == "pre" and self.in_details:
            self.in_pre = False
            if self.current_method and self.current_text:
                pre_content = self.current_text.strip()
                if pre_content:
                    if "request" in self.current_change_type:
                        self.current_method["request_changes"] = pre_content
                    elif "response" in self.current_change_type:
                        self.current_method["response_changes"] = pre_content
                    else:
                        self.current_method["changes"].append(pre_content)
            self.capture_text = False
            self.current_text = ""

    def handle_data(self, data):
        if self.capture_text:
            self.current_text += data


def fetch_api_details(url: str, retry_count: int = 2) -> dict:
    """Fetch detailed API method information from the detail page.

    Args:
        url: URL of the API changes detail page
        retry_count: Number of retries on failure

    Returns:
        Dictionary with methods list
    """
    for attempt in range(retry_count + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; AWSAPIChangesParser/1.0)'
                }
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                html_content = response.read().decode('utf-8')

            parser = APIChangesHTMLParser()
            parser.feed(html_content)

            return {
                "methods": parser.methods,
                "method_count": len(parser.methods)
            }

        except Exception as e:
            if attempt < retry_count:
                time.sleep(1)
                continue
            print(f"Warning: Failed to fetch details from {url}: {e}", file=sys.stderr)
            return {"methods": [], "method_count": 0, "error": str(e)}

    return {"methods": [], "method_count": 0}


def parse_feed(feed_path: str, days: int = 7, fetch_details: bool = False,
               service_filter: str = None) -> list[dict]:
    """Parse AWS API Changes RSS feed and filter by date.

    Args:
        feed_path: Path to the RSS feed XML file
        days: Number of days to look back
        fetch_details: Whether to fetch detailed API method information
        service_filter: Filter by service name (partial match, case-insensitive)

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
        desc_elem = item.find('description')
        pubdate_elem = item.find('pubDate')

        if title_elem is None or link_elem is None or pubdate_elem is None:
            continue

        title = title_elem.text or ""
        link = link_elem.text or ""
        description = desc_elem.text if desc_elem is not None else ""
        pubdate_str = pubdate_elem.text or ""

        # Parse date: "Mon, 05 Jan 2026 19:07:09 +0000"
        try:
            pubdate = datetime.strptime(pubdate_str, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError as e:
            print(f"Warning: Failed to parse date '{pubdate_str}': {e}", file=sys.stderr)
            continue

        # Filter by date
        if pubdate.replace(tzinfo=timezone.utc) < cutoff_date:
            continue

        # Extract service name from title (e.g., "AWS Clean Rooms ML - 4 updated methods")
        service_name = ""
        if " - " in title:
            service_name = title.split(" - ")[0].strip()

        # Filter by service name if specified
        if service_filter:
            if service_filter.lower() not in service_name.lower():
                continue

        # Parse method counts from title
        new_count = 0
        updated_count = 0
        removed_count = 0

        # Match patterns like "4 new 2 updated methods" or "3 updated methods"
        new_match = re.search(r'(\d+)\s+new', title, re.IGNORECASE)
        updated_match = re.search(r'(\d+)\s+updated', title, re.IGNORECASE)
        removed_match = re.search(r'(\d+)\s+removed', title, re.IGNORECASE)

        if new_match:
            new_count = int(new_match.group(1))
        if updated_match:
            updated_count = int(updated_match.group(1))
        if removed_match:
            removed_count = int(removed_match.group(1))

        item_data = {
            'title': title,
            'link': link,
            'description': description,
            'pubDate': pubdate_str,
            'pubDateISO': pubdate.isoformat(),
            'service': service_name,
            'newMethods': new_count,
            'updatedMethods': updated_count,
            'removedMethods': removed_count
        }

        # Fetch detailed API method information if requested
        if fetch_details:
            print(f"Fetching details for {service_name}...", file=sys.stderr)
            details = fetch_api_details(link)
            item_data['details'] = details
            # Rate limiting to avoid overwhelming the server
            time.sleep(0.5)

        items.append(item_data)

    return items


def main():
    parser = argparse.ArgumentParser(
        description='Parse AWS API Changes RSS feed',
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
        default='/tmp/aws_api_changes_feed.xml',
        help='Path to the RSS feed XML file (default: /tmp/aws_api_changes_feed.xml)'
    )
    parser.add_argument(
        '--details',
        action='store_true',
        help='Fetch detailed API method information from each page'
    )
    parser.add_argument(
        '--service',
        type=str,
        default=None,
        help='Filter by service name (partial match, case-insensitive)'
    )

    args = parser.parse_args()

    feed_path = Path(args.feed)
    if not feed_path.exists():
        print(f"Error: Feed file not found: {feed_path}", file=sys.stderr)
        sys.exit(1)

    items = parse_feed(
        str(feed_path),
        days=args.days,
        fetch_details=args.details,
        service_filter=args.service
    )

    # Output as JSON
    print(json.dumps(items, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
