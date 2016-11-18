#!/usr/bin/env bash

set -e
set -u

cd "$( dirname "${BASH_SOURCE[0]}" )/.."

cp src/db.sqlite3 ../backups/`date '+%Y-%m-%d-%H.%M.%S'`-db.sqlite3
git pull

set +u
. venv/bin/activate
set -u

pip install --requirement=src/requirements.txt

python src/manage.py migrate
python src/manage.py collectstatic --noinput

PIDS=`ps auxww | grep '[l]ive-osale/foodbank-campaign/conf/django-fcgi.py' |  awk '{ print $2; }'`
for PID in $PIDS
do
	echo "Running 'kill -HUP $PID'"
	kill -HUP $PID
done
