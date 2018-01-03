
import curses

prenamed = {
    10: "NEWLINE"
}

def nameFromKey(key):
    if key in prenamed:
        return prenamed[key]
    return str(curses.keyname(key), "utf-8")
