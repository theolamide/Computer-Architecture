"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0]*8
        self.flag = [0]*8
        self.running = True
        self.pc = 0
        self.CALL = 0b01010000
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.POP = 0b01000110
        self.PUSH = 0b01000101
        self.RET = 0b00010001
        self.ADD = 0b10100000
        self.MUL = 0b10100010
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JNE = 0b01010110
        self.JEQ = 0b01010101
        self.E = 7

    def load(self):
        """Load a program into memory."""

        address = 0
        filename = sys.argv[1]

        with open(filename) as program:
            for line in program:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                self.ram[address] = int(line, 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "CMP":
            if self.register[reg_a] == self.register[reg_b]:
                self.flag = 0b00000001
            elif self.register[reg_a] < self.register[reg_b]:
                self.flag = 0b00000100
            elif self.register[reg_a] > self.register[reg_b]:
                self.flag = 0b00000010
        else:
            raise Exception("Unsupported ALU operation")

    def halt(self):
        self.running = False

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, payload):
        self.ram[address] = payload

    def flag_check(self):
        return (self.flag == 1)

    def run(self):
        """Run the CPU."""
        IR = self.pc

        while self.running:
            instruction = self.ram[IR]

            if instruction == self.LDI:
                reg_num = self.ram[IR+1]
                value = self.ram[IR+2]
                self.register[reg_num] = value
                IR += 3

            elif instruction == self.PRN:
                reg_num = self.ram[IR+1]
                value = self.register[reg_num]
                print(value)
                IR += 2

            elif instruction == self.ADD:
                self.alu("ADD", self.ram[IR+1], self.ram[IR+2])
                IR += 3

            elif instruction == self.MUL:
                self.alu("MUL", self.ram[IR+1], self.ram[IR+2])
                IR += 3

            elif instruction == self.CMP:
                self.alu("CMP", self.ram[IR+1], self.ram[IR+2])
                IR += 3

            elif instruction == self.JMP:
                IR = self.register[self.ram_read(IR+1)]

            elif instruction == self.JNE:
                if not self.flag_check():
                    reg_num = self.ram[IR+1]
                    IR = self.register[reg_num]
                else:
                    IR += 2

            elif instruction == self.JEQ:
                if self.flag_check():
                    reg_num = self.ram[IR+1]
                    IR = self.register[reg_num]
                else:
                    IR += 2

            elif instruction == self.HLT:
                self.halt()

            else:
                print("Unknown Instruction")
                self.halt()

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         # self.fl,
    #         # self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()
