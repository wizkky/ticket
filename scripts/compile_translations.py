"""Compile upstream gettext catalogs using the locked Babel dependency."""

from pathlib import Path

from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

root = Path(__file__).resolve().parents[1] / "apps/api/src/locale"
count = 0
for source in sorted(root.glob("*/LC_MESSAGES/*.po")):
    with source.open("rb") as stream:
        catalog = read_po(stream, locale=source.parent.parent.name)
    with source.with_suffix(".mo").open("wb") as stream:
        write_mo(stream, catalog, use_fuzzy=False)
    count += 1
print(f"Compiled {count} translation catalogs.")
