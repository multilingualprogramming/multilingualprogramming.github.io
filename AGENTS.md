# AGENTS.md

Guidance for coding agents working in this repository.

## Purpose

This repository contains the static GitHub Pages landing site for the Multilingual Programming Language project.

## Key files

- `index.html`: primary page, including markup, inline CSS, and inline JavaScript
- `projects.json`: canonical registry for tracked multilingual projects and linked pages
- `scripts/check_projects.py`: dependency-free monitoring script used by GitHub Actions
- `monitoring/`: generated status snapshots for ecosystem tracking
- `assets/images/`: image assets used by the landing page
- `README.md`: repository overview and related links
- `CONTRIBUTING.md`: contributor workflow and expectations
- `robots.txt`, `sitemap.xml`, `site.webmanifest`: static site metadata

## Working style

- Make focused edits that match the existing structure.
- Prefer updating the single-page site in place rather than introducing new tooling.
- Keep the site static unless the task explicitly requires a different approach.
- Preserve current external links unless the task is to replace or refresh them.
- Use ASCII by default when editing Markdown or code.

## Editing expectations

- Use `apply_patch` for direct file edits.
- Do not add frameworks, package managers, or build steps without explicit user approval.
- Reuse existing CSS classes and section patterns where practical.
- Keep JavaScript small and dependency-free.
- If you add a new section to `index.html`, make sure the copy is consistent with the rest of the page.
- If you change tracked external links, update `projects.json` too.

## Validation

After edits, do a lightweight verification pass:

- Confirm the intended text or links exist
- Check for obvious HTML structure issues
- If possible, validate any changed URLs and references locally

## Common tasks

- Add or update links to docs, playgrounds, and project repositories
- Update the project registry and monitoring coverage
- Refresh landing page copy
- Improve metadata or assets for GitHub Pages
- Expand repository documentation

## Avoid

- Large rewrites unrelated to the user request
- Destructive git operations
- Introducing unnecessary complexity into a static site repository
