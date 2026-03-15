# Contributing

Thanks for improving the Multilingual Programming Language landing site.

## Scope

This repository hosts the public GitHub Pages website for the project. Most changes here fall into one of these categories:

- Updating landing page copy in `index.html`
- Refreshing links to related repositories or live demos
- Improving visuals, layout, metadata, or accessibility
- Updating static assets such as logos, icons, and social preview images
- Improving repository documentation

## Repository layout

- `index.html`: main landing page, inline styles, and inline JavaScript
- `assets/images/`: logos, favicon source, and social preview assets
- `robots.txt`, `sitemap.xml`, `site.webmanifest`: site metadata files

## Development workflow

1. Create a branch for your change.
2. Make focused edits.
3. Preview the site locally in a browser.
4. Verify links, responsive layout, and basic accessibility.
5. Open a pull request with a concise summary.

## Local preview

You can use a lightweight static server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000/`.

## Content guidelines

- Keep language clear and concise.
- Prefer official project URLs under `multilingualprogramming.github.io` and `github.com/multilingualprogramming` when available.
- Preserve the current visual style unless the change is intentionally a design refresh.
- Keep external links opening safely with `target="_blank"` and `rel="noopener"` where appropriate.

## HTML, CSS, and JS guidance

- Favor small, localized edits over broad rewrites.
- Preserve semantic HTML and existing section structure where possible.
- Reuse existing utility classes and visual patterns before adding new ones.
- Keep JavaScript minimal and framework-free.
- Avoid introducing build tooling unless explicitly discussed first.

## Before submitting

Please check:

- The page loads without console errors in a browser
- New links are correct
- Mobile and desktop layouts still work
- Copy changes are free of obvious typos
- Any added assets are optimized and referenced correctly

## Pull request notes

A good pull request includes:

- A short description of what changed
- Screenshots for visible UI updates
- Notes about any follow-up work or open questions
