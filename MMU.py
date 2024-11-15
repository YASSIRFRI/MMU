import sys
from Buffer import Buffer
from MemoryManager import MMU
from Policy import FirstFit, NextFit, BestFit, WorstFit
from Process import Process

def display_help():
    print("""
    Help:
    cr <size>: Create a new process with the specified size.
    dl <process_id>: Delete the process with the given ID.
    cv <process_id> <virtual_address>: Convert virtual address to physical address.
    pm: Print memory map.
    exit: Exit the application.
    """)

if len(sys.argv) != 3:
    print("Invalid Format (Usage: python MMU.py TOTAL_MEMORY MANAGEMENT_POLICY)")
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
mmu = MMU(buffer, management_policy)  
process_id_counter = 1

while True:
    command = input('> ').split()
    if command[0] == '-h':
        display_help()
    elif command[0] == 'cr':
        size = int(command[1])
        process = Process(process_id_counter, None, 0, size)
        if mmu.management_policy.allocate(mmu.buffer, process):
            process.base, process.limit = mmu.buffer.get(process.id)
            mmu.add_process(process)
            print(f'Process {process.id} created with base {process.base} and limit {size}')
            process_id_counter += 1
        else:
            print('Error: Not enough memory')
    elif command[0] == 'dl':
        process_id = int(command[1])
        if process_id in mmu.process_map:
            mmu.delete(process_id)
            print(f'Process {process_id} deleted')
        else:
            print('Error: No such process')
    elif command[0] == 'cv':
        process_id = int(command[1])
        virtual_address = int(command[2])
        if process_id in mmu.process_map:
            process = mmu.process_map[process_id]
            if 0 < virtual_address <= process.limit - process.base :
                print(f'Physical address: {virtual_address + process.base}')
            else:
                print('Error: Address outside process address space')
        else:
            print('Error: No such process')
    elif command[0] == 'pm':
        mmu.buffer.flush()
    elif command[0] == 'exit':
        print("Exiting the application...")
        sys.exit(1)
    else:
        print("Invalid command. Use '-h' for help.")
