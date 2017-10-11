class MidiNote:
    def __init__(self, value, velocity, duration):
        self.value = value
        self.velocity = velocity
        self.duration = duration
        self.On = 0x90
        self.Off = 0x80

