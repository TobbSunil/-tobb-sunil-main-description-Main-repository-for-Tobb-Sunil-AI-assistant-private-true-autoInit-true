#!/usr/bin/env python3
"""Fetch the latest 20 Moltbook posts and produce a short summary.
The script:
1. Calls the Moltbook API with the stored bearer token.
2. Parses JSON, extracts title, author, upvotes for each post.
3. Prints a concise bullet‑list summary (max 10 posts).
"""
import os
import json
import urllib.request
import sys

API_TOKEN = os.getenv('MOLTBOOK_TOKEN') or 'moltbook_sk_KxVEcX5LBe2l4kDJdBC342NL7hUpEqaF'
API_URL = 'https://www.moltbook.com/api/v1/posts?limit=20'

def fetch_posts():
    req = urllib.request.Request(API_URL)
    req.add_header('Authorization', f'Bearer {API_TOKEN}')
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return data

def summarize(posts):
    lines = []
    for i, post in enumerate(posts[:10], 1):
        title = post.get('title', 'No title')
        author = post.get('author', 'unknown')
        upvotes = post.get('upvotes', 0)
        lines.append(f"{i}. {title} (by {author}) – {upvotes} upvotes")
    return '\n'.join(lines)

def main():
    try:
        posts = fetch_posts()
    except Exception as e:
        print(f"Error fetching Moltbook feed: {e}")
        sys.exit(1)
    summary = summarize(posts)
    print("Latest Moltbook posts (top 10):\n" + summary)

if __name__ == '__main__':
    main()
