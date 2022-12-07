# KotBot
#Discord bot with AI utilities

After run message bot with !help for list of commands.
Some of current utilities:

!genanything
Will generate anything you want to see,
optional params: amount=, sampling_steps=, CFG= example cat in house amount=3 sampling_steps=40 CFG=15
command give prompts and options to one of various stabble diffusion models, which are installed locally

!catgen
Instantly send unique picture of computer generated cat image from internet site

!cat
get random picture of cat from local folders with cat pics

!roll_dice 
simulated rolling the dice, need to be given: number of dices, number of sides

Bot on fixed intervals send random message from list of poke_messages on specified channel

There are more utilities which are subject to change

Requires .env file with Discord Token, Discord Guild and Discord Channel ID and vars.py file with variables: trivias (list), status (string), poke_messages (list), poke_channel (channel id)
