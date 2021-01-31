Feature: reset advance
  Scenario Outline: reset advance
    Given an English speaking user
     When the user says "<reset room>"
     Then "wiser-heating-skill.steversig" should reply with dialog from "heating.wiser.reset.dialog"
	 
	Examples:
	| reset room |
    | Reset hall |
    | Reset the hall |
    | Reset eat hall |
    | Reset heat hall |
    | Reset heating hall |
    | Reset heat in the hall |
    | Reset heat in hall |
	
#Reset (|the) (eat|heat|heating) (|in the|in) {wiserroom}
#(Reset the|Reset) (eat in the|heat in the|heating in the|eat in|heat in|heating in|eat|heat|heating|) {wiserroom}