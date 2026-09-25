# HSAA website

Open `dist/index.html` in a browser. No installation is required to view the site.

- `dist/`: six complete HTML pages together: `index.html`, `about.html`, `contact.html`, `football.html`, `other-sports.html` and `information.html`.
- The main navigation links to the five main pages; the header Get in touch button opens the dedicated contact page. Sitemap subsections appear as normal content within their parent pages, including contact information under About us; there are no separate content-fragment pages or duplicate homepage.
- `dist/css/styles.css` and `dist/js/main.js`: shared styling, menus, ticker and email forms.
- `dist/assets/source/`: reviewed supplied photos and extracted logos.
- `dist/downloads/`: the reviewed blank alumni membership form.

Upload the contents of `dist/` to a static web host, preserving its folders. `hsaa-website.zip` contains those deployable files.

## Editing and rebuilding

- Edit `scripts/page_structure.py` for the page grouping and section links.
- Edit `scripts/navigation.py` for the shared navigation.
- Edit `content/pages/*.html` for the long-form public copy.
- Edit `content/people.json` for former players, association figures and partners.
- Edit `content/records.json` for the Lester Finch archive.
- Edit `scripts/additional-pages.py` for page assembly, results forms and other-sports summaries.
- Edit `scripts/build-pages.py` for the shared shell, homepage layout and ticker headlines.

Run `python scripts/build-pages.py` to regenerate the site. Direct edits to generated HTML will be overwritten. The fragments in `content/pages/` are build inputs only; every published page in `dist/` already contains its complete content. Normal builds need only Python’s standard library; the one-off Office/image extraction scripts are not required.

## Checks

Run `python scripts/check-site.py`, `python scripts/check-content.py`, `node --check dist/js/main.js`, and `node scripts/check-form-behavior.js`.

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
