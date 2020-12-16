from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger

from wiserHeatingAPI import wiserHub
import json
import sys

__author__ = 'steversig'
LOGGER = getLogger(__name__)

# Timeout time for Wiser requests
TIMEOUT = 10


class WiserHeatingSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        super().__init__(name="WiserHeatingSkill")
        self.wh = None

    def initialize(self):
        my_setting = self.settings.get('my_setting')
        wiserkey=""
        wiserhubip=""
        # connect to the wiser hub
        try:
            try:
                self.wh = wiserHub.wiserHub(wiserhubip,wiserkey)
            except:
                LOGGER.debug("Unable to connect to Wiser Hub {}".format(sys.exc_info()[1])    )
                LOGGER.debug (' Wiser Hub IP= {}'.format(wiserip))
                LOGGER.debug (' WiserKey= {}'.format(wiserkey))
        except json.decoder.JSONDecodeError as ex:
            LOGGER.debug("JSON Exception")

    @intent_file_handler('heating.wiser.advance.intent')
    def handle_heating_wiser_advance(self, message):
        self.speak_dialog('heating.wiser.advance')

    @intent_file_handler('heating.wiser.awaymode.intent')
    def handle_heating_wiser_awaymode(self, message):
        self.speak_dialog('heating.wiser.awaymode')

    @intent_file_handler('heating.wiser.boost.intent')
    def handle_heating_wiser_boost(self, message):
        self.speak_dialog('heating.wiser.boost')

    @intent_file_handler('heating.wiser.getroomtemp.intent')
    def handle_heating_wiser_getroomtemp(self, message):
        adv_room ="All"
        response = ""
        for room in self.wh.getRooms():
            name = room.get("Name")
            if adv_room == "All" or name == adv_room:
                response += "{} {} degrees ".format(name,room.get("CalculatedTemperature")/10)
        LOGGER.info(response)
        self.speak_dialog(response.replace('.', ' point '))

    @intent_file_handler('heating.wiser.setroomtemp.intent')
    def handle_heating_wiser_setroomtemp(self, message):
        self.speak_dialog('heating.wiser.setroomtemp')

    def stop(self):
        pass

def create_skill():
    return WiserHeatingSkill()

