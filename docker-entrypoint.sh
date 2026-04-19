#!/bin/bash
source /workspace/git-ignore-files/osenv.sh 2>/dev/null || true
git config --global --add safe.directory /workspace
exec "${@:-bash}"
