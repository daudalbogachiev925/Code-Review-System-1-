import requests
import os
from src.analyzer import analyze_directory
from src.metrics import analyze_project
from src.report import to_markdown

GITHUB_API = "https://api.github.com"

def post_pr_comment(repo, pr_number, body, token=None):
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN required")
    url = f"{GITHUB_API}/repos/{repo}/issues/{pr_number}/comments"
    r = requests.post(url, json={"body": body},
                      headers={"Authorization": f"token {token}",
                               "Accept": "application/vnd.github+json"})
    r.raise_for_status()
    return r.json()

def review_pr(repo, pr_number, src_path="src"):
    issues = analyze_directory(src_path)
    metrics = analyze_project(src_path)
    md = to_markdown(issues, metrics)
    post_pr_comment(repo, pr_number, md)
    return {"issues": len(issues), "posted": True}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python -m src.bot <repo> <pr_number>")
        sys.exit(1)
    review_pr(sys.argv[1], sys.argv[2])
