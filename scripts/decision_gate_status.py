#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sync_decision_gate_issue import extract_decision_line


def fetch_issue(repo: str, issue_number: int) -> dict[str, object]:
    output = subprocess.check_output(
        [
            "gh",
            "issue",
            "view",
            str(issue_number),
            "--repo",
            repo,
            "--json",
            "title,url,comments",
        ],
        text=True,
    )
    payload = json.loads(output)
    return payload if isinstance(payload, dict) else {}


def summarize_comments(comments: list[dict[str, object]]) -> dict[str, object]:
    decision_comments = []
    for comment in comments:
        body = str(comment.get("body", ""))
        decision_line = extract_decision_line(body)
        if not decision_line:
            continue
        author = "unknown"
        author_data = comment.get("author")
        if isinstance(author_data, dict):
            author = str(author_data.get("login") or author)
        decision_comments.append(
            {
                "author": author,
                "decision": decision_line.removeprefix("Decision: ").lower(),
                "created_at": str(comment.get("createdAt", "")),
            }
        )
    return {
        "comment_count": len(comments),
        "decision_comment_count": len(decision_comments),
        "decision_comments": decision_comments,
    }


def load_final_decision(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"decision": "pending", "total_votes": 0}
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Show the current operational status of the benchmark decision gate.")
    parser.add_argument("--repo", default="TakoVHS/CogniPrint")
    parser.add_argument("--issue", type=int, default=16)
    parser.add_argument("--decision-file", type=Path, default=Path("docs/decisions/final-decision.json"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    issue_payload = fetch_issue(args.repo, args.issue)
    comments = issue_payload.get("comments", [])
    if not isinstance(comments, list):
        comments = []
    comment_summary = summarize_comments(comments)
    decision_payload = load_final_decision(root / args.decision_file)
    payload = {
        "issue_title": issue_payload.get("title"),
        "issue_url": issue_payload.get("url"),
        "comment_count": comment_summary["comment_count"],
        "decision_comment_count": comment_summary["decision_comment_count"],
        "decision_comments": comment_summary["decision_comments"],
        "current_decision_file": decision_payload,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Issue: {payload['issue_url']}")
        print(f"Comments: {payload['comment_count']}")
        print(f"Decision-bearing comments: {payload['decision_comment_count']}")
        print(f"Current decision file: {decision_payload.get('decision')} (votes={decision_payload.get('total_votes')})")
        if payload["decision_comments"]:
            print("Decision comments:")
            for entry in payload["decision_comments"]:
                print(f"- {entry['author']}: {entry['decision']} ({entry['created_at']})")
        else:
            print("Decision comments: none yet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
