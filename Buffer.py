class Buffer:
    def __init__(self, size):
        self.size = size
        #maps a tuple of (start, end) to a process id
        self.map={}
        
    
    
    def is_free(self, start, end):
        """Returns True if the range is free, False otherwise."""
        for e in self.map:
            if start >= e[0] and end <= e[1]:
                return False
        return True
    
    def get(self,process_id):
        for e in self.map:
            if self.map[e] == process_id:
                return e
        return None