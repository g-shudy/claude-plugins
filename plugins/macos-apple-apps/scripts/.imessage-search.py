#!/usr/bin/env python3
"""iMessage search with attributedBody BLOB decoding support."""

import sqlite3
import os
import sys
import json
import biplist
import re
from datetime import datetime

def extract_text_streamtyped(blob):
    """Extract text from NSArchiver streamtyped format (primary method for iMessages).

    The attributedBody field uses Apple's NSArchiver 'streamtyped' format:
    - Starts with '\\x04\\x0bstreamtyped'
    - Contains NSAttributedString with embedded NSString
    - Text follows pattern: NSString\\x01\\x94\\x84\\x01<marker><length><text>\\x86\\x84
    """
    if not blob:
        return None

    try:
        # Primary pattern: NSString followed by control bytes, marker, and text
        match = re.search(rb'NSString\x01\x94\x84\x01.(.+?)\x86\x84', blob, re.DOTALL)
        if match:
            text_with_len = match.group(1)
            if len(text_with_len) > 1:
                text = text_with_len[1:].decode('utf-8', errors='ignore')
                text = re.sub(r'[\x00-\x1f]', '', text)
                if text.strip():
                    return text.strip()

        # Fallback pattern for different encodings
        match = re.search(rb'NSString.{1,10}?([^\x00\x01\x02\x03\x04\x05\x84\x85\x86\x92\x94\x96]{3,})', blob)
        if match:
            text = match.group(1).decode('utf-8', errors='ignore')
            text = re.sub(r'[\x00-\x1f]', '', text)
            if text.strip():
                return text.strip()
    except:
        pass

    return None


def extract_text_from_attributedBody(attributed_body_blob):
    """Extract plain text from attributedBody BLOB using multiple methods."""
    if not attributed_body_blob:
        return None

    # Method 1: streamtyped (primary for modern iMessages)
    text = extract_text_streamtyped(attributed_body_blob)
    if text:
        return text

    # Method 2: biplist fallback (older formats)
    try:
        plist_data = biplist.readPlistFromString(attributed_body_blob)

        if isinstance(plist_data, dict):
            for key in ['NSString', 'NS.string', '$objects']:
                if key in plist_data:
                    value = plist_data[key]
                    if isinstance(value, str):
                        return value
                    elif isinstance(value, list):
                        for obj in value:
                            if isinstance(obj, str) and len(obj) > 0 and obj != '$null':
                                return obj
        elif isinstance(plist_data, str):
            return plist_data
    except:
        pass

    # Method 3: generic regex fallback
    try:
        text = attributed_body_blob.decode('utf-8', errors='ignore')
        cleaned = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f\x80-\x9f]', '', text)
        words = re.findall(r'[a-zA-Z][a-zA-Z0-9\s\'".,!?\-:;@#$%&*()]{4,}', cleaned)
        if words:
            return max(words, key=len).strip()
    except:
        pass

    return None

def search_messages(keywords, limit=None):
    """Search messages for keywords and group by contact."""
    db_path = os.path.expanduser('~/Library/Messages/chat.db')

    if not os.path.exists(db_path):
        print(f"Error: Messages database not found at {db_path}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Use proper chat linkage - most messages (146K+) have handle_id = 0
    # and link through chat_message_join -> chat -> chat_identifier
    query = """
    SELECT
        m.ROWID,
        m.text,
        m.attributedBody,
        COALESCE(h.id, c.chat_identifier) as contact,
        datetime(m.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as date
    FROM message m
    LEFT JOIN handle h ON m.handle_id = h.ROWID AND m.handle_id > 0
    LEFT JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
    LEFT JOIN chat c ON cmj.chat_id = c.ROWID
    WHERE m.is_from_me = 1
      AND (h.id IS NOT NULL OR c.chat_identifier IS NOT NULL)
    ORDER BY m.date DESC
    """

    cursor.execute(query)

    contacts = {}

    for row in cursor:
        rowid, text, attributed_body, contact, date = row

        message_text = text
        if not message_text and attributed_body:
            message_text = extract_text_from_attributedBody(attributed_body)

        if not message_text:
            continue

        message_text_lower = message_text.lower()

        found_keywords = []
        for keyword in keywords:
            if keyword.lower() in message_text_lower:
                found_keywords.append(keyword)

        if found_keywords:
            if contact not in contacts:
                contacts[contact] = {
                    'count': 0,
                    'keywords': set(),
                    'last_date': None,
                    'messages': []
                }

            contacts[contact]['count'] += 1
            contacts[contact]['keywords'].update(found_keywords)
            if not contacts[contact]['last_date'] or date > contacts[contact]['last_date']:
                contacts[contact]['last_date'] = date

            if len(contacts[contact]['messages']) < 3:
                contacts[contact]['messages'].append({
                    'date': date,
                    'text': message_text[:100],
                    'keywords': found_keywords
                })

    conn.close()

    sorted_contacts = sorted(contacts.items(), key=lambda x: x[1]['count'], reverse=True)

    if limit:
        sorted_contacts = sorted_contacts[:limit]

    return sorted_contacts

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Advanced iMessage search', add_help=False)
    parser.add_argument('--felicitations', action='store_true')
    parser.add_argument('--pattern')
    parser.add_argument('--keywords')
    parser.add_argument('-o', '--output')
    parser.add_argument('-j', '--json', action='store_true')
    parser.add_argument('--csv', action='store_true')
    parser.add_argument('-l', '--limit', type=int)
    parser.add_argument('-h', '--help', action='store_true')

    args = parser.parse_args()

    if args.help:
        return

    if args.felicitations:
        keywords = [
            'happy birthday', 'merry christmas', 'happy new year',
            'congratulations', 'congrats', 'happy thanksgiving',
            'happy easter', 'happy holidays', 'seasons greetings',
            'best wishes', 'happy anniversary'
        ]
    elif args.pattern:
        keywords = [args.pattern]
    elif args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',')]
    else:
        print("Error: Must specify --felicitations, --pattern, or --keywords", file=sys.stderr)
        sys.exit(2)

    results = search_messages(keywords, args.limit)

    if not results:
        print("No matches found.")
        return

    output_lines = []

    if args.json:
        data = {
            'count': len(results),
            'contacts': [
                {
                    'contact': contact,
                    'message_count': data['count'],
                    'last_sent': data['last_date'],
                    'keywords': list(data['keywords'])
                }
                for contact, data in results
            ]
        }
        output_lines.append(json.dumps(data, indent=2))
    elif args.csv:
        output_lines.append('contact,count,last_sent,keywords')
        for contact, data in results:
            keywords_str = ';'.join(sorted(data['keywords']))
            output_lines.append(f'"{contact}",{data["count"]},"{data["last_date"]}","{keywords_str}"')
    else:
        output_lines.append(f"Found {len(results)} contacts:\n")
        output_lines.append(f"{'Contact':<40} {'Count':<8} {'Last Sent':<20} {'Keywords'}")
        output_lines.append("=" * 120)
        for contact, data in results:
            keywords_str = ', '.join(sorted(data['keywords']))[:40]
            output_lines.append(f"{contact:<40} {data['count']:<8} {data['last_date']:<20} {keywords_str}")

    output = '\n'.join(output_lines)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Results saved to: {args.output}")
    else:
        print(output)

if __name__ == '__main__':
    main()
