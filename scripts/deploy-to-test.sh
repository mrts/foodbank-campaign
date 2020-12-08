#!/bin/bash

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR

# export TOIDUPANK_SSH_HOST=user@example.org:22
winpty fab -H $TOIDUPANK_SSH_HOST deploy
