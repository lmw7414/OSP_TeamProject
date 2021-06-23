#!/bin/bash

pip3 install requests
pip3 install flask
pip3 install bs4
pip3 install urllib3
pip3 install argparse
pip3 install nltk
pip3 install elasticsearch

pip3 install matplotlib
pip3 install pandas
pip3 install numpy

sudo apt-get install fonts-nanum*
sudo cp /usr/share/fonts/truetype/nanum/Nanum* ../.local/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
rm -rf /home/ubuntu/.cache/matplotlib/*
./app.py

