

(require [asciifarm.client.keymacros [*]])

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
  "v" (fn [client] (.select (selector "inventory") 1 True True))
  "c" (fn [client] (.select (selector "ground") 1 True True))
;;   "x" (fn [client] (.select (selector "equipment") 1 True True))
  "f" (doall [
        (input ["attack"])
        (input ["attack" "north"])
        (input ["attack" "south"])
        (input ["attack" "east"])
        (input ["attack" "west"])])
  "t" (fn [client] (client.readString)) })
