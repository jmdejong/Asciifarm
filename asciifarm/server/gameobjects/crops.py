

from ..entity import Entity
from ..components import Build, Food, Growing
from ..datacomponents import Interact, Loot, Remove, Serialise, Static, LootMessage
from ..template import Template

entities = {}

def cropSerializer(name):
    return (lambda obj, roomData:
        Template(name, targetTime=obj.getComponents("grow").getTargetTime())
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
            components = {}
            dataComponents = []
            if self.duration is not None:
                if targetTime is None:
                    components["grow"] = Growing(Template(nextstage), self.duration*timestep)
                else:
                    components["grow"] = Growing(Template(nextstage), targetTime=targetTime)
                dataComponents.append(Serialise(cropSerializer(name)))
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
                components=components,
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
        components={
            "item": Build(stagenames[0], flagsNeeded={"soil"}, blockingFlags={"occupied", "solid"})
        },
        dataComponents=[Static(seedname)]
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

entities["carrot"] = lambda: Entity(sprite="food", name="carrot", height=0.3, components={"item": Food(4)}, dataComponents=[Static("carrot")])


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

entities["radishes"] = lambda: Entity(sprite="food", name="radishes", height=0.3, components={"item": Food(2)}, dataComponents=[Static("radishes")])

entities["food"] = entities["radishes"]
entities["sownseed"] = entities["plantedradishseed"]
entities["youngplant"] = entities["youngradishplant"]
entities["plant"] = entities["radishplant"]
entities["seed"] = entities["radishseed"]

entities["eldritch_radish"] = lambda: Entity(sprite="food", name="eldritch radishes", height=0.3, components={"item": Food(20)}, dataComponents=[Static("eldritch_radish")])



