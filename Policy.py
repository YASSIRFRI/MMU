class Policy:
    """Abstract class for management policies"""
    def allocate(self, start, end):
        raise NotImplementedError("Subclasses must implement abstract method")
    
    




class FirstFit(Policy):
    def __init__(self):
        pass
    def allocate(self, buffer, process):
        for i, hole in enumerate(buffer.holes):
            start, end = hole
            if end - start >= process.limit:
                buffer.map[(start, start+process.limit)] = process.id
                buffer.holes[i] = (start+process.limit, end)
                return True
        return False
    
class NextFit(Policy):
    def __init__(self):
        self.last_allocation = 0
        self.last_hole = 0
    def allocate(self, buffer, process):
        for i, hole in enumerate(buffer.holes):
            start, end = hole
            if end - start >= process.limit and i >= self.last_hole:
                buffer.map[(start, start+process.limit)] = process.id
                buffer.holes[i] = (start+process.limit, end)
                buffer.pointer = start+process.limit
                last_hole = i
                return True
        return False

class BestFit(Policy):
    def __init__(self):
        pass
    def allocate(self, buffer, process):
        best = None
        for i, hole in enumerate(buffer.holes):
            start, end = hole
            if end - start >= process.limit:
                if best is None or end-start < best[1]-best[0]:
                    best = (i, start, end)
        if best is None:
            return False
        i, start, end = best
        buffer.map[(start, start+process.limit)] = process.id
        buffer.holes[i] = (start+process.limit, end)
        return True
    
class WorstFit(Policy):
    def __init__(self):
        pass
    
    def allocate(self, buffer, process):
        worst = None
        for i, hole in enumerate(buffer.holes):
            start, end = hole
            if end - start >= process.limit:
                if worst is None or end-start > worst[1]-worst[0]:
                    worst = (i, start, end)
        if worst is None:
            return False
        i, start, end = worst
        buffer.map[(start, start+process.limit)] = process.id
        if end - start > process.limit:
            buffer.holes[i] = (start+process.limit, end)
        return True