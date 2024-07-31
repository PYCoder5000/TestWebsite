#!/bin/bash
sudo yum update -y
sudo yum install python pip -y
sudo pip install flask
sudo pip install boto3
sudo pip install werkzeug
sudo pip install itsdangerous