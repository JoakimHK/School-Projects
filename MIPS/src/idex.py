import unittest
from cpuElement import CPUElement
from testElement import TestElement

class IDEX(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 8), 'ID/EX should have seven input'
        assert(len(outputValueNames) == 8), 'ID/EX has seven output'
        assert(len(control) == 10), 'ID/EX has ten control signals'
        assert(len(outputSignalNames) == 10), 'ID/EX has ten control outputs'


        self.regDst = control[0][1]
        self.aluSrc = control[1][1]
        self.memtoReg = control[2][1]
        self.regWrite = control[3][1]
        self.memRead = control[4][1]
        self.memWrite = control[5][1]
        self.branchEQ = control[6][1]
        self.branchNE = control[7][1]
        self.loadImm = control[8][1]
        self.aluOp = control[9][1]
        #Jump does not go through this pipeline register

        self.adder = inputSources[0][1]     # Incremented next address
        self.reg1 = inputSources[1][1]      # Data from first register
        self.reg2 = inputSources[2][1]      # Data from second register
        self.signEx = inputSources[3][1]    # Sign extended immidiate
        self.shift16 = inputSources[4][1]   # Immidiate shift lefted 16 bits
        self.instReg1 = inputSources[5][1]   # 25-21 part of instruction
        self.instReg2 = inputSources[6][1]  # 20-16 part of instruction
        self.instReg3 = inputSources[7][1]  # 15-11 part of instruction


    def writeOutput(self):

        self.outputControlSignals[self.regDst] = self.controlSignals.get(self.regDst, 0)
        self.outputControlSignals[self.aluSrc] = self.controlSignals.get(self.aluSrc, 0)
        self.outputControlSignals[self.memtoReg] = self.controlSignals.get(self.memtoReg, 0)
        self.outputControlSignals[self.regWrite] = self.controlSignals.get(self.regWrite, 0)
        self.outputControlSignals[self.memRead] = self.controlSignals.get(self.memRead, 0)
        self.outputControlSignals[self.memWrite] = self.controlSignals.get(self.memWrite, 0)
        self.outputControlSignals[self.branchEQ] = self.controlSignals.get(self.branchEQ, 0)
        self.outputControlSignals[self.branchNE] = self.controlSignals.get(self.branchNE, 0)
        self.outputControlSignals[self.loadImm] = self.controlSignals.get(self.loadImm, 0)
        self.outputControlSignals[self.aluOp] = self.controlSignals.get(self.aluOp, 0)


        self.outputValues[self.adder] = self.inputValues.get(self.adder, 0)
        self.outputValues[self.reg1] = self.inputValues.get(self.reg1, 0)
        self.outputValues[self.reg2] = self.inputValues.get(self.reg2, 0)
        self.outputValues[self.signEx] = self.inputValues.get(self.signEx, 0)
        self.outputValues[self.shift16] = self.inputValues.get(self.shift16, 0)
        self.outputValues[self.instReg1] = self.inputValues.get(self.instReg1, 0)
        self.outputValues[self.instReg2] = self.inputValues.get(self.instReg2, 0)
        self.outputValues[self.instReg3] = self.inputValues.get(self.instReg3, 0)

    '''    print('\n%s: %d' % (self.adder, self.inputValues[self.adder]))
        print('%s: %d' % (self.reg1, self.inputValues[self.reg1]))
        print('%s: %d' % (self.reg2, self.inputValues[self.reg2]))
        print('%s: %d' % (self.signEx, self.inputValues[self.signEx]))
        print('%s: %d' % (self.shift16, self.inputValues[self.shift16]))
        print('%s: %d' % (self.instReg1, self.inputValues[self.instReg1]))
        print('%s: %d' % (self.instReg2, self.inputValues[self.instReg2]))
        print('%s: %d\n' % (self.instReg3, self.inputValues[self.instReg3]))

        print('\n%s: %d' % (self.regDst, self.controlSignals[self.regDst]))
        print('%s: %d' % (self.aluSrc, self.controlSignals[self.aluSrc]))
        print('%s: %d' % (self.memtoReg, self.controlSignals[self.memtoReg]))
        print('%s: %d' % (self.regWrite, self.controlSignals[self.regWrite]))
        print('%s: %d' % (self.memRead, self.controlSignals[self.memRead]))
        print('%s: %d' % (self.memWrite, self.controlSignals[self.memWrite]))
        print('%s: %d' % (self.branchEQ, self.controlSignals[self.branchEQ]))
        print('%s: %d' % (self.branchNE, self.controlSignals[self.branchNE]))
        print('%s: %d' % (self.loadImm, self.controlSignals[self.loadImm]))
        print('%s: %d\n' % (self.aluOp, self.controlSignals[self.aluOp]))
'''
