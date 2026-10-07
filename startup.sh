#!/usr/bin/env bash
#
# startup.sh - Startup script for the Greeting App
#
# NOTE (for students): this script is shipped WITHOUT execute permission
# on purpose. If you try to run it directly (./startup.sh) and get a
# "permission denied" error, that is expected. We'll cover `chmod +x`
# next to fix it.
#
# This script does NOT install dependencies automatically. It only checks
# whether they're installed and tells you what to do.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS_FILE="${PROJECT_DIR}/requirements.txt"
APP_FILE="${PROJECT_DIR}/app.py"
LOG_DIR="${PROJECT_DIR}/logs"
ENV_DIR="${PROJECT_DIR}/env"
ENV_PYTHON="${ENV_DIR}/bin/python3"

echo "Project directory: ${PROJECT_DIR}"

mkdir -p "${LOG_DIR}"

# Deliberately check inside the local env/ virtualenv, NOT the global python3.
if [ ! -x "${ENV_PYTHON}" ]; then
    echo "ERROR: No virtual environment found at ${ENV_DIR}"
    echo "Create one first with:"
    echo "    python3 -m venv env"
    echo "    env/bin/pip install -r requirements.txt"
    exit 1
fi

echo "Checking dependencies (inside env/) from ${REQUIREMENTS_FILE} ..."

MISSING=0
while IFS= read -r line || [ -n "$line" ]; do
    # skip blank lines / comments
    [[ -z "$line" || "$line" == \#* ]] && continue

    PKG_NAME="$(echo "$line" | cut -d'=' -f1)"

    if ! "${ENV_PYTHON}" -c "import importlib.metadata as m; m.version('${PKG_NAME}')" >/dev/null 2>&1; then
        echo "  MISSING: ${line}"
        MISSING=1
    else
        echo "  OK: ${line}"
    fi
done < "${REQUIREMENTS_FILE}"

if [ "${MISSING}" -eq 1 ]; then
    echo ""
    echo "One or more dependencies are NOT installed in env/."
    echo "Install them with:"
    echo "    env/bin/pip install -r requirements.txt"
    echo ""
    echo "Then re-run this script."
    exit 1
fi

echo ""
echo "All dependencies are installed in env/. Starting the app..."
echo "Logs will be written to: ${LOG_DIR}/app.log"
echo ""

exec "${ENV_PYTHON}" "${APP_FILE}"
