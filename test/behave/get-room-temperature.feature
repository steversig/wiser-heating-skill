Feature: get-room-temperature
  Scenario Outline: get room temperature
    Given an English speaking user
     When the user says "<get hall temperature>"
     Then "wiser-heating-skill.steversig" should reply with dialog from "heating.wiser.temperature.dialog"
	 
	Examples:
	| get hall temperature |
    | What is the hall temperature |
    | What is the hall temp |
    | What's the hall temperature |
    | What's the hall temp |
    | Get hall temperature |
    | Get hall temp |
    | Get me hall temperature |
    | Get me hall temp |
    | Get the hall temperature |
    | Get the hall temp |
    | Get me the hall temperature |
    | Get me the hall temp |

  Scenario Outline: unknown room
    Given an English speaking user
     When the user says "<get unknown temperature>"
     Then "wiser-heating-skill.steversig" should reply with dialog from "heating.wiser.unknown.room.dialog"

	Examples:
	| get unknown temperature |
    | What is the garden temperature |
	