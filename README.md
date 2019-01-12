Installation Instructions:

1) qbittorrent:

sudo apt install qbittorrent
run qbittorrent
Herramientas -> opciones -> Interfaz web  Habilitar interfaz web checked, Eludir la autenticacion para localhost checked.
Herramientas -> opciones -> Bittorrent  Maximo de subidas activas = 0

sudo vim  ~/.config/lxsession/LXDE-pi/autostart add at the end the following line:
@qbittorrent



2) Lazy app
sudo apt-get install libzbar-dev libzbar0 libxml2-dev libxslt-dev redis-server supervisor
sudo pip3 install virtualenv
mkdir app
cd app
git clone https://github.com/federulli/lazy_app.git
virtualenv -p /usr/bin/python3 lazy_app_venv
lazy_app_venv/bin/pip install -r lazy_app/requirements
lazy_app_venv/bin/python3 lazy_app/manage.py migrate
sudo cp lazy_app/lazy_app.conf /etc/supervisor/conf.d/
sudo mkdir /var/log/lazy_app
sudo touch /var/log/lazy_app/celery_stdout.log
sudo touch /var/log/lazy_app/celery_stderr.log
sudo touch /var/log/lazy_app/api_stdout.log
sudo touch /var/log/lazy_app/api_stderr.log
sudo touch /var/log/lazy_app/cron_stdout.log
sudo touch /var/log/lazy_app/cron_stderr.log

update configuration to external hardrive

3) Lazy bot
git clone https://github.com/federulli/lazy_bot.git
virtualenv -p /usr/bin/python3 lazy_bot_venv
lazy_bot_venv/bin/pip install -r lazy_bot/requirements.txt
Update lazy_bot.conf with the token provided by botfather and the telegram username
sudo cp lazy_bot.conf /etc/supervisor/conf.d/

4) Plex
wget -O - https://dev2day.de/pms/dev2day-pms.gpg.key | sudo apt-key add -
echo "deb https://dev2day.de/pms/ jessie main" | sudo tee /etc/apt/sources.list.d/pms.list
sudo apt-get update
sudo apt-get install -t jessie plexmediaserver

mount hd
sudo mkdir /mnt/library
sudo mount /dev/sda1 /mnt/library
sudo vim /etc/fstab

add line:
PARTUUID=<get value from sudo blkid>       /mnt/library    <get value from sudo blkid> defaults          0       0