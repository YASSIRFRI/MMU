

class MMU:
    def __init__(self, buffer, management_policy):
        self.buffer = buffer
        self.process_map = {}
        self.management_policy = management_policy

    def add_process(self, process):
        self.process_map[process.id] = process

    def load(self, process_id):
        process = self.process_map[process_id]
        self.management_policy.allocate(self.buffer, process)
        
    
    def convert(self, process_id, logical_address):
        process = self.process_map[process_id]
        if logical_address < process.limit:
            return process.base + logical_address
        return -1
    
    def delete(self, process_id):
        del self.process_map[process_id]