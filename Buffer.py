class Buffer:
    def __init__(self, size):
        self.size = size
        # Map of allocated memory ranges to process ids
        #e.g {1: (0, 10), 2: (10, 20), 3: (30, 40)}
        self.map={}
        self.holes = [(0, size)]
        self.pointer = 0
    
    def is_free(self, start, end):
        """Returns True if the range is free, False otherwise."""
        for e in self.map:
            if  start<= e[0] < end or start < e[1] <= end:
                return False
        return True
    
    def get(self,process_id):
        for e in self.map:
            if self.map[e] == process_id:
                return e
        return None
    
    def compactHoles(self):
        self.holes = sorted(self.holes, key=lambda x: x[0])
        i = 0
        while i < len(self.holes) - 1:
            if self.holes[i][1] == self.holes[i+1][0]:
                self.holes[i] = (self.holes[i][0], self.holes[i+1][1])
                del self.holes[i+1]
            else:
                i += 1
               
                
    def free(self, process_id):
        hole = self.get(process_id)
        for i, h in enumerate(self.holes):
            if h[0]>hole[0]:
                self.holes.insert(i, hole)
                break
        self.compactHoles()
        del self.map[hole]
        
    def flush(self):
        memory_file=open("memory.txt","w")
        output_buffer = [" " for _ in range(self.size*32)]
        print(self.map)
        for e in self.map:
            procees_name="@@@@@@Process "+str(self.map[e])+"@@@@"
            for i in range(32-len(procees_name)):
                procees_name+="@"
            output_buffer[e[0]*32:e[0]*32+32] = procees_name
            for i in range(e[0]+1, e[1]):
                for j in range(32):
                    output_buffer[i*32+j] = "*"
        for i in range(self.size):
            memory_file.write("".join(output_buffer[i*32:(i+1)*32]) + "\n")
        memory_file.close()