
class Message:
    def __init__(self, parser:dict) -> None:
        self.parser = parser
    def print(self, message):
        if self.parser["system"]["quiet_mode"] == "True":
            return
        print(message)