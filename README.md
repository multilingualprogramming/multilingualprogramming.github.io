# multilingualprogramming.github.io

This repository contains the GitHub Pages landing site for the Multilingual Programming Language project.

The site is a static single-page experience built around [`index.html`](./index.html) and a small set of assets in [`assets/images/`](./assets/images/). It highlights the language, links to documentation and the playground, and showcases related projects.

This repository also acts as the central landing-page registry for linked multilingual projects and includes a scheduled monitoring workflow to help track repo and site changes across the ecosystem.

## Live site

- Main site: [multilingualprogramming.github.io](https://multilingualprogramming.github.io/)
- Documentation: [multilingualprogramming.github.io/docs/](https://multilingualprogramming.github.io/docs/)
- Playground: [multilingualprogramming.github.io/playground/](https://multilingualprogramming.github.io/playground/)

## Related repositories

- Core language project: [github.com/multilingualprogramming/multilingual](https://github.com/multilingualprogramming/multilingual)
- Original repository: [github.com/johnsamuelwrites/multilingual](https://github.com/johnsamuelwrites/multilingual)
- Documentation repository: [github.com/multilingualprogramming/docs](https://github.com/multilingualprogramming/docs)
- Playground repository: [github.com/multilingualprogramming/playground](https://github.com/multilingualprogramming/playground)

## French-language example projects

- Fractales: [site](https://multilingualprogramming.github.io/fractales/) | [repository](https://github.com/multilingualprogramming/fractales)
- Cellular automata (`cellcosmos`): [site](https://multilingualprogramming.github.io/cellcosmos/) | [repository](https://github.com/multilingualprogramming/cellcosmos)

## Repository structure

```text
.
|-- .github/
|   `-- workflows/
|-- monitoring/
|-- scripts/
|-- projects.json
|-- index.html
|-- assets/
|   `-- images/
|-- favicon.ico
|-- apple-touch-icon.png
|-- robots.txt
|-- sitemap.xml
`-- site.webmanifest
```

## Project registry

The file [`projects.json`](./projects.json) is the central registry for the projects this landing page points to. Each entry includes the primary repository, live site URL, category, language, status, and review date.

When you add or update a project link on the landing page, update the registry too so monitoring stays in sync.

## Monitoring

This repository now includes a scheduled GitHub Actions workflow at [`.github/workflows/project-watch.yml`](./.github/workflows/project-watch.yml).

It is designed to:

- Check linked GitHub Pages URLs for basic availability
- Fetch GitHub repository metadata for the tracked projects
- Record a snapshot in [`monitoring/project-status.json`](./monitoring/project-status.json)
- Publish a readable report in [`monitoring/project-status.md`](./monitoring/project-status.md)
- Open an issue when alerts or snapshot changes are detected

The checker itself lives in [`scripts/check_projects.py`](./scripts/check_projects.py).

## Status snapshot

The latest committed monitoring report is available at [`monitoring/project-status.md`](./monitoring/project-status.md).

After the first GitHub Actions run, this file will show the latest observed status for the landing page, docs, playground, and showcase projects.

## Local preview

Because this is a static site, you can preview it with any simple local HTTP server.

### Python

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/`.

## Contributing

Contributions are welcome. For site-specific workflow and expectations, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

The repository is distributed under the terms described in [LICENSE](./LICENSE).
