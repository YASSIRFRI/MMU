class Buffer:
    class Hole:
        def __init__(self, start, end):
            self.start = start
            self.end = end
            self.next = None

    def __init__(self, size):
        self.size = size
        # Map of allocated memory ranges to process ids
        # e.g {1: (0, 10), 2: (10, 20), 3: (30, 40)}
        self.map = {}
        self.holes = self.Hole(0, size)
        self.pointer = 0

    def is_free(self, start, end):
        """Returns True if the range is free, False otherwise."""
        current = self.holes
        while current:
            if current.start <= start < current.end or start < current.start < end:
                return False
            current = current.next
        return True

    def get(self, process_id):
        for e in self.map:
            if self.map[e] == process_id:
                return e
        return None

    def compactHoles(self):
        current = self.holes
        while current.next:
            if current.end == current.next.start:
                current.end = current.next.end
                current.next = current.next.next
            else:
                current = current.next
        return

    def free(self, process_id):
        hole = self.get(process_id)
        current = self.holes
        if hole[0] < current.start:
            new_hole = self.Hole(hole[0], hole[1])
            new_hole.next = self.holes
            self.holes = new_hole
        else:
            while current.next and current.next.start < hole[0]:
                current = current.next
            new_hole = self.Hole(hole[0], hole[1])
            new_hole.next = current.next
            current.next = new_hole
        self.compactHoles()
        del self.map[hole]

    def flush(self):
        memory_file = open("memory.txt", "w")
        output_buffer = [" " for _ in range(self.size * 32)]
        map2 = {}
        for key, value in self.map.items():
            newkey = (key[0], key[1] - key[0])
            map2[newkey] = value
        print(map2)
        for e in self.map:
            procees_name = "@@@@@@Process " + str(self.map[e]) + "@@@@"
            for i in range(32 - len(procees_name)):
                procees_name += "@"
            output_buffer[e[0] * 32:e[0] * 32 + 32] = procees_name
            for i in range(e[0] + 1, e[1]):
                for j in range(32):
                    output_buffer[i * 32 + j] = "*"
        for i in range(self.size):
            memory_file.write("".join(output_buffer[i * 32:(i + 1) * 32]) + "\n")
        memory_file.close()
