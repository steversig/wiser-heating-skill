from mycroft import MycroftSkill, intent_file_handler


class WiserHeating(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('heating.wiser.intent')
    def handle_heating_wiser(self, message):
        self.speak_dialog('heating.wiser')


def create_skill():
    return WiserHeating()

