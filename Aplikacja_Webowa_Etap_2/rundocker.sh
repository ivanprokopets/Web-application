#!/bin/bash
sudo docker build -t aplikacja .
sudo docker run --rm -p 8080:80 aplikacja
echo "Prosze wejdz na http://localhost/"
