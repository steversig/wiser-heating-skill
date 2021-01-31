Feature: awaymode away
  Scenario Outline: away mode away
    Given an English speaking user
     When the user says "<away mode away>"
     Then "wiser-heating-skill.steversig" should reply with dialog from "heating.wiser.awaymode.away.dialog"
	 
	Examples:
	| away mode away |
    | Set awaymode on |
    | Set away mode on |
    | Set awaymode to 7 |
    | Set awaymode to 7 |
    | away mode on |
    | awaymode on |
    | awaymode to 7 |
    | awaymode 2 7 |
	
#Set (away mode|awaymode) (on|to|2 {wisertemp})
#(away mode|awaymode) (on|to {wisertemp}|2 {wisertemp})
