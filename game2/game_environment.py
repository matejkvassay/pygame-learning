class GameEnvironment:
    def __init__(self):
        self.obj_buffer = dict()

    def __iter__(self):
        return self.obj_buffer.copy().values().__iter__()

    def add(self, obj):
        obj_id = id(obj)
        self.obj_buffer[obj_id] = obj
        return obj_id

    def remove(self, obj):
        obj_id = id(obj)
        del self.obj_buffer[obj_id]
