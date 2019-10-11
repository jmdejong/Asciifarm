
class Control:
    
    name = None
    
    def do_json(self):
        raise NotImplementedError
    
    @classmethod
    def from_json(cls, jsondata):
        name, arg = jsondata
        assert name == cls.name, "Control names do not match: {}, {}".format(name, cls.name)
        return cls(arg)
    

_DIRECTIONS = {"north", "south", "east", "west"}
_ALL_DIRECTIONS = _DIRECTIONS | {None}


class MoveControl(Control):
    name = "move"
    def __init__(self, direction):
        assert direction in _DIRECTIONS, "Unknown direction: " + str(direction)
        self.direction = direction
    
    def to_json(self):
        return [self.name, self.direction]

class RankedControl(Control):
    def __init__(self, rank=None):
        assert rank is None or isinstance(rank, int) and rank >= 0, "rank is not positive numeric: " + str(rank)
        self.rank = rank
    
    def to_json(self):
        return [self.name, self.rank]
    

class TakeControl(RankedControl):
    name = "take"

class DropControl(RankedControl):
    name = "drop"

class UseControl(RankedControl):
    name = "use"
    def __init__(self, container, rank=None):
        assert rank is None or isinstance(rank, int) and rank >= 0, "rank is not positive numeric: " + str(rank)
        assert container in ("inventory", "equipment"), "Invalid container: " + str(container)
        self.container = container
        self.rank = rank
    
    def to_json(self):
        return [self.name, self.rank]
    
    @classmethod
    def from_json(cls, jsondata):
        name, container, rank = jsondata
        assert name == cls.name, "Control names do not match: {}, {}".format(name, cls.name)
        return cls(container, rank)


class InteractControl(Control):
    name = "interact"
    def __init__(self, directions=(), parameter=None):
        for direction in directions:
            assert direction in _ALL_DIRECTIONS, "Unknown direction: " + str(direction)
        self.directions = directions
        self.parameter = parameter
    
    def to_json(self):
        return [self.name, self.directions, parameter]
    
    @classmethod
    def from_json(cls, jsondata):
        if len(jsondata) == 3:
            name, directions, parameter = jsondata
        else:
            name, directions = jsondata
            parameter = None
        assert name == cls.name, "Control names do not match: {}, {}".format(name, cls.name)
        return cls(directions, parameter)
    

class AttackControl(Control):
    name = "attack"
    def __init__(self, directions=()):
        for direction in directions:
            assert direction in _ALL_DIRECTIONS, "Unknown direction: " + str(direction)
        self.directions = directions
    
    def to_json(self):
        return [self.name, self.directions]
    

class SayControl(Control):
    name = "say"
    def __init__(self, text):
        assert isinstance(text, str), "text is not a string: " + str(text)
        self.text = text
    
    def to_json(self):
        return [self.name, text]

_controls_by_name = {control.name: control for control in [
    MoveControl,
    TakeControl,
    DropControl,
    UseControl,
    InteractControl,
    AttackControl,
    SayControl
]}

def controlFromJson(jsondata):
    return _controls_by_name[jsondata[0]].from_json(jsondata)


