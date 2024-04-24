#!/bin/bash

# Ping google.com
ping -c 1 google.com > /dev/null

# Vérifier le code de retour de la commande ping
if [ $? -eq 0 ]; then
    echo "True" > /etc/LedService/connected.conf
else
    echo "False" > /etc/LedService/connected.conf
fi
