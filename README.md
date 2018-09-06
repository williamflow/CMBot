# CMBot

sudo apt install -y python python-pip libjpeg-dev libffi-dev libtiff-dev libssl-dev firefox-esr xvfb
sudo pip install -U python-telegram-bot selenium pillow pyvirtualdisplay
Install geckodriver (https://github.com/mozilla/geckodriver/releases)
sudo adduser cmbot
sudo passwd -d cmbot
sudo -u cmbot -s
git clone https://github.com/williamflow/CMBot.git /home/cmbot/CMBot
cd /home/cmbot/CMBot
echo TOKEN=\"token\" > private.py
./bot.py
Press enter to stop
exit
sudo mv cmbot.service /etc/systemd/system/
sudo systemctl enable cmbot
sudo systemctl start cmbot
