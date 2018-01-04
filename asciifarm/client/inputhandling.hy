
(require [asciifarm.client.keymacros [*]])
(import [asciifarm.client.keynames [nameFromKey]])

(defclass InputHandler []
    
    (defn --init-- [self client display connection]
          (setv self.client client)
          (setv self.display display)
          (setv self.connection connection)
          (setv self.commands None))
    
    (defn readCommands [self commandsstring]
        (setv self.commands
            (dict-comp 
                (str key)
                (
                    (eval `(do
                        (require [asciifarm.client.keymacros [*]])
                        (fn [handler]
                            (fn [] ~value))))
                    self)
                [[key value] (.items (read-str commandsstring))])))
    
    (defn runCommand [self commandstring]
          (try 
              (eval (read-str (+ "(" commandstring ")")))
              (except [e Exception]
                    (self.client.log (repr e)))))
    
    (defn parseMessage [self message]
        (if message
            (if (= (first message) "/")
                (do
                    (setv msg (.join "" (drop 1 message)))
                    (if (= (first msg) "/")
                        (send ["chat" msg])
                        (self.runCommand msg)))
                (send ["chat" message]))))
    
    (defn getDocs [self]
          (if (in "help" self.commands) ((get self.commands "help")) ""))
    
    (defn onKey [self key] (do
        (setv keyname (nameFromKey key))
        (if (in keyname self.commands) ((get self.commands keyname)))))
)
