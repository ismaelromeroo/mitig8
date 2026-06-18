import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

REPOS = [
    "fastapi/fastapi",
    "pydantic/pydantic",
]

FIELDS_TO_KEEP = ["tag_name", "published_at", "body", "html_url"]
OUTPUT_DIR = Path("data/raw")
PER_PAGE = 100


def _next_url(link_header: str) -> str | None:
    """Extract the rel="next" URL from a GitHub Link header, or None if absent."""
    for part in link_header.split(","):
        if 'rel="next"' in part:
            return part.split(";")[0].strip().strip("<>")
    return None


def fetch_releases(repo: str, token: str) -> list[dict]:
    """Fetch all stable releases for a repo, handling pagination.

    Skips drafts and pre-releases. Returns only the four fields we care about.
    Exits the process on rate-limit (403) since all repos share the same token.
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/repos/{repo}/releases"
    params = {"per_page": PER_PAGE}
    releases = []

    while url:
        response = requests.get(url, headers=headers, params=params, timeout=15)

        if response.status_code == 403:
            reset = response.headers.get("X-RateLimit-Reset", "unknown")
            print(f"Rate limit hit. Resets at epoch {reset}. Aborting.")
            sys.exit(1)

        response.raise_for_status()

        for release in response.json():
            if release["draft"] or release["prerelease"]:
                continue
            releases.append({field: release.get(field) for field in FIELDS_TO_KEEP})

        # params are baked into the next URL — don't send them again
        url = _next_url(response.headers.get("Link", ""))
        params = {}

    return releases


def save_releases(repo: str, releases: list[dict]) -> Path:
    """Write releases to data/raw/<slug>.json and return the path."""
    slug = repo.split("/")[1]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{slug}.json"
    path.write_text(json.dumps(releases, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def main() -> None:
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN not set. Add it to your .env file.")
        sys.exit(1)

    for repo in REPOS:
        print(f"Fetching {repo} ...", end=" ", flush=True)
        try:
            releases = fetch_releases(repo, token)
            path = save_releases(repo, releases)
            print(f"{len(releases)} releases -> {path}")
        except requests.RequestException as e:
            print(f"ERROR: {e}")
            continue

    print("Done.")


if __name__ == "__main__":
    main()
