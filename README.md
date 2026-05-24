# HHW - Hamri's Health and Wellness

https://hamrishealthandwellness.com

Flask web application deployed on Ubuntu/Debian VPS with Apache + mod_wsgi.

## Quick Deploy (Ubuntu/Debian VPS)

```bash
# 1. Clone the repo to the server
git clone <your-repo-url> /var/www/hhw
cd /var/www/hhw

# 2. Run the deploy script
sudo bash deploy.sh
```

## Manual Deploy Steps

### Prerequisites
- Ubuntu 20.04+ / Debian 11+
- Python 3.8+
- MySQL Server
- Apache2 with mod_wsgi

### 1. Install System Packages
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev \
    apache2 libapache2-mod-wsgi-py3 \
    mysql-server libmysqlclient-dev build-essential
```

### 2. Set Up the App
```bash
sudo mkdir -p /var/www/hhw
sudo cp -r . /var/www/hhw/
cd /var/www/hhw
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. Set Up MySQL
```sql
CREATE DATABASE IF NOT EXISTS registration;
-- Update MYSQL_USER and MYSQL_PASSWORD in nutras/__init__.py if needed
```

### 4. Configure Apache
```bash
sudo cp hhw.conf /etc/apache2/sites-available/hhw.conf
# Edit hhw.conf: update ServerName to your domain or IP
sudo a2enmod wsgi
sudo a2ensite hhw.conf
sudo a2dissite 000-default.conf
sudo systemctl restart apache2
```

### 5. Set Permissions
```bash
sudo chown -R www-data:www-data /var/www/hhw
sudo chmod -R 755 /var/www/hhw
```

## Configuration

Edit `nutras/__init__.py` to update:
- **MySQL credentials**: `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`
- **Mail settings**: `MAIL_USERNAME`, `MAIL_PASSWORD`

Edit `hhw.conf` to update:
- **ServerName**: your actual domain or VPS IP address

Edit `hhw.wsgi` if using a different install path than `/var/www/hhw/`.

## Troubleshooting
```bash
# Check Apache status
sudo systemctl status apache2

# Check Apache error logs
sudo tail -f /var/log/apache2/hhw-error.log

# Check app log
tail -f /var/www/hhw/nutras/test.log

# Test WSGI manually
cd /var/www/hhw && source env/bin/activate && python -c "from nutras import app; print('OK')"
```
