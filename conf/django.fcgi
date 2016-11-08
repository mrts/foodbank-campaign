#!/usr/local/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HTDOCS_PROJ_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_NAME="$(basename "$HTDOCS_PROJ_DIR")"
PROJ_DIR="$(cd "$HTDOCS_PROJ_DIR/../../django-projects/$ENV_NAME/foodbank-campaign" && pwd)"

$PROJ_DIR/venv/bin/python $PROJ_DIR/conf/django-fcgi.py
~
