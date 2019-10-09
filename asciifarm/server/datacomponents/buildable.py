

class Buildable:
    def __init__(self, template, flagsneeded=frozenset(), blockingflags=frozenset()):
        self.template = template
        self.flagsneeded = flagsneeded
        self.blockingflags = blockingflags
