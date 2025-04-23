class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.program_counter = 0
        self.memory = {}
        self.running = True
        