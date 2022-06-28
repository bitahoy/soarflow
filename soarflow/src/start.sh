#! /usr/bin/env bash

#Now let the app start
echo "Starting app..."

uvicorn app:app --proxy-headers --host 0.0.0.0 --port 80