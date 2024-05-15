#!/bin/bash

# Install required software.
apt-get update
apt-get install -y openssh-server python3 python3-pip dos2unix python3-venv

# Copy project to container.
cd ../
cp -r ./limbosh /etc/limbosh
cd ./limbosh

# Fix line endings in entrypoint files, then source files.
dos2unix /etc/limbosh/limbosh*
find /etc/limbosh -type f -name '*.py' -print0 | xargs -0 dos2unix --

# Set appropriate permissions, create symlinks, register shell.
chmod +x /etc/limbosh/limbosh-docker
ln -s /etc/limbosh/limbosh-docker /usr/bin/limbosh
chmod +x /usr/bin/limbosh
echo '/usr/bin/limbosh' >> /etc/shells

# Set up Python dependencies.
cd /etc/limbosh
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Add admin:admin honeypot user with limbosh as shell.
useradd -rm -d /home/admin -s /usr/bin/limbosh -g root -G sudo -u 1000 admin && echo 'admin:admin' | chpasswd
