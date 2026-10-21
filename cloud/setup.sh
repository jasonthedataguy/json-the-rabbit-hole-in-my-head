#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r cloud/requirements.txt
npm ci --ignore-scripts --no-audit --no-fund --prefix studio/apps/video
python cloud/bootstrap.py --download
(
  cd studio/apps/video
  node node_modules/@remotion/cli/remotion-cli.js browser ensure
)
npm run typecheck --prefix studio/apps/video
