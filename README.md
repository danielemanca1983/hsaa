# HSAA website

Open dist/index.html in a browser. No installation or build step is required.

- dist/html/ — 17 complete, interlinked HTML pages
- dist/css/styles.css — shared styles; logo accent is --blue
- dist/js/main.js — accessible navigation and results email preparation
- dist/assets/ — supplied logo and selected HSAA photographs

Upload the contents of dist/ to a static web host, preserving its folders.
The root index.html is a full homepage with a base pointing into html/.

Pages can be edited directly. scripts/build-pages.py regenerates the HTML from its embedded copy and overwrites direct HTML edits; if using it, edit the copy in that script first. Run python scripts/check-site.py to check local links and node --check dist/js/main.js to check JavaScript syntax.

Content notes:
- The supplied introduction says 1881, but the centenary date and old website imply 1891. No association founding year is asserted.
- The requested name uses Athletics; the original crest says Athletic and is reproduced unchanged.
- Cross country, kwik cricket, tag rugby (labelled Tag touch per the requested sitemap) and orienteering are described as planned for 2026–27, as supplied.
- Detailed five-a-side rules, fixtures, future event dates and eligibility were not provided. Pages direct enquiries to info@hsaa.org.uk.
- Results forms open the visitor's email app. They do not send or store data themselves and require an email app to be configured.
- No social media login document or other source Office files are included in dist/.
- Additional archive topics outside the requested sitemap have not been made into separate pages.
