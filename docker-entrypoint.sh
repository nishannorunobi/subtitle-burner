#!/bin/bash
source /workspace/git-ignore-files/osenv.sh 2>/dev/null || true
exec "${@:-bash}"
