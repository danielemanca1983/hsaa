# HSAA website

Open `dist/index.html` in a browser. No installation is required to view the site.

- `dist/`: six complete HTML pages together: `index.html`, `about.html`, `contact.html`, `football.html`, `other-sports.html` and `information.html`.
- The main navigation links to the five main pages; the header Get in touch button opens the dedicated contact page. Sitemap subsections appear within their parent pages, including contact information under About us.
- `dist/css/styles.css` and `dist/js/main.js`: shared styling, menus, ticker and email forms.
- `dist/assets/source/`: reviewed supplied photos and extracted logos.
- `dist/downloads/`: the reviewed blank alumni membership form and six October 2026 PDFs covering the committee, school competitions, cross country and district trophy draws.

Upload the contents of `dist/` to a static web host, preserving its folders. `hsaa-website.zip` contains those deployable files.

## Editing and rebuilding

Edit the complete page in `content/pages/`:

| Source file | Content |
| --- | --- |
| `index.html` | Home, welcome, ticker and mission |
| `about.html` | Mission, history, committee and contact details |
| `contact.html` | Contact details and social links |
| `football.html` | Schools football, five a sides, nine a side, district teams and results form |
| `other-sports.html` | Cross country, other sports and Young & Active |
| `information.html` | Contacts and supporters, former players, association figures, foundation, district competitions and results form |

Each source file contains its full HTML document, including navigation and footer. Edit `dist/css/styles.css` for shared styling and `dist/js/main.js` for interactions. Run `python scripts/build-pages.py` to copy the six source pages to `dist/`; direct edits to the six HTML files in `dist/` will be overwritten. Normal builds need only Python’s standard library.

## Checks

Run `python scripts/check-site.py`, `python scripts/check-content.py`, `node --check dist/js/main.js`, and `node scripts/check-form-behavior.js`.

The October 2026 source files and instructions are in `Final Updates Oct 2026/`. The published copies of the PDFs and logos are in `dist/downloads/` and `dist/assets/source/`. Rebuild HTML from `content/pages/`, then refresh the deployment archives after content changes.

## Content status

Read [CONTENT-REPORT.md](CONTENT-REPORT.md) for missing information, conflicting historical details and editorial decisions. The file-by-file inventory is [source-content-map.md](source-content-map.md).

The Contact page includes the supplied Facebook page name and Instagram, X and TikTok handles. Forms prepare emails and do not send or store submissions themselves. Future events are labelled as planned when dates have not been supplied. No login-information document is published.

## Live preview

The site is published on GitHub Pages at https://danielemanca1983.github.io/hsaa/.
GitHub Pages serves the root of the `gh-pages` branch, containing only `dist/`.

After committing updated site files on `master`, publish them with:

```sh
git subtree split --prefix dist -b pages-update
git push origin pages-update:gh-pages
git branch -D pages-update
```

GitHub Pages rebuilds automatically when the publishing branch is updated.
