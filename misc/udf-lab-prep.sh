#!/bin/bash

# Ensure the script is run with root privileges
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

# Create /etc/systemd/resolved.conf.d directory if it doesn't exist
mkdir -p /etc/systemd/resolved.conf.d

# Create resolved.conf file with specified settings
cat <<EOF >/etc/systemd/resolved.conf.d/custom.conf
[Resolve]
DNSStubListener=no
DNS=127.0.0.1
EOF

# Restart systemd-resolved to apply changes
systemctl restart systemd-resolved

# Install dnsmasq
apt-get update --quiet
apt-get install --quiet --yes dnsmasq

# Configure dnsmasq to forward specific domain requests to given IP
cat <<EOF >/etc/dnsmasq.d/mcn-lab.conf
server=/mcn-lab.f5demos.com/10.1.1.4
address=/ubuntu/127.0.0.1
EOF

# Restart dnsmasq to apply the new configuration
systemctl restart dnsmasq

echo "Configuration complete."
