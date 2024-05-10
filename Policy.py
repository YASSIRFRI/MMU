class Policy:
    """Abstract class for management policies"""
    def allocate(self, start, end):
        raise NotImplementedError("Subclasses must implement abstract method")
    
    




class FirstFit(Policy):
    def __init__(self):
        pass
    def allocate(self, buffer, process):
        for e in buffer.map:
            if buffer.map[e] == process.id:
                return True
        start=0
        while start < buffer.size:
            end = start + process.limit
            if buffer.is_free(start, end):
                buffer.map[(start, end)] = process.id
                return True
            else:
                start = end+1
        raise Exception("No free space available")
    
    
class NextFit(Policy):
    def __init__(self):
        self.last_allocation = 0
    def allocate(self, buffer, process):
        for e in buffer.map:
            if buffer.map[e] == process.id:
                return
        start = self.last_allocation
        while start < buffer.size:
            end = start + process.limit
            if buffer.is_free(start, end):
                buffer.map[(start, end)] = process.id
                self.last_allocation = end
                return
            else:
                start = end+1
        start = 0
        while start < self.last_allocation:
            end = start + process.limit
            if buffer.is_free(start, end):
                buffer.map[(start, end)] = process.id
                self.last_allocation = end
                return
            else:
                start = end+1
        raise Exception("No free space available")


class BestFit(Policy):
    def __init__(self):
        pass
    def allocate(self, buffer, process):
        for e in buffer.map:
            if buffer.map[e] == process.id:
                return
        best_start = 0
        best_size = buffer.size
        start = 0
        while start < buffer.size:
            end = start + process.limit
            if buffer.is_free(start, end):
                if end - start < best_size:
                    best_start = start
                    best_size = end - start
            start = end+1
        if best_size == buffer.size:
            raise Exception("No free space available")
        buffer.map[(best_start, best_start+best_size)] = process.id
        return
    
class WorstFit(Policy):
    def __init__(self):
        pass
    def allocate(self, buffer, process):
        for e in buffer.map:
            if buffer.map[e] == process.id:
                return
        worst_start = 0
        worst_size = 0
        start = 0
        while start < buffer.size:
            end = start + process.limit
            if buffer.is_free(start, end):
                if end - start > worst_size:
                    worst_start = start
                    worst_size = end - start
            start = end+1
        if worst_size == 0:
            raise Exception("No free space available")
        buffer.map[(worst_start, worst_start+worst_size)] = process.id
        return
