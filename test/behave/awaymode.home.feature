Feature: awaymode home
  Scenario Outline: away mode home
    Given an English speaking user
     When the user says "<away mode home>"
     Then "wiser-heating-skill.steversig" should reply with dialog from "heating.wiser.awaymode.home.dialog"
	 
	Examples:
	| away mode home |
    | Back home |
    | Returned home |
    | I am home |
    | I'm home |
    | away mode off|
    | awaymode off|
    | set away mode off|
    | set awaymode off|
	
#(Back|Returned|I am|I'm) home
#(away mode|awaymode|Set away mode|Set awaymode) off