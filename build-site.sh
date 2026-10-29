#!/usr/bin/env bash
# Gera o site estático em _site/ (usado pelo Cloudflare Pages).
set -euo pipefail
cd "$(dirname "$0")"

rm -rf _site
mkdir -p _site

cp index.html _site/
cp -r V1.0 V1.1 V1.2 V1.3 docs agentes assets _site/

for v in V2.0 V2.1 V2.2; do
  (cd "$v" && npm ci && npm run build)
  mkdir -p "_site/$v"
  cp -r "$v/dist/." "_site/$v/"
done
