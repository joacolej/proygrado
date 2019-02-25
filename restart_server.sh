#!/bin/sh
sudo systemctl stop gunicorn.service
sudo systemctl start gunicorn.service
sudo service nginx restart
