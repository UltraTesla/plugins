class Nodes(list):
    def append(self, object, /):
        aux = object
        id = 0

        while (True):
            id += 1
            id_str = "%s - (%d)" % (object, id)

            if (super().count(aux) >= 1):
                aux = id_str

            else:
                break

        object = aux

        super().append(object)

        return object
