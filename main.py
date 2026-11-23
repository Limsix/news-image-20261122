"""Entrypoint for the news-image-20261122 make.fun entry.

Writes a single 1024x1024 newspaper front page to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Deterministic: fixed seed, no timestamps, no network, no system paths.
"""

import os
import sys
from pathlib import Path

# python3 -P -s does not put the script directory on sys.path, so add it
# explicitly before importing the local draw module.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from draw import render_front_page


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    image = render_front_page()
    image.save(out_dir / "entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
