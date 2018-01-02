
(require [asciifarm.client.keymacros [*]])

(defmacro eval-in-context [code] 
    `(
        (eval `(do
            (require [asciifarm.client.keymacros [*]])
            (fn [client display connection]
                ~~code)))
        self.client
        self.display
        self.connection))

(defmacro sendinput [message] `(
    self.client.send ["input" ~message]))

(defclass InputHandler []
    
    (defn --init-- [self client display connection]
          (setv self.client client)
          (setv self.display display)
          (setv self.connection connection)
          (setv self.commands None))
    
    (defn readCommands [self commandsstring]
        (setv self.commands
            (dict-comp 
                (eval key)
                (
                    (eval `(do
                        (require [asciifarm.client.keymacros [*]])
                        (fn [handler]
                            (fn [] ~value))))
                    self)
                [[key value] (.items (read-str commandsstring))])))
    
    (defn runCommand [self commandstring]
          (eval (read-str (+ "(" commandstring ")"))))
    
    (defn parseMessage [self message]
        (if message
            (if (= (first message) "/")
                (do
                    (setv msg (.join "" (drop 1 message)))
                    (if (= (first msg) "/")
                        (inp ["say" msg])
                        (self.runCommand msg)))
                (inp ["say" message]))))
    
    (defn getDocs [self]
          (if (in "help" self.commands) ((get self.commands "help")) ""))
    
    (defn onKey [self key]
          (if (in key self.commands) ((get self.commands key))))
)
