
import os

from .paths import keybindingsPath
import json


standardKeyFiles = {
    "default": os.path.join(keybindingsPath, "keybindings.json"),
    "azerty": os.path.join(keybindingsPath, "azerty.json")
}

def loadKeybindings(name):
    fname = None
    if name in standardKeyFiles:
        fname = standardKeyFiles[name])
    else:
        fname = name
    with open(fname) as f:
        data = json.load(f)
    bindings = {}
    for template in data.get(templates, []):
        if template.partition(os.sep)[0] in {".", ".."}:
            template = os.path.relpath(template, fname)
        bindings.update(loadKeybindings(template))
    bindings.update(data["actions"])
    return (bindings, data["help"])


def loadCharmap(name):
    fname = None
    if name in standardKeyFiles:
        fname = standardKeyFiles[name])
    else:
        fname = name
    with open(fname) as f:
        data = json.load(f)
    bindings = {}
    for template in data.get(templates, []):
        if template.partition(os.sep)[0] in {".", ".."}:
            template = os.path.relpath(template, fname)
        bindings.update(loadKeybindings(template))
    bindings.update(data["actions"])
    return (bindings, data["help"])
