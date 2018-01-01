

;; mainly intended as example for using different keybindings
"k" (input ["move" "north"])
"j" (input ["move" "south"])
"l" (input ["move" "east"])
"h" (input ["move" "west"])
"KEY_UP" (input ["move" "north"])
"KEY_DOWN" (input ["move" "south"])
"KEY_RIGHT" (input ["move" "east"])
"KEY_LEFT" (input ["move" "west"])
"g" (input ["take" (selectorvalue "ground")])
"q" (input ["drop" (selectorvalue "inventory")])
"E" (input ["use" (selectorvalue "inventory")])
"r" (input ["interact" (selectorvalue "ground")])
"v" (fn [client] (.select (selector "inventory") 1 True True))
"c" (fn [client] (.select (selector "ground") 1 True True))
"x" (fn [client] (.select (selector "equipment") 1 True True))
"z" (input ["unequip" (selectorvalue "equipment")])
"f" (doall [
    (input ["attack"])
    (input ["attack" "north"])
    (input ["attack" "south"])
    (input ["attack" "east"])
    (input ["attack" "west"])])
"t" (fn [client] (client.readString))
"help" "\
Controls:
 wasd or arrows:
    Move around
 e: Grab
 q: Drop
 E: Use
 r: Interact
 f: Attack
 t: Chat
 z: Unequip
 xcv: scroll"

