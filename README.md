# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/thermometer-half.svg" card_color="#D81159" width="50" height="50" style="vertical-align:bottom"/> Wiser Heating
Controls the heating

Work In Progress - first go at a Mycroft skill
Uses Padatious intents, so commands need to include all settings in one go

So far uses wiserheatingapi API calls
* room.get("CalculatedTemperature")
* setRoomTemperature
* setRoomScheduleAdvance
* setRoomScheduleAdvanceUndo
* setRoomMode (Boost support)
* setHomeAwayMode

## Installation

mycroft-msm install https://github.com/steversig/wiser-heating-skill

## Configuration
* Either copy a wiserkeys.param file into the same directory as \_\_init\_\_.py
This is probably going to be /opt/mycroft/skills/wiser-heating-skill.steversig
* Or Log in to https://account.mycroft.ai and select Skills from the right hand top Personal menu.
Then click on the configure icon on the Wiser Heating app, fill in the Wiser Hub IP and key, then Save 

## About
Controls the heating via Mycroft AI, the wiserheatingapi library by Asantaga and a Wiser Heathub

## Examples
* "hey Mycroft what's the lounge temperature"
* "hey Mycroft temp|temperature lounge"
* "hey Mycroft lounge temp|temperature"
* "hey Mycroft house temp|temperature"
* "hey Mycroft heat lounge to 21"
* "hey Mycroft lounge heat 21"
* "hey Mycroft advance heat|heating lounge"
* "hey Mycroft advance heat|heating house"
* "hey Mycroft reset heat|heating lounge"
* "hey Mycroft boost lounge" - will add 2 degress for 30 mins
* "hey Mycroft boost lounge to 21" - will boost to 21 degrees for 30 mins
* "hey Mycroft boost lounge to 21 for 20" - will boost to 21 degrees for 20 mins
* "hey Mycroft set away mode" - sets away mode on and a default temperature of 7 degrees
* "hey Mycroft set away mode to 8" - sets away mode on and a temperature of 8 degrees
* "hey Mycroft I'm home" - clears away mode

## Credits
SteveR

## Thanks
Asantaga https://github.com/asantaga/wiserheatingapi for wiserheating api

Steve Ovens https://opensource.com/users/stratusss for several articles about Mycroft that helped me to make this work better

## Category
**IoT**

## Tags
#Wiser
#Heat
#Mycroft
