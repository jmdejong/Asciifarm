
(defmacro send [data]
    `(fn [client] (client.send ~data)))

(defmacro input [action]
    `(send ["input" ~action]))

(defmacro doall [actions]
    `(fn [client] (for [action ~actions] (action client))))

(defmacro selector [name]
    `(.getSelector (.getDisplay client) ~name))

(defmacro selectorvalue [name]
    `(.getValue (selector ~name)))

(setv commands {
    "w" (input ["move" "north"])
    "s" (input ["move" "south"])
    "d" (input ["move" "east"])
    "a" (input ["move" "west"])
    "KEY_UP" (input ["move" "north"])
    "KEY_DOWN" (input ["move" "south"])
    "KEY_RIGHT" (input ["move" "east"])
    "KEY_LEFT" (input ["move" "west"])
    "e" (input ["take" (selectorvalue "ground")])
    "q" (input ["drop" (selectorvalue "inventory")])
    "E" (input ["use" (selectorvalue "inventory")])
    "r" (input ["interact" (selectorvalue "ground")])
    "f" (doall [
        (input ["attack"])
        (input ["attack" "north"])
        (input ["attack" "south"])
        (input ["attack" "east"])
        (input ["attack" "west"])])
    "t" (fn [client] (client.readString))
    
})
