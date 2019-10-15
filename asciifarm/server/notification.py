

class Notification:
    
    type = None
    
    def toString(self):
        raise NotImplementedError
    
    def body(self):
        return []
    
    def toJSON(self):
        return [self.type, self.toString(), *self.body()]

class SoundNotification(Notification):
    
    type = "sound"
    
    def __init__(self, source, text):
        self.source = source
        self.text = text
    
    def toString(self):
        return self.source + ": " + self.text

class HealthNotification(Notification):
    
    text = None
    
    def __init__(self, actor, subject, health):
        self.actor = actor
        self.subject = subject
        self.health = health
    
    def toString(self):
        return self.text.format(actor=self.actor, subject=self.subject, health=self.health)

#print(HealthNotification, type(HealthNotification))
class AttackNotification(HealthNotification):
    
    type = "attack"
    text = "{actor} attacks {subject} for {health} damage"

class DamageNotification(HealthNotification):
    type = "damage"
    text = "{subject} got {health} damage from {actor}"

class HealNotification(HealthNotification):
    type = "heal"
    text = "{subject} got {health} health from {actor}"

class KillNotification(Notification):
    type = "kill"
    def __init__(self, actor, subject):
        self.actor = actor
        self.subject = subject
    
    def toString(self):
        return "{actor} kills {subject}".format(actor=self.actor, subject=self.subject)

class DieNotification(Notification):
    type = "die"
    def __init__(self, actor, subject):
        self.actor = actor
        self.subject = subject
    
    def toString(self):
        return "{subject} was killed by {actor}".format(actor=self.actor, subject=self.subject)
