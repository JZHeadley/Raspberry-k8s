while true
do
    curl -w "%{time_total}\n" -so /dev/null  http://localhost:8080
    #date
    sleep 1
done
