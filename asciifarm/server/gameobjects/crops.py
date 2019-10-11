

from ..entity import Entity
from ..datacomponents import Interact, Loot, Remove, Serialise, Static, LootMessage, Periodic, StartTimer, Create, Item, Food, Buildable
from ..template import Template

entities = {}

def cropSerializer(name):
    return (lambda obj, roomData:
        Template(name, targetTime=roomData.getComponent(obj, Periodic).targetTime)
    )

class Stage:
    
    def __init__(self, name, sprite=None, height=0.5, shownname=None, duration=None, harvest=None):
        self.name = name
        self.duration = duration
        self.sprite = sprite or name
        self.height = height
        self.shownname = shownname or name
        self.harvest = harvest
    
    def create(self, cropname="", nextstage=None, timestep=1):
        name = self.name.format(cropname)
        def makeEntity(targetTime=None):
            dataComponents = []
            if self.duration is not None:
                ongrow = [Remove, Create(Template(nextstage))]
                if targetTime is None:
                    timer = Periodic(ongrow, self.duration * timestep)
                else:
                    timer = Periodic(ongrow, targetTime=targetTime)
                dataComponents.append(timer)
                dataComponents.append(Serialise(cropSerializer(name)))
                dataComponents.append(StartTimer())
            else:
                dataComponents.append(Static(name))
            if self.harvest is not None:
                dataComponents.append(Interact(LootMessage, Remove))
                dataComponents.append(Loot(self.harvest))
            flags = {"occupied"}
            return Entity(
                sprite=self.sprite.format(cropname),
                height=self.height,
                name=self.shownname.format(cropname),
                flags=flags,
                dataComponents=dataComponents
            )
        entities[name] = makeEntity

    
    @classmethod
    def Seed(cls, duration):
        return cls("planted{}seed", duration=duration, sprite="seed", height=0.05, shownname="plantedseed")
    
    @classmethod
    def Seedling(cls, duration):
        return cls("planted{}seedling", duration=duration, sprite="seedling", height=0.09, shownname="seedling")
    
    @classmethod
    def YoungPlant(cls, duration, height=0.4):
        return cls("young{}plant", duration=duration, sprite="youngplant", height=height)


def createCrop(name, stages, timestep=1):
    seedname = "{}seed".format(name)
    sownname = "sown{}seed".format(name)
    stagenames = [stage.name.format(name) for stage in stages]
    entities[seedname] = lambda: Entity(
        sprite="seed",
        name=seedname,
        height=0.2,
        dataComponents=[Static(seedname), Item, Buildable(Template(stagenames[0]), flagsneeded={"soil"}, blockingflags={"occupied", "solid"})]
    )
    
    for i, stage in enumerate(stages[:-1]):
        nextstage = stagenames[i+1]
        stage.create(name, nextstage, timestep)
    stages[-1].create(name, None)


createCrop("carrot", [
    Stage.Seed(20),
    Stage.Seedling(40),
    Stage("carrotplant", sprite="smallplant", height=0.5, harvest=[("carrot", 1), ("carrotseed", 1)])
], 600)

entities["carrot"] = lambda: Entity(sprite="food", name="carrot", height=0.3, dataComponents=[Static("carrot"), Item, Food(5)])


createCrop("radish", [
    Stage.Seed(3),
    Stage.Seedling(3),
    Stage.YoungPlant(6),
    Stage(
        "{}plant",
        sprite="smallplant",
        height=0.5,
        harvest=[("radishseed", .92), ("radishseed", .20), ("radishes", .8), ("radishes", .4)]
    )
], 10)

entities["radishes"] = lambda: Entity(sprite="food", name="radishes", height=0.3, dataComponents=[Static("radishes"), Item, Food(3)])

entities["food"] = entities["radishes"]
entities["sownseed"] = entities["plantedradishseed"]
entities["youngplant"] = entities["youngradishplant"]
entities["plant"] = entities["radishplant"]
entities["seed"] = entities["radishseed"]

entities["eldritch_radish"] = lambda: Entity(sprite="food", name="eldritch radishes", height=0.3, dataComponents=[Static("eldritch_radish"), Item, Food(20)])



