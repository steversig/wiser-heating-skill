Feature: boost temperature in room
  Scenario Outline: boost temperature
    Given an English speaking user
     When the user says "<boost room>"
     Then "wiser-heating-skill.steversig" should reply with dialog from "heating.wiser.boost.dialog"
	 
	Examples:
	| boost room |
    | hall Boost |
    | hall Boost heat |
    | hall Boost heating |
    | hall Boost to 15 |
    | hall Boost to 15 for 5|
    | hall Boost for 5 |
    | hall Boost for 5 to 15|
    | Boost hall |
    | Boost heat hall |
    | Boost heating hall |
    | Boost hall to 15 |
    | Boost hall to 15 for 5|
    | Boost hall for 5 |
    | Boost hall for 5 to 15|
	
#{wiserroom} (Boost|Boost heat|Boost heating) (|to {wisertemp}) (|for {wisertime})
#{wiserroom} (Boost|Boost heat|Boost heating) (|for {wisertime}) (|to {wisertemp}) 
#(Boost heat|Boost heating|Boost) {wiserroom} (|to {wisertemp}) (|for {wisertime})
#(Boost heat|Boost heating|Boost) {wiserroom} (|for {wisertime}) (|to {wisertemp})