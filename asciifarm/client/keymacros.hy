
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
