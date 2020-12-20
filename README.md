# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/thermometer-half.svg" card_color="#D81159" width="50" height="50" style="vertical-align:bottom"/> Wiser Heating
Controls the heating

Very much Initial Work In Progress - first go at a mycroft skill

So far uses wiserheatingapi API calls
* room.get("CalculatedTemperature")
* setRoomTemperature
* setRoomScheduleAdvance
* setRoomScheduleAdvanceUndo

to do
* setHomeAwayMode
* setRoomMode (Boost support)

## Installation

mycroft-msm install https://github.com/steversig/wiser-heating-skill

Then copy a wiserkeys.param file into the same directory as \_\_init\_\_.py
this is probably going to be /opt/mycroft/skills/wiser-heating-skill.steversig

## About
Controls the heating via Mycroft AI, the wiserheatingapi library by Asantaga and a Wiser Heathub

## Examples
* "hey Mycroft what's the lounge temperature"
* "hey Mycroft temp|temperature lounge"
* "hey Mycroft lounge temp|temperature"
* "hey Mycroft house temp|temperature"
* "hey Mycroft heat lounge to 21" - parsing issues
* "hey Mycroft lounge heat 21"
* "hey Mycroft advance heat|heating lounge"
* "hey Mycroft advance heat|heating house"
* "hey Mycroft reset heat|heating lounge"

## Credits
SteveR

## Category
**IoT**

## Tags
#Wiser
#Heat
#Mycroft
