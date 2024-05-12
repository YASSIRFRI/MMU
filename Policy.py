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
        self.last_allocated_index = 0
    
    def allocate(self, buffer, process):
        num_holes = len(buffer.holes)
        start_index = self.last_allocated_index
        print(start_index)
        for i in range(start_index, num_holes):
            start, end = buffer.holes[i]
            if end - start >= process.limit:
                buffer.map[(start, start + process.limit)] = process.id
                buffer.holes[i] = (start + process.limit, end)
                if end - start > process.limit:
                    self.last_allocated_index = i
                else :
                    self.last_allocated_index = (i+1)%num_holes
                return True
        for i in range(num_holes):
            start, end = buffer.holes[i]
            if end - start >= process.limit:
                buffer.map[(start, start + process.limit)] = process.id
                buffer.holes[i] = (start + process.limit, end)
                if end - start > process.limit:
                    self.last_allocated_index = i
                else :
                    self.last_allocated_index = (i+1)%num_holes
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
                if best is None or end-start < best[2]-best[1]:
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
                if worst is None or end-start > worst[2]-worst[1]:
                    worst = (i, start, end)
        if worst is None:
            return False
        i, start, end = worst
        buffer.map[(start, start+process.limit)] = process.id
        if end - start > process.limit:
            buffer.holes[i] = (start+process.limit, end)
        return True