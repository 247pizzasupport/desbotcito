# Desbotcito

This is a discord bot that serves the sole purpose of memeing.

# How it works

bot.py is the control script that controls how the bot handles messages and what functionality it has.

# Using it

The python script is run as a systemd process, there is a service file in /etc/systemd/system that contains all the information to run the service.
Use systemctl stop, start, restart, enable/disable, and daemon-reload to control the script.

# What does it do?

Below are the current list of functions that the bot has:

* Messages asking Alexa to play Despacito will link to the youtube video for Despacito
* Messages alluding to September will link to the youtube video for September (Bass Boosted)
* Messages in which it has been will send a copy of its_been.mp3
* Messages containing the forbidden v-word will reset the counter and announce how long it has been since the word was used as well has how many times that user has used the word
* !roll XdY rolls X Y-sided dice and sends back the result
* !shrug (@ user) sends back the shrug emoji and optionally mentions another user in the message (Does not work with @ everyone and @ here)
* !anime selects a random anime from MyAnimeList (In testing)
* If you ask 'How valid is ___', the bot will tell you how valid it is. (With new and improved pseudo-randomness!)
* !8ball asks the 8ball a question and you will receive an answer.
* !fmk x,y,z : Provide the bot with three options and she will select which ones to bed, wed, and behead.
