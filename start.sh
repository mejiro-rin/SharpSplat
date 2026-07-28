#! /bin/bash
cd "$(dirname "$0")"
echo "Starting SharpSplat..."
./.venv/bin/python src/sharpsplat/app.py "$@"
