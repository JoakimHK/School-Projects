'''
Implements CPU element for Instruction Memory in MEM stage.

Code written for inf-2200, University of Tromso
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
        assert(len(outputSignalNames) == 0), 'Instruction memory should not have any control output'

        self.inputName = inputSources[0][1]
        self.outputNames = outputValueNames


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

        self.outputValues[self.outputNames[0]] = opcode
        self.outputValues[self.outputNames[1]] = rs
        self.outputValues[self.outputNames[2]] = rt
        self.outputValues[self.outputNames[3]] = rd
        self.outputValues[self.outputNames[4]] = addr
        self.outputValues[self.outputNames[5]] = funct
        self.outputValues[self.outputNames[6]] = jAddr



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
