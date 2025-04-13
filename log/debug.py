class DebugHandler:
    def __init__(self, name):
        self.name = name
        self.debug = False

    def print(self, message):
        if self.debug:
            print(f"{self.name}: {message}")

    # Debug Print Function
    def dprint(self, *args):
        if self.debug:
            print(f"{self.name}: ", *args)
