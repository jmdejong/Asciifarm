
import curses

prenamed = {
    10: "NEWLINE"
}

def nameFromKey(key):
    if key in prenamed:
        return prenamed[key]
    try:
        keyname = curses.keyname(key)
    except ValueError:
        return None
    return str(keyname, "utf-8")
