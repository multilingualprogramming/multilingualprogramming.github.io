#!/usr/bin/env python
"""Validate linked multilingual projects and write a status snapshot."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def fetch_json(url: str, headers: dict[str, str]) -> tuple[int | None, dict | None, str | None]:
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = getattr(response, "status", response.getcode())
            body = response.read().decode("utf-8")
            return status, json.loads(body), None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = None
        return exc.code, data, str(exc)
    except Exception as exc:  # pragma: no cover - defensive for GitHub Actions runtime
        return None, None, str(exc)


def fetch_url(url: str, headers: dict[str, str]) -> tuple[int | None, str | None]:
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = getattr(response, "status", response.getcode())
            return status, None
    except urllib.error.HTTPError as exc:
        return exc.code, str(exc)
    except Exception as exc:  # pragma: no cover - defensive for GitHub Actions runtime
        return None, str(exc)


def repo_api_url(repo_url: str) -> str | None:
    parsed = urllib.parse.urlparse(repo_url)
    if parsed.netloc != "github.com":
      return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1]
    return f"https://api.github.com/repos/{owner}/{repo}"


def collect_project_status(project: dict, headers: dict[str, str]) -> dict:
    result = {
        "id": project["id"],
        "name": project["name"],
        "category": project["category"],
        "language": project.get("language", ""),
        "site_url": project.get("site_url"),
        "repo_url": project.get("repo_url"),
        "alternate_repo_urls": project.get("alternate_repo_urls", []),
        "site_status": None,
        "repo_status": None,
        "repo_default_branch": None,
        "repo_pushed_at": None,
        "repo_updated_at": None,
        "repo_open_issues": None,
        "alerts": []
    }

    site_url = project.get("site_url")
    if site_url:
        site_status, site_error = fetch_url(site_url, headers)
        result["site_status"] = site_status
        if site_status != 200:
            detail = site_error or "Site did not return HTTP 200"
            result["alerts"].append(f"Site check failed for {site_url}: {detail}")

    repo_url = project.get("repo_url")
    api_url = repo_api_url(repo_url) if repo_url else None
    if api_url:
        repo_status, payload, repo_error = fetch_json(api_url, headers)
        result["repo_status"] = repo_status
        if repo_status == 200 and payload:
            result["repo_default_branch"] = payload.get("default_branch")
            result["repo_pushed_at"] = payload.get("pushed_at")
            result["repo_updated_at"] = payload.get("updated_at")
            result["repo_open_issues"] = payload.get("open_issues_count")
        else:
            detail = repo_error or "Repository metadata could not be fetched"
            result["alerts"].append(f"Repo check failed for {repo_url}: {detail}")

    return result


def compare_snapshots(previous: dict | None, current: dict) -> list[str]:
    if not previous:
        return ["No previous snapshot found. Created initial monitoring snapshot."]

    previous_projects = {item["id"]: item for item in previous.get("projects", [])}
    changes: list[str] = []
    for item in current.get("projects", []):
        earlier = previous_projects.get(item["id"])
        if not earlier:
            changes.append(f"New project added to registry: {item['name']}")
            continue

        for field in ("site_status", "repo_status", "repo_default_branch", "repo_pushed_at", "repo_updated_at"):
            if earlier.get(field) != item.get(field):
                changes.append(
                    f"{item['name']} changed {field}: {earlier.get(field)} -> {item.get(field)}"
                )
    return changes


def build_markdown(snapshot: dict) -> str:
    lines = [
        "# Project Watch Status",
        "",
        f"- Generated at: `{snapshot['generated_at']}`",
        f"- Projects monitored: `{len(snapshot['projects'])}`",
        f"- Alert count: `{snapshot['alert_count']}`",
        ""
    ]

    if snapshot["changes"]:
        lines.extend(["## Notable changes", ""])
        for change in snapshot["changes"]:
            lines.append(f"- {change}")
        lines.append("")

    lines.extend(
        [
            "## Snapshot",
            "",
            "| Project | Category | Language | Site | Repo | Last push | Alerts |",
            "| --- | --- | --- | --- | --- | --- | --- |"
        ]
    )

    for item in snapshot["projects"]:
        site = str(item["site_status"]) if item["site_status"] is not None else "n/a"
        repo = str(item["repo_status"]) if item["repo_status"] is not None else "n/a"
        pushed = item["repo_pushed_at"] or "n/a"
        alerts = "; ".join(item["alerts"]) if item["alerts"] else "none"
        lines.append(
            f"| {item['name']} | {item['category']} | {item['language']} | {site} | {repo} | {pushed} | {alerts} |"
        )

    alert_items = [alert for item in snapshot["projects"] for alert in item["alerts"]]
    lines.append("")
    lines.append("## Alerts")
    lines.append("")
    if alert_items:
        for alert in alert_items:
            lines.append(f"- {alert}")
    else:
        lines.append("- No active alerts in this snapshot.")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check project links and GitHub repository metadata.")
    parser.add_argument("--registry", required=True, help="Path to the project registry JSON file.")
    parser.add_argument("--status-json", required=True, help="Path to write the status JSON snapshot.")
    parser.add_argument("--status-md", required=True, help="Path to write the status markdown report.")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "multilingualproject-watch"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    registry_path = Path(args.registry)
    status_json_path = Path(args.status_json)
    status_md_path = Path(args.status_md)

    registry = load_json(registry_path)
    previous_snapshot = load_json(status_json_path) if status_json_path.exists() else None

    projects = [collect_project_status(project, headers) for project in registry.get("projects", [])]
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    changes = compare_snapshots(previous_snapshot, {"projects": projects})
    alert_count = sum(len(item["alerts"]) for item in projects)

    snapshot = {
        "generated_at": generated_at,
        "alert_count": alert_count,
        "changes": changes,
        "projects": projects
    }

    save_json(status_json_path, snapshot)
    save_text(status_md_path, build_markdown(snapshot))

    return 1 if alert_count else 0


if __name__ == "__main__":
    sys.exit(main())
