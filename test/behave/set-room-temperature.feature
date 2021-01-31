Feature: set-room-temperature
  Scenario Outline: set room temperature
    Given an English speaking user
     When the user says "<set room temperature>"
     Then "wiser-heating-skill.steversig" should reply with dialog from "heating.wiser.temperature.dialog"
	 
	Examples:
	| set room temperature |
    | Heat hall to 15 |
    | Heat the hall to 15 |
    | Heat hall 2 15 |
    | Heat the hall 2 15 |
    | hall Heat to 15 |
    | hall Heat 2 15 |
	
