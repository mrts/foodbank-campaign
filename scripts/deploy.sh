#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR
winpty fab -u azureuser -H kassisilm.cloudapp.net deploy
