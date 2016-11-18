PIDS=`ps auxww | grep '[t]est-osale/foodbank-campaign/conf/django-fcgi.py' | awk '{ print $2; }'`
for PID in $PIDS
do
	echo "Running 'kill -HUP $PID'"
	kill -HUP $PID
done
