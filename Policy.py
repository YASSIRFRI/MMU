class Policy:
    """Abstract class for management policies"""
    def allocate(self, buffer, process):
        raise NotImplementedError("Subclasses must implement abstract method")


class FirstFit(Policy):
    def allocate(self, buffer, process):
        current_hole = buffer.holes
        while current_hole:
            start, end = current_hole.start, current_hole.end
            if end - start >= process.limit:
                buffer.map[(start, start + process.limit)] = process.id
                current_hole.start = start + process.limit
                buffer.compactHoles()
                return True
            current_hole = current_hole.next
        return False


class NextFit(Policy):
    def __init__(self):
        self.last_allocated_hole = None

    def allocate(self, buffer, process):
        start_hole = self.last_allocated_hole if self.last_allocated_hole else buffer.holes
        current_hole = start_hole
        while current_hole:
            start, end = current_hole.start, current_hole.end
            if end - start >= process.limit:
                buffer.map[(start, start + process.limit)] = process.id
                current_hole.start = start + process.limit
                buffer.compactHoles()
                self.last_allocated_hole = current_hole
                return True
            current_hole = current_hole.next
            if current_hole == start_hole:
                break
        start_hole = buffer.holes
        while start_hole != current_hole:
            start, end = start_hole.start, start_hole.end
            if end - start >= process.limit:
                buffer.map[(start, start + process.limit)] = process.id
                start_hole.start = start + process.limit
                buffer.compactHoles()
                self.last_allocated_hole = start_hole
                return True
            start_hole = start_hole.next
        return False


class BestFit(Policy):
    def allocate(self, buffer, process):
        best_hole = None
        current_hole = buffer.holes
        while current_hole:
            start, end = current_hole.start, current_hole.end
            if end - start >= process.limit:
                if best_hole is None or (end - start) < (best_hole.end - best_hole.start):
                    best_hole = current_hole
            current_hole = current_hole.next

        if best_hole:
            start, end = best_hole.start, best_hole.end
            buffer.map[(start, start + process.limit)] = process.id
            best_hole.start = start + process.limit
            buffer.compactHoles()
            return True
        return False


class WorstFit(Policy):
    def allocate(self, buffer, process):
        worst_hole = None
        current_hole = buffer.holes
        while current_hole:
            start, end = current_hole.start, current_hole.end
            if end - start >= process.limit:
                if worst_hole is None or (end - start) > (worst_hole.end - worst_hole.start):
                    worst_hole = current_hole
            current_hole = current_hole.next

        if worst_hole:
            start, end = worst_hole.start, worst_hole.end
            buffer.map[(start, start + process.limit)] = process.id
            worst_hole.start = start + process.limit
            buffer.compactHoles()
            return True
        return False
