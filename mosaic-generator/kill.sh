pids=$(pgrep -f "flask run")

if [ -z "$pids" ]; then
    echo "No Flask apps are running."
else
    echo "Terminating Flask apps..."
    kill $pids
    echo "All Flask apps terminated."
fi