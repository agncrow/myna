#!/bin/bash
# Myna's site: the article (site/index.html) at the root and the Myna Book
# (docs/book, rendered by docs/book/site.co) under book/, published as the
# one commit of the public repository agncrow/myna-site, whose Pages serve
# it at https://agncrow.github.io/myna-site/. Myna's own repository stays
# private: only the rendered pages leave it.
#
#   scripts/publish_site.sh              render, assemble and push
#   scripts/publish_site.sh --dry-run    render and assemble only; prints where
set -euo pipefail
cd "$(dirname "$0")/.."
crow=${CROW:-crow}
remote=${MYNA_SITE_REMOTE:-git@github.com:agncrow/myna-site.git}

"$crow" test docs/book/site.co
"$crow" run -i docs/book/site.co

out=$(mktemp -d "${TMPDIR:-/tmp}/myna-site.XXXXXX")
cp site/index.html "$out/"
cp -R site/shots "$out/shots"
cp assets/myna.svg assets/favicon.ico assets/apple-touch-icon.png assets/myna-social.png "$out/"
cp -R docs/book/crow-site "$out/book"
touch "$out/.nojekyll"   # serve the files as they are

if [ "${1:-}" = "--dry-run" ]; then
    echo "assembled in $out"
    exit 0
fi

made=$(git rev-parse --short HEAD)
cd "$out"
git init -q -b main
git add -A
git -c user.name="$(git -C "$OLDPWD" config user.name)" -c user.email="$(git -C "$OLDPWD" config user.email)" \
    commit -q -m "Myna's site, from myna $made"
git push -q -f "$remote" main
cd - > /dev/null
rm -rf "$out"
echo "published from myna $made"
