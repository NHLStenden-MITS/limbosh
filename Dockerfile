FROM ubuntu:jammy

# Install Python and OpenSSH server.
RUN apt-get update
RUN apt-get install -y openssh-server python3 python3-pip dos2unix

# Copy project to container.
COPY . /etc/limbosh

# Fix line endings in entrypoint files.
RUN dos2unix /etc/limbosh/limbosh*

# Set appropriate permissions, create symlinks, register shell.
RUN chmod +x /etc/limbosh/limbosh-docker
RUN ln -s /etc/limbosh/limbosh-docker /usr/bin/limbosh
RUN chmod +x /usr/bin/limbosh
RUN echo '/usr/bin/limbosh' >> /etc/shells

# Set up Python dependencies.
WORKDIR /etc/limbosh
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Add admin:admin honeypot user with limbosh as shell.
RUN useradd -rm -d /home/admin -s /usr/bin/limbosh -g root -G sudo -u 1000 admin && echo 'admin:admin' | chpasswd

# Restart SSH service to enable login and sleep forever.
CMD limbosh
