class Process:
    def __init__(self, id, parent, base, limit):
        self.id = id
        self.parent = parent
        self.base = base
        self.limit = limit