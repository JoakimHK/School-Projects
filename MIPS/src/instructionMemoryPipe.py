'''
This version tries to implement control hazard detection, but I didn't get it to work :/
'''

from cpuElement import CPUElement
from memory import Memory
from testElement import TestElement
import unittest
import sys
from config import *

class InstructionMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'Instruction memory should have one input'
        assert(len(outputValueNames) == 7), 'Instruction memory has seven outputs'
        assert(len(control) == 0), 'Instruction memory should not have any control signal'
        assert(len(outputSignalNames) == 1), 'Instruction memory should have one control output'

        self.inputName = inputSources[0][1]
        self.outputNames = outputValueNames
        self.outputSignal = outputSignalNames[0]
        self.stallNext = 0
        self.prevWasStall = 0
        #self.timeTillBreak = 0


    def writeOutput(self):
        inputAddr = self.inputValues[self.inputName]
        instruction = self.memory[inputAddr]

        assert(isinstance(instruction, int)), 'Invalid instruction: %d' % (instruction,)

        if instruction == BREAK:
            sys.exit()

        opcode = instruction >> 26
        rs = (instruction >> 21) & FIRST_5_BITS
        rt = (instruction >> 16) & FIRST_5_BITS
        rd = (instruction >> 11) & FIRST_5_BITS
        funct = instruction & FIRST_6_BITS
        addr = instruction & FIRST_16_BITS
        jAddr = instruction & FIRST_26_BITS


        if self.stallNext > 0:
            opcode = NOP
            stallSignal = 1
            self.stallNext -= 1
            self.prevWasStall = 1

        else:
            if self.prevWasStall == 0 and (opcode == LUI or opcode == BEQ or opcode == BNE):
                stallSignal = 1
                self.stallNext = 3
                self.prevWasStall = 1

            elif self.prevWasStall == 0 and (opcode == JMP): # or opcode == LW or opcode == SW):
                stallSignal = 1
                self.prevWasStall = 1

            else:
                stallSignal = 0
                self.prevWasStall = 0

#        if instruction == BREAK:
#            opcode = NOP
#            self.stallNext = 3
#            self.prevWasStall = 1
#            self.timeTillBreak = 3
#
#        if self.timeTillBreak > 0:
#            if self.timeTillBreak == 1:
#                sys.exit()
#            self.timeTillBreak -= 1

        #print('stalls: %d ' % self.stallNext)
        #print('stallSignal: %d' % stallSignal)

        self.outputValues[self.outputNames[0]] = opcode
        self.outputValues[self.outputNames[1]] = rs
        self.outputValues[self.outputNames[2]] = rt
        self.outputValues[self.outputNames[3]] = rd
        self.outputValues[self.outputNames[4]] = addr
        self.outputValues[self.outputNames[5]] = funct
        self.outputValues[self.outputNames[6]] = jAddr

        self.outputControlSignals[self.outputSignal] = stallSignal



class TestIM(unittest.TestCase):
    def setUp(self):

        self.instructionMemory = InstructionMemory('add.mem')
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['address'],
            [],
            []
        )

        self.instructionMemory.connect(
            [(self.testInput, 'address')],
            ['opcode', 'rs', 'rt', 'rd', 'address', 'func', 'jmpAddress'],
            [],
            []
        )

        self.testOutput.connect(
            [(self.instructionMemory, 'opcode'),
            (self.instructionMemory, 'rs'),
            (self.instructionMemory, 'rt'),
            (self.instructionMemory, 'rd'),
            (self.instructionMemory, 'address'),
            (self.instructionMemory, 'func'),
            (self.instructionMemory, 'jmpAddress'),
            ],
            [],
            [],
            []
        )


    def test(self):
        self.testInput.setOutputValue('address', 0xbfc00210)

        self.instructionMemory.readInput()
        self.instructionMemory.readControlSignals()
        self.instructionMemory.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['opcode']
        self.assertEqual(output, 0)
        output = self.testOutput.inputValues['rs']
        self.assertEqual(output, 10)
        output = self.testOutput.inputValues['rt']
        self.assertEqual(output, 9)
        output = self.testOutput.inputValues['rd']
        self.assertEqual(output, 10)
        output = self.testOutput.inputValues['address']
        self.assertEqual(output, 20512)
        output = self.testOutput.inputValues['func']
        self.assertEqual(output, 32)
        output = self.testOutput.inputValues['jmpAddress']
        self.assertEqual(output, 21581856)



if __name__ == '__main__':
    unittest.main()
