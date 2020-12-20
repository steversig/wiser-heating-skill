from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger

from wiserHeatingAPI import wiserHub
import json
import sys
import os.path

__author__ = 'steversig'
LOGGER = getLogger(__name__)

# Timeout time for Wiser requests
TIMEOUT = 10


class WiserHeatingSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        super().__init__(name="WiserHeatingSkill")
        self.wh = None

    def _setup(self, force=False):
        try:
            pwd = os.path.dirname(os.path.abspath(__file__))
            fpath = os.path.join(pwd, 'wiserkeys.params')
            LOGGER.info(fpath)
            with open(fpath, 'r') as f:
                data = f.read().split('\n')
        except FileNotFoundError as e:
            LOGGER.debug("{}, {}".format(e.strerror, fpath)    )
        else:
            wiserkey=""
            wiserip=""

            for lines in data:
                line=lines.split('=')
                if line[0]=='wiserkey':
                    wiserkey=line[1]
                if line[0]=='wiserhubip':
                    wiserhubip=line[1]

        if self.settings.get('wiserkey') is not None:
            wiserkey = self.settings.get('wiserkey')
        if self.settings.get('wiserhubip') is not None:
            wiserhubip = self.settings.get('wiserhubip')
        # connect to the wiser hub
        try:
            try:
                self.wh = wiserHub.wiserHub(wiserhubip,wiserkey)
            except:
                LOGGER.debug("Unable to connect to Wiser Hub {}".format(sys.exc_info()[1])    )
                LOGGER.debug (' Wiser Hub IP= {}'.format(wiserhubip))
                LOGGER.debug (' WiserKey= {}'.format(wiserkey))
        except json.decoder.JSONDecodeError as ex:
            LOGGER.debug("JSON Exception")

    def initialize(self):
        self._setup()

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
        myroom = message.data["wiserroom"].lower()
        logresponse = ""
        for room in self.wh.getRooms():
            name = room.get("Name").lower()
            if myroom == "house" or name == myroom:
                temperature = room.get("CalculatedTemperature")/10
                self.speak_dialog('heating.wiser.temperature', 
                    {"wiserroom": name, "wisertemp": temperature})
                logresponse += "{} {} ".format(name,temperature)
        LOGGER.info("getroomtemp: {} ".format(logresponse))
        if logresponse == "":
            self.speak_dialog('heating.wiser.unknown.room', {
                              "wiserroom": myroom})

    @intent_file_handler('heating.wiser.setroomtemp.intent')
    def handle_heating_wiser_setroomtemp(self, message):
        myroom = message.data["wiserroom"].lower()
        temperature = round(float(message.data["wisertemp"])*2)/2
        logresponse = ""
        for room in self.wh.getRooms():
            name = room.get("Name").lower()
            roomId = room.get("id")
            if myroom == "house" or name == myroom:
                self.wh.setRoomTemperature(roomId, temperature)
                self.speak_dialog('heating.wiser.temperature', 
                    {"wiserroom": name, "wisertemp": temperature})
                logresponse += "{} => {} ".format(name,temperature)
        LOGGER.info("setroomtemp: {}".format(logresponse))
        if logresponse == "":
            self.speak_dialog('heating.wiser.unknown.room', {
                              "wiserroom": myroom})

    def stop(self):
        pass

def create_skill():
    return WiserHeatingSkill()

