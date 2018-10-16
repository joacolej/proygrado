#!/bin/sh
sudo systemctl start gunicorn.service
sudo systemctl stop gunicorn.service
sudo service nginx restart
