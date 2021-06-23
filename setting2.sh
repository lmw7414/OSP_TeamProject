#!/bin/bash

pip install requests
pip install flask
pip install bs4
pip install urllib3
pip install argparse
pip install nltk
pip install elasticsearch

pip install matplotlib
pip install pandas
pip install numpy

sudo apt-get install fonts-nanum*
sudo cp /usr/share/fonts/truetype/nanum/Nanum* ../.local/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/
rm -rf /home/ubuntu/.cache/matplotlib/*
./app.py

