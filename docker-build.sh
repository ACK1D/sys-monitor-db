#!/bin/bash

if ! command -v docker &> /dev/null; then
    echo "Docker не установлен"
    exit 1
fi

mkdir -p dist
sudo chmod 777 dist

docker build -t system-monitor-builder .
docker run --rm -v "$(pwd)/dist:/output" system-monitor-builder

docker rmi system-monitor-builder

sudo chmod 755 dist
echo "Build is complete. The archive is located in dist/system-monitor.tar.gz" 