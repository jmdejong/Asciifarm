
import os

from .paths import keybindingsPath, charmapPath
import json


standardKeyFiles = {
    "default": os.path.join(keybindingsPath, "default.json"),
    "azerty": os.path.join(keybindingsPath, "azerty.json")
}

def loadKeybindings(name):
    fname = None
    if name in standardKeyFiles:
        fname = standardKeyFiles[name]
    else:
        fname = name
    with open(fname) as f:
        data = json.load(f)
    bindings = {}
    help = ""
    for ftemplate in data.get("templates", []):
        if ftemplate.partition(os.sep)[0] in {".", ".."}:
            ftemplate = os.path.relpath(ftemplate, fname)
        template = loadKeybindings(ftemplate)
        bindings.update(template.get("actions", {}))
        help = template.get("help", help)
    bindings.update(data.get("actions", {}))
    help = data.get("help", help)
    return {"actions": bindings, "help": help}


standardCharFiles = {name: os.path.join(charmapPath, file) for name, file in {
    "default": "halfwidth.json",
    "halfwidth": "halfwidth.json",
    "hw": "halfwidth.json",
    "fullwidth": "fullwidth.json",
    "fw": "fullwidth.json",
    "emoji": "emoji.json"
}.items()}

def loadCharmap(name):
    fname = None
    if name in standardCharFiles:
        fname = standardCharFiles[name]
    else:
        fname = name
    with open(fname) as f:
        data = json.load(f)
    
    templates = []
    for ftemplate in data.get("templates", []):
        if ftemplate.partition(os.sep)[0] in {".", ".."}:
            ftemplate = os.path.relpath(ftemplate, fname)
        templates.append(loadCharmap(ftemplate))
    
    templates.append(data)
    
    mapping = {}
    writable = {}
    default = None
    charwidth = 1
    healthfull = None
    healthempty = None
    alphabet = ""
    msgcolours = {}
    
    for template in templates:
        mapping.update(template.get("mapping", {}))
        writable.update(template.get("writable", {}))
        default = template.get("default", default)
        charwidth = template.get("charwidth", charwidth)
        healthfull = template.get("healthfull", healthfull)
        healthempty = template.get("healthempty", healthempty)
        alphabet = template.get("alphabet", alphabet)
        msgcolours.update(template.get("msgcolours", {}))
    return {
        "mapping": mapping,
        "writable": writable,
        "default": default,
        "charwidth": charwidth,
        "healthfull": healthfull,
        "healthempty": healthempty,
        "alphabet": alphabet,
        "msgcolours": msgcolours
    }
