while true
do
    curl -w "%{time_total}\n" -so /dev/null  http://localhost:9090
    #date
    sleep 20
done
