from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
from mycroft.util.parse import match_one
from mycroft.util.parse import extract_number
from mycroft.util.format import pronounce_number
from mycroft.util.format import nice_number

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
        if self.settings.get('wiserhousename') is not None:
            self.my_house = self.settings.get('wiserhousename')
        else:
            self.my_house = "house"
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

    def match_room(self, my_room, wiserrooms): # Nudge room name towards best match of room from Wiser Hub
        rooms = ['house']
        pronounce_to_name = {'house':'house'}
        for room in wiserrooms:
            name = room.get("Name").lower()
            rooms.append(name)
            pronounce_to_name[name] = name
            ex_number = extract_number(name, short_scale=True, ordinals=False, lang=None)
            if ex_number != False: # add alternative with one set of spelled out numbers
                n_number = pronounce_number(ex_number, lang=None, places=2)
                name_num = name.replace(str(ex_number),n_number)
                #LOGGER.info("{} => {} => {}".format(ex_number, n_number, name_num))
                rooms.append(name_num)
                pronounce_to_name[name_num] = name
        #LOGGER.info(pronounce_to_name)
        #LOGGER.info(rooms)
        match, confidence = match_one(my_room, list(rooms))
        LOGGER.info("Match room: ({} <=> {}) @{:.4f} => {}".format(my_room, match, confidence, pronounce_to_name[match]))
        if confidence > 0.65:
            return pronounce_to_name[match]
        else:
            return my_room

    @intent_file_handler('heating.wiser.advance.intent')
    def handle_heating_wiser_advance(self, message):
        my_room = message.data["wiserroom"].lower()
        logresponse = ""
        try:
            wiserrooms = self.wh.getRooms()
        except AttributeError:
            self.speak_dialog('heating.wiser.lostcomms')		
            self._setup()			
        else:
            my_room = self.match_room(my_room, wiserrooms) # get the nearest matching room
            for room in wiserrooms:
                name = room.get("Name").lower()
                roomId = room.get("id")
                if my_room == self.my_house or name == my_room:
                    try:
                        self.wh.setRoomScheduleAdvance(roomId)
                    except AttributeError:
                        self.speak_dialog('heating.wiser.lostcomms')
                        self._setup()			
                    else:
                        self.speak_dialog('heating.wiser.advance', 
                            {"wiserroom": name})
                        logresponse += "{} ".format(name)
            LOGGER.info("Advance: {} ".format(logresponse))
            if logresponse == "":
                self.speak_dialog('heating.wiser.unknown.room', 
                                  {"wiserroom": my_room})

    @intent_file_handler('heating.wiser.awaymode.away.intent')
    def handle_heating_wiser_awaymode_away(self, message):
        LOGGER.info("awaymode away: {}".format(message.data))
        temperature = 7 
        if message.data.get('wisertemp') != None:
            temperature = round(float(message.data["wisertemp"])*2)/2 
        try:
            self.wh.setHomeAwayMode("AWAY",int(temperature))
        except ValueError as e:
            LOGGER.error("awaymode away: {}".format(e))
        except:
            self.speak_dialog('heating.wiser.lostcomms')
            self._setup()			
        else:
            LOGGER.info("awaymode: away at {}".format(temperature))
            self.speak_dialog('heating.wiser.awaymode.away',
                             {"wisertemp": temperature})

    @intent_file_handler('heating.wiser.awaymode.home.intent')
    def handle_heating_wiser_awaymode_home(self, message):
        LOGGER.info("awaymode home: {}".format(message.data))
        try:
            self.wh.setHomeAwayMode("HOME")
        except ValueError as e:
            LOGGER.error("awaymode home: {}".format(e))
        except AttributeError:
            self.speak_dialog('heating.wiser.lostcomms')
            self._setup()			
        else:
            self.speak_dialog('heating.wiser.awaymode.home')

    @intent_file_handler('heating.wiser.boost.intent')
    def handle_heating_wiser_boost(self, message):
        LOGGER.info(message.data)
        my_room = message.data["wiserroom"].lower()
        myparams = ""
        try:
            mytemp = message.data["wisertemp"]
        except KeyError:
            mytemp = 2
        else:
            mytemp = round(float(mytemp)*2)/2
        myparams += ",{} deg ".format(str(mytemp))
        try:
            mytime = int(message.data['wisertime'])
        except KeyError:
            mytime = 30
        myparams += ",{} mins ".format(str(mytime))

        logresponse = ""
        try:
            self.wh.refreshData()
        except ValueError as e:
            LOGGER.error(e)
            self.speak_dialog('heating.wiser.lostcomms')		
            self._setup()			
        else:
            wiserrooms = self.wh.getRooms()
            my_room = self.match_room(my_room, wiserrooms) # get the nearest matching room
            for room in wiserrooms:
                name = room.get("Name").lower()
                roomId = room.get("id")
                if my_room == self.my_house or name == my_room:
                    if mytemp == 2:
                        dtemp = float(room.get("CalculatedTemperature")/10 +2)
                        settemp = dtemp
                    else:
                        settemp = mytemp
                    #LOGGER.info("boost: id:{} {} {}".format(roomId,settemp,mytime))
                    try:
                        self.wh.setRoomMode(roomId,"boost",settemp,mytime)
                    except ValueError as e:
                        LOGGER.error("boost: {}".format(e))
                    except AttributeError:
                        self.speak_dialog('heating.wiser.lostcomms')
                        self._setup()			
                    else:
                        nice_settemp = nice_number(settemp, lang=None, speech=True, denominators=None)
                        self.speak_dialog('heating.wiser.boost', 
                            {"wiserroom": name, "wisertemp": nice_settemp, "wisertime": int(mytime)})
                        logresponse += "{} ".format(name)
            logresponse += myparams
            logresponse = logresponse.replace('2 deg','+2 deg')
            LOGGER.info("boost: {}".format(logresponse))
            if logresponse == "":
                self.speak_dialog('heating.wiser.unknown.room', {
                                  "wiserroom": my_room})

    @intent_file_handler('heating.wiser.getroomtemp.intent')
    def handle_heating_wiser_getroomtemp(self, message):
        my_room = message.data["wiserroom"].lower()
        logresponse = ""
        try:
            self.wh.refreshData()
        except ValueError as e:
            LOGGER.error(e)
            self._setup()			
        else:
            wiserrooms = self.wh.getRooms()
            my_room = self.match_room(my_room, wiserrooms) # get the nearest matching room
            for room in wiserrooms:
                name = room.get("Name").lower()
                if my_room == self.my_house or name == my_room:
                    temperature = room.get("CalculatedTemperature")/10
                    self.speak_dialog('heating.wiser.temperature', 
                        {"wiserroom": name, "wisertemp": temperature})
                    logresponse += "{} {} ".format(name,temperature)
            if logresponse == "":
                LOGGER.info("getroomtemp: unknown room _{}_".format(my_room))
                self.speak_dialog('heating.wiser.unknown.room', {
                                  "wiserroom": my_room})
            else:
                LOGGER.info("getroomtemp: {} ".format(logresponse))

    @intent_file_handler('heating.wiser.reset.intent')
    def handle_heating_wiser_reset(self, message):
        my_room = message.data["wiserroom"].lower()
        logresponse = ""
        try:
            wiserrooms = self.wh.getRooms()
        except AttributeError:
            self.speak_dialog('heating.wiser.lostcomms')		
            self._setup()			
        else:
            my_room = self.match_room(my_room, wiserrooms) # get the nearest matching room
            for room in wiserrooms:
                name = room.get("Name").lower()
                roomId = room.get("id")
                if my_room == self.my_house or name == my_room:
                    try:
                        self.wh.setRoomScheduleAdvanceUndo(roomId)
                    except AttributeError:
                        self.speak_dialog('heating.wiser.lostcomms')		
                        self._setup()			
                    else:
                        self.speak_dialog('heating.wiser.reset', 
                        {"wiserroom": name})
                        logresponse += "{} ".format(name)
            LOGGER.info("Reset: {} ".format(logresponse))
            if logresponse == "":
                self.speak_dialog('heating.wiser.unknown.room', {
                                  "wiserroom": my_room})

    @intent_file_handler('heating.wiser.setroomtemp.intent')
    def handle_heating_wiser_setroomtemp(self, message):
        LOGGER.info("setroomtemp: {}".format(message.data))
        my_room = message.data["wiserroom"].lower()
        if message.data.get('wisertemp') != None:
            temperature = round(float(message.data["wisertemp"])*2)/2
            logresponse = ""
            try:
                wiserrooms = self.wh.getRooms()
            except AttributeError:
                self.speak_dialog('heating.wiser.lostcomms')		
            else:
                my_room = self.match_room(my_room, wiserrooms) # get the nearest matching room
                for room in wiserrooms:
                    name = room.get("Name").lower()
                    roomId = room.get("id")
                    if my_room == self.my_house or name == my_room:
                        try:
                            self.wh.setRoomTemperature(roomId, temperature)
                        except ValueError as e:
                            LOGGER.error("setroomtemp: {}".format(e))
                        except WiserRESTException as e:
                            LOGGER.error("setroomtemp: {}".format(e))
                        except AttributeError:
                            self.speak_dialog('heating.wiser.lostcomms')		
                            self._setup()			
                        else:
                            self.speak_dialog('heating.wiser.temperature', 
                                {"wiserroom": name, "wisertemp": temperature})
                            logresponse += "{} => {} ".format(name,temperature)
                LOGGER.info("setroomtemp: {}".format(logresponse))
                if logresponse == "":
                    self.speak_dialog('heating.wiser.unknown.room', {
                                      "wiserroom": my_room})

    def stop(self):
        pass

def create_skill():
    return WiserHeatingSkill()

