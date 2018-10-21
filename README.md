# CMBot

sudo apt install -y python3 python-pip3 libffi-dev libtiff-dev libssl-dev youtube-dl atomicparsley

sudo pip3 install -U python-telegram-bot

sudo adduser cmbot

sudo passwd -d cmbot

sudo -u cmbot -s

git clone https://github.com/williamflow/CMBot.git /home/cmbot/CMBot

cd /home/cmbot/CMBot

echo TOKEN=\"token\" > private.py

exit

sudo mv cmbot.service /etc/systemd/system/

sudo systemctl enable cmbot

sudo systemctl start cmbot
