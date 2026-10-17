"""Copy the six complete editable HTML pages into the deployable site."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "content" / "pages"
DESTINATION = ROOT / "dist"
PAGES = ("index", "about", "contact", "football", "other-sports", "information")

for name in PAGES:
    source = SOURCE / f"{name}.html"
    published = DESTINATION / f"{name}.html"
    text = source.read_text(encoding="utf-8")
    if not text.lstrip().lower().startswith("<!doctype html>") or "</html>" not in text.lower():
        raise ValueError(f"Expected a complete HTML page: {source}")
    shutil.copyfile(source, published)

print(f"Copied {len(PAGES)} complete pages from content/pages/ to dist/.")
