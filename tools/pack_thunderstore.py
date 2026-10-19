"""Build the Thunderstore package (team raccoondotwtf) from a release zip's DLL.

    python tools/pack_thunderstore.py 1.2.0

Reads BigOrb-<version>.zip (the GitHub release asset), writes dist/raccoondotwtf-BigOrb-<version>.zip with
manifest.json, icon.png, README.md (image links made absolute so they show on Thunderstore) and BigOrb.dll.
The same zip goes to cdn.raccoon.wtf/mods/bigorb/ for direct downloads.
"""
import json, re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_RAW = 'https://raw.githubusercontent.com/ellietheraccoon/bigorb/main/'

version = sys.argv[1] if len(sys.argv) > 1 else '1.2.0'
release = ROOT / f'BigOrb-{version}.zip'
with zipfile.ZipFile(release) as z:
    dll_name = next(n for n in z.namelist() if n.replace(chr(92), '/').endswith('BigOrb.dll'))
    dll = z.read(dll_name)

manifest = {
    'name': 'BigOrb',
    'version_number': version,
    'website_url': 'https://github.com/ellietheraccoon/bigorb',
    'description': 'Host-side moderation dashboard for Big Walk: kick, ban and shared ban lists, modded-client detection, puzzle and item resets, chat and sign logs.',
    'dependencies': ['BepInEx-BepInExPack_IL2CPP-6.0.755'],
}
assert len(manifest['description']) <= 250, 'Thunderstore descriptions max out at 250 characters'

readme = (ROOT / 'README.md').read_text(encoding='utf-8')
# relative image/link targets -> absolute GitHub raw URLs (Thunderstore has no repo files)
readme = re.sub(r'\]\((?!https?://|#|mailto:)([^)]+)\)', lambda m: f']({REPO_RAW}{m.group(1)})', readme)

out = ROOT / 'dist' / f'raccoondotwtf-BigOrb-{version}.zip'
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('manifest.json', json.dumps(manifest, indent=2))
    z.write(ROOT / 'icon.png', 'icon.png')
    z.writestr('README.md', readme)
    z.writestr('BigOrb.dll', dll)
print(out)
