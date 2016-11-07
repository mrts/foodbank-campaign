PID=`ps auxww | grep django.fcgi | head -1 | awk '{ print $2; }'`
echo "Running 'kill -HUP $PID'"
kill -HUP $PID
