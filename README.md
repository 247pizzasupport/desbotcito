# Desbotcito

This is a discord bot that serves the sole purpose of memeing.

# How it works

bot.py is the control script that controls how the bot handles messages and what functionality it has.

# Using it

The python script is run as a systemd process, there is a service file in /etc/systemd/system that contains all the information to run the service.
Use systemctl stop, start, restart, enable/disable, and daemon-reload to control the script.
