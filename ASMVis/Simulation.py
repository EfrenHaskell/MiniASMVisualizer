from collections import defaultdict
import Grammar as grm
import Visualizer as v

'''
Author: Efren Haskell
Last Update: 4/8/2024
Simulation class handles simulation of CPU and ASM semantic parsing
'''

class Simulation:

    def __init__(self):
        """The Simulation Constructor initializes the below variables:
            - history: stores all register, menu and disk values for every visualizer state
            - base_cache: stores all initialized presets
            - label_map: maps label name to line number
            - operation_log: stores a log of skeletons produced during first parse of MiniASM program
            - index_log: keeps track of prior indexes
            - curr_line: currently unused
            - cache_log: stores a log of all operations performed by MiniASM program
        """
        self.history = {
            "registers": defaultdict(str),
            "memory": defaultdict(str),
            "disk": defaultdict(str)
        }
        self.base_cache = {
            "memory": defaultdict(str),
            "disk": defaultdict(str)
        }
        self.label_map: defaultdict(str) = defaultdict()
        self.operation_log = [] # for storing skeletons
        self.index_log = [0]
        self.curr_line = 0
        self.cache_log = []

    def set_base(self, location: str, address: str, data: str):
        """Adds new preset to history and base cache"""
        self.history[location][address] = data
        self.base_cache[location][address] = data


    def remove_base(self, location: str, address: str):
        """Removes preset from history and base cache if it exists"""
        if address in self.history[location]:
            self.history[location].pop(address)
            self.base_cache[location].pop(address)


    def instruction_handle(self, instruction: str, tokens: list[str], types: list[str], offset: int):
        """skeleton encoder for instructions
        Instruction skeleton takes form: (instruction, address_mode, destination, source, destination value, source value)
        """
        address_mode = "direct"
        source = tokens[3 + offset]
        source_type = types[3 + offset]
        destination = tokens[1 + offset]
        if source in grm.address_modes:
            address_mode = grm.address_modes[source]
            source = tokens[4 + offset]
            source_type = types[4 + offset]
            if address_mode == "index":
                source = (source, tokens[6] + offset)
        if instruction == "load" or instruction == "store":
            source_loc = "memory"
        else:
            source_loc = "disk"
        if source_type == "reg" and address_mode != "relative":
            source_loc = "registers"
        if instruction == "load" or instruction == "read":
            return (instruction, address_mode, "registers", source_loc, destination, source)
        else:
            return (instruction, address_mode, source_loc, "registers", source, destination)


    def label_handle(self, instruction: str, tokens: list[str], types: list[str], line_index):
        """skeleton encoder for labels"""
        self.label_map[tokens[0]] = line_index
        self.encode_skel(tokens, types, line_index+1, offset=1)


    def encode_skel(self, tokens: list[str], types: list[str], line_index: int, offset: int = 0):
        """handles control flow for skeleton encoding creation"""
        token_count: int = len(tokens)
        first_type: str = types[0+offset]
        if first_type in grm.instructions:
            self.operation_log.append(self.instruction_handle(first_type, tokens, types, offset))
        elif first_type == "label":
            self.label_handle(first_type, tokens, types, line_index-1)
        elif first_type == "arithmetic":
            self.operation_log.append((tokens[offset], tokens[1+offset], tokens[3+offset]))
        elif first_type == "branch":
            self.operation_log.append((tokens[offset], tokens[1+offset], tokens[3+offset], tokens[5+offset]))
        elif first_type == "br":
            self.operation_log.append((first_type, tokens[1+offset]))
        elif first_type == "inc":
            self.operation_log.append((first_type, tokens[1+offset]))
        else:
            self.operation_log.append((first_type, None))


    def make_log_string(self, index) -> list[str]:
        """String list conversion for operation log encodings"""
        log = self.operation_log[index]
        log_string = f"Instruction: {log[0]}"
        if log[0] in grm.instructions:
            return [log_string, f"Addressing Mode: {log[1]}", f"Bus Motion: {log[3]} -> {log[2]}"]
        elif log[0] in grm.branches:
            return [log_string, f"Expression: if {log[1]} {grm.branches[log[0]]} {log[2]} -> goto({log[3]})"]
        elif log[0] in grm.arithmetic:
            return [log_string, f"Expression: {log[1]} {grm.arithmetic[log[0]]} {log[2]}"]
        elif log[0] == "br":
            return [log_string, f"Expression: goto({log[1]})"]
        elif log[0] == "inc":
            return [log_string, f"Expression: {log[1]}++"]
        else:
            return [log_string, ""]


    def revert_step(self, index):
        """Reverts a visualizer step by undoing last action in cache_log
        Returns previous index
        """
        cache_val = self.cache_log[index]
        instruction = self.operation_log[index][0]
        if cache_val != None:
            if instruction in grm.instructions:
                if cache_val[2] in self.history[cache_val[1]]:
                    self.history[cache_val[1]].pop(cache_val[2])
            else:
                self.history[cache_val[1]][cache_val[2]] = cache_val[0]
        if len(self.index_log) > 1:
            self.index_log.pop()
        return self.index_log[-1]


    def simulate_step(self, index) -> int:
        """Changes history values based on MiniASM operation
        Keeps track of state changes in cache_log
        """
        skeleton = self.operation_log[index]
        instruction = skeleton[0]
        if instruction in grm.instructions:
            val: str = skeleton[4]
            address_mode: str = skeleton[1]
            changed_val: str = skeleton[4]
            if address_mode == "direct":
                self.history[skeleton[2]][skeleton[4]] = self.history[skeleton[3]][skeleton[5]]
            elif address_mode == "immediate":
                self.history[skeleton[2]][skeleton[4]] = skeleton[5]
            elif address_mode == "index":
                if instruction == "load" or instruction == "read":
                    self.history[skeleton[2]][skeleton[4]] = self.history[skeleton[3]][str(int(skeleton[5][0]) + int(skeleton[5][1]))]
                else:
                    changed_val = str(int(skeleton[4][0]) + int(skeleton[4][1]))
                    self.history[skeleton[2]][str(int(skeleton[4][0]) + int(skeleton[4][1]))] = self.history[skeleton[3]][skeleton[5]]
            elif address_mode == "relative":
                if instruction == "load":
                    relative_address = skeleton[5]
                    val = "x"
                    if grm.get_type(relative_address) == "reg":
                        relative_address = self.history["registers"][relative_address]
                    num_val = int(relative_address) + 4 * index
                    if num_val > 0:
                        val += " + " + num_val
                    changed_val = val
                    self.history[skeleton[2]][skeleton[4]] = self.history[skeleton[3]][val]
                else:
                    relative_address = skeleton[4]
                    val = "x"
                    if grm.get_type(relative_address) == "reg":
                        relative_address = self.history["registers"][relative_address]
                    num_val = int(relative_address) + 4 * index
                    if num_val > 0:
                        val += "+" + str(num_val)
                    changed_val = val
                    self.history[skeleton[2]][val] = self.history["registers"][skeleton[5]]
            else:
                self.history[skeleton[2]][val] = self.history["memory"][self.history[skeleton[3]][skeleton[5]]]
            if len(self.cache_log) <= index:
                self.cache_log.append((self.history[skeleton[2]][val], skeleton[2], changed_val))
        elif instruction in grm.branches:
            branch_type = instruction
            goto = self.label_map[skeleton[3]+":"]
            if len(self.cache_log) <= index:
                self.cache_log.append(None)
            if branch_type == "blt" and skeleton[1] < skeleton[2] or branch_type == "bgt" and skeleton[1] > skeleton[2] or branch_type == "bleq" and skeleton[1] <= skeleton[2] or branch_type == "bgeq" and skeleton[1] >= skeleton[2]:
                return goto
        elif instruction == "br":
            if len(self.cache_log) <= index:
                self.cache_log.append(None)
            return self.label_map[skeleton[1]+":"]
        elif instruction in grm.arithmetic:
            change_val: str = self.history["registers"][skeleton[1]]
            if instruction == "add":
                self.history["registers"][skeleton[1]] = str(int(self.history["registers"][skeleton[1]]) + int(self.history["registers"][skeleton[2]]))
            elif instruction == "sub":
                self.history["registers"][skeleton[1]] = str(int(self.history["registers"][skeleton[1]]) - int(self.history["registers"][skeleton[2]]))
            elif instruction == "div":
                self.history["registers"][skeleton[1]] = str(int(self.history["registers"][skeleton[1]]) / int(self.history["registers"][skeleton[2]]))
            elif instruction == "mul":
                self.history["registers"][skeleton[1]] = str(int(self.history["registers"][skeleton[1]]) * int(self.history["registers"][skeleton[2]]))
            if len(self.cache_log) <= index:
                self.cache_log.append((change_val, "registers", skeleton[1]))
        elif instruction == "inc":
            if len(self.cache_log) <= index:
                self.cache_log.append((self.history["registers"][skeleton[1]], "registers", skeleton[1]))
            self.history["registers"][skeleton[1]] = str(int(self.history["registers"][skeleton[1]]) + 1)
        else:
            if len(self.cache_log) <= index:
                self.cache_log.append(None)
        return index+1


    def log_index(self, index: int):
        """Manual index logger for accurate determination of previous steps"""
        if self.index_log[-1] != index:
            self.index_log.append(index)
