Feature: advance temperature in room
  Scenario Outline: advance temperature
    Given an English speaking user
     When the user says "<advance room>"
     Then "wiser-heating-skill.steversig" should reply with dialog from "heating.wiser.advance.dialog"
	 
	Examples:
	| advance room |
    | Advance hall |
    | Advanced hall |
    | Advance the hall |
    | Advance eat hall |
    | Advance heat hall |
    | Advance heating hall |
    | Advance heat in the hall |
    | Advance heat in hall |
	
#(Advance|Advanced) (|the) (eat|heat|heating) (|in the|in) {wiserroom}
#(Advance|Advanced) (|the) (eat in the|heat in the|heating in the|eat in|heat in|heating in|eat|heat|heating|) {wiserroom}
