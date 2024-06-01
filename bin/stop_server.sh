#!/bin/bash
PID=$(lsof -t -i:80 -sTCP:LISTEN)
if [ -z "$PID" ]; then
    echo "No process is listening on port 80."
else
    echo "Killing process on port 80 with PID $PID."
    kill -9 $PID
    echo "Process killed."
fi