import unittest
from config import *
from cpuElement import CPUElement
from testElement import TestElement


class ControlUnit(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'Control unit should have two inputs'
        assert(len(outputValueNames) == 0), 'Control unit has no output'
        assert(len(control) == 0), 'Control unit has no control signal'
        assert(len(outputSignalNames) == 11), 'Control unit has 10 control outputs'

        self.outputNames = outputSignalNames

    def writeOutput(self):
        opcode = self.inputValues[self.inputSources[0][1]]
        funct = self.inputValues[self.inputSources[1][1]]

        #print('opcode: %d' % opcode)


        RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch, BranchNE, Jump, LoadImm, ALUOp = 0,0,0,0,0,0,0,0,0,0,0


        if opcode == R_TYPE:
            RegDst = 1
            RegWrite = 1

            if funct == ADD:
                ALUOp = ALU_ADD
            elif funct == ADDU:
                ALUOp = ALU_ADDU
            elif funct == SUB:
                ALUOp = ALU_SUB
            elif funct == SUBU:
                ALUOp = ALU_SUB
            elif funct == AND:
                ALUOp = ALU_AND
            elif funct == OR:
                ALUOp = ALU_OR
            elif funct == NOR:
                ALUOp = ALU_NOR
            elif funct == SLT:
                ALUOp = ALU_SLT

        elif opcode == LW:
            ALUSrc = 1
            MemtoReg = 1
            RegWrite = 1
            MemRead = 1
            ALUOp = ALU_ADD

        elif opcode == SW:
            ALUSrc = 1
            MemWrite = 1
            ALUOp = ALU_ADD

        elif opcode == BEQ:
            Branch = 1
            ALUOp = ALU_SUB

        elif opcode == BNE:
            BranchNE = 1
            ALUOp = ALU_SUB

        elif opcode == JMP:
            Jump = 1

        elif opcode == LUI:
            RegWrite = 1
            LoadImm = 1

        elif opcode == ADDI:
            ALUSrc = 1
            RegWrite = 1
            ALUOp = ALU_ADD

        elif opcode == ADDIU:
            ALUSrc = 1
            RegWrite = 1
            ALUOp = ALU_ADDU

        elif opcode == NOP:
            print('nop')


        self.outputControlSignals[self.outputNames[0]] = RegDst
        self.outputControlSignals[self.outputNames[1]] = ALUSrc
        self.outputControlSignals[self.outputNames[2]] = MemtoReg
        self.outputControlSignals[self.outputNames[3]] = RegWrite
        self.outputControlSignals[self.outputNames[4]] = MemRead
        self.outputControlSignals[self.outputNames[5]] = MemWrite
        self.outputControlSignals[self.outputNames[6]] = Branch
        self.outputControlSignals[self.outputNames[7]] = BranchNE
        self.outputControlSignals[self.outputNames[8]] = Jump
        self.outputControlSignals[self.outputNames[9]] = LoadImm
        self.outputControlSignals[self.outputNames[10]] = ALUOp





class TestControlUnit(unittest.TestCase):
    def setUp(self):
        self.controlUnit = ControlUnit()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['controlInput', 'func'],
        [],
        []
        )

        self.controlUnit.connect(
        [(self.testInput, 'controlInput'), (self.testInput, 'func')],
        [],
        [],
        ['RegDst', 'ALUSrc', 'MemtoReg', 'RegWrite', 'MemRead', 'MemWrite', 'Branch', 'BranchNE', 'Jump', 'LoadImm', 'ALUOp']
        )

        self.testOutput.connect(
        [],
        [],
        [(self.controlUnit, 'RegDst'),
        (self.controlUnit, 'ALUSrc'),
        (self.controlUnit, 'MemtoReg'),
        (self.controlUnit, 'RegWrite'),
        (self.controlUnit, 'MemRead'),
        (self.controlUnit, 'MemWrite'),
        (self.controlUnit, 'Branch'),
        (self.controlUnit, 'BranchNE'),
        (self.controlUnit, 'Jump'),
        (self.controlUnit, 'LoadImm'),
        (self.controlUnit, 'ALUOp')
        ],
        []
        )

    def assertOutputs(self, a, b, c ,d ,e ,f ,g ,h, i, j, k):
        output = self.testOutput.controlSignals['RegDst']
        self.assertEqual(output, a)
        output = self.testOutput.controlSignals['ALUSrc']
        self.assertEqual(output, b)
        output = self.testOutput.controlSignals['MemtoReg']
        self.assertEqual(output, c)
        output = self.testOutput.controlSignals['RegWrite']
        self.assertEqual(output, d)
        output = self.testOutput.controlSignals['MemRead']
        self.assertEqual(output, e)
        output = self.testOutput.controlSignals['MemWrite']
        self.assertEqual(output, f)
        output = self.testOutput.controlSignals['Branch']
        self.assertEqual(output, g)
        output = self.testOutput.controlSignals['BranchNE']
        self.assertEqual(output, h)
        output = self.testOutput.controlSignals['Jump']
        self.assertEqual(output, i)
        output = self.testOutput.controlSignals['LoadImm']
        self.assertEqual(output, j)
        output = self.testOutput.controlSignals['ALUOp']
        self.assertEqual(output, k)

    def test_correct_behavior(self):
        self.testInput.setOutputValue('controlInput', 0)    # R-type
        self.testInput.setOutputValue('func', 32)           # add

        self.controlUnit.readInput()
        self.controlUnit.writeOutput()
        self.testOutput.readControlSignals()

        self.assertOutputs(1,0,0,1,0,0,0,0,0,0,2)

        self.testInput.setOutputValue('controlInput', 35)    # Load Word

        self.controlUnit.readInput()
        self.controlUnit.writeOutput()
        self.testOutput.readControlSignals()

        self.assertOutputs(0,1,1,1,1,0,0,0,0,0,2)

        self.testInput.setOutputValue('controlInput', 43)      # Store Word

        self.controlUnit.readInput()
        self.controlUnit.writeOutput()
        self.testOutput.readControlSignals()

        self.assertOutputs(0,1,0,0,0,1,0,0,0,0,2)

        self.testInput.setOutputValue('controlInput', 4)    # Branch on equal

        self.controlUnit.readInput()
        self.controlUnit.writeOutput()
        self.testOutput.readControlSignals()

        self.assertOutputs(0,0,0,0,0,0,1,0,0,0,6)

        self.testInput.setOutputValue('controlInput', 5)    # branch on not equal

        self.controlUnit.readInput()
        self.controlUnit.writeOutput()
        self.testOutput.readControlSignals()

        self.assertOutputs(0,0,0,0,0,0,0,1,0,0,6)

        self.testInput.setOutputValue('controlInput', 2)    # Jump

        self.controlUnit.readInput()
        self.controlUnit.writeOutput()
        self.testOutput.readControlSignals()

        self.assertOutputs(0,0,0,0,0,0,0,0,1,0,0)

        self.testInput.setOutputValue('controlInput', 15)    # Load upper immidiate

        self.controlUnit.readInput()
        self.controlUnit.writeOutput()
        self.testOutput.readControlSignals()

        self.assertOutputs(0,0,0,1,0,0,0,0,0,1,0)

        self.testInput.setOutputValue('controlInput', 8)    # Add immidiate

        self.controlUnit.readInput()
        self.controlUnit.writeOutput()
        self.testOutput.readControlSignals()

        self.assertOutputs(0,1,0,1,0,0,0,0,0,0,2)

        self.testInput.setOutputValue('controlInput', 9)    # Add immidiate unsigned

        self.controlUnit.readInput()
        self.controlUnit.writeOutput()
        self.testOutput.readControlSignals()

        self.assertOutputs(0,1,0,1,0,0,0,0,0,0,3)

if __name__ == '__main__':
    unittest.main()
