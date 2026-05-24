#!/bin/bash
# ============================================
# HHW VPS Deployment Script
# Run as root or with sudo on Ubuntu/Debian
# ============================================

set -e

APP_DIR="/var/www/hhw"
PYTHON_VERSION="python3"

echo "=== 1. Installing system dependencies ==="
apt-get update
apt-get install -y python3 python3-pip python3-venv python3-dev \
    apache2 libapache2-mod-wsgi-py3 \
    mysql-server libmysqlclient-dev \
    build-essential

echo "=== 2. Creating application directory ==="
mkdir -p $APP_DIR
cp -r . $APP_DIR/
chown -R www-data:www-data $APP_DIR

echo "=== 3. Setting up Python virtual environment ==="
cd $APP_DIR
$PYTHON_VERSION -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r nutras/requirements.txt

echo "=== 4. Creating log directories ==="
mkdir -p $APP_DIR/nutras/logs
touch $APP_DIR/nutras/test.log
chown -R www-data:www-data $APP_DIR/nutras/logs
chown www-data:www-data $APP_DIR/nutras/test.log

echo "=== 5. Setting up MySQL database ==="
echo "-----------------------------------------------"
echo "  Make sure MySQL is running. Then run:"
echo "    sudo mysql -u root"
echo "    CREATE DATABASE IF NOT EXISTS registration;"
echo "    CREATE USER 'root'@'localhost' IDENTIFIED BY 'root';"
echo "    GRANT ALL PRIVILEGES ON registration.* TO 'root'@'localhost';"
echo "    FLUSH PRIVILEGES;"
echo "-----------------------------------------------"

echo "=== 6. Configuring Apache ==="
cp $APP_DIR/hhw.conf /etc/apache2/sites-available/hhw.conf
a2enmod wsgi
a2ensite hhw.conf
a2dissite 000-default.conf

echo "=== 7. Setting permissions ==="
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR

echo "=== 8. Restarting Apache ==="
systemctl restart apache2
systemctl enable apache2

echo "=== Deployment complete! ==="
echo "Check status with: systemctl status apache2"
echo "Check logs with: tail -f /var/log/apache2/hhw-error.log"
