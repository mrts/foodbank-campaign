PID=`ps auxww | grep test-osale/foodbank-campaign/conf/django-fcgi.py | head -1 | awk '{ print $2; }'`
echo "Running 'kill -HUP $PID'"
kill -HUP $PID
