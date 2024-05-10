import sys
from Buffer import Buffer
from MMU import MMU
from Policy import FirstFit, NextFit, BestFit, WorstFit
from Process import Process


if len(sys.argv) != 3:
    print("Usage: python main.py TOTAL_MEMORY MANAGEMENT_POLICY")
    sys.exit(1)

total_memory = int(sys.argv[1])
management_policy = sys.argv[2]  
if management_policy == '1':
    management_policy = FirstFit()
elif management_policy == '2':
    management_policy = NextFit()
elif management_policy == '3':
    management_policy = BestFit()
elif management_policy == '4':
    management_policy = WorstFit()
else:
    print('Invalid management policy')
    sys.exit(1)
buffer = Buffer(total_memory)
mmu = MMU(buffer, management_policy)  # Replace ManagementPolicy() with your actual policy based on management_policy
process_id_counter = 1

while True:
    command = input('> ').split()
    if command[0] == 'cr':
        size = int(command[1])
        process = Process(process_id_counter, None, 0, size)
        if mmu.management_policy.allocate(mmu.buffer, process):
            process.base, process.limit = mmu.buffer.get(process.id)
            mmu.add_process(process)
            print(f'Process {process.id} created with base {process.base} and limit {process.limit}')
            process_id_counter += 1
        else:
            print('Error: Not enough memory')
    elif command[0] == 'dl':
        process_id = int(command[1])
        if process_id in mmu.process_map:
            process = mmu.process_map[process_id]
            mmu.buffer.size += process.size
            del mmu.process_map[process_id]
            print(f'Process {process_id} deleted')
        else:
            print('Error: No such process')
    elif command[0] == 'cv':
        process_id = int(command[1])
        virtual_address = int(command[2])
        if process_id in mmu.process_map:
            process = mmu.process_map[process_id]
            if process.base <= virtual_address < process.limit:
                print(f'Physical address: {virtual_address - process.base}')
            else:
                print('Error: Address outside process address space')
        else:
            print('Error: No such process')
    elif command[0] == 'pm':
        for process in mmu.process_map.values():
            print(f'Process {process.id}: base {process.base}, limit {process.limit}')
        print(f'Free memory: {mmu.buffer.size}')