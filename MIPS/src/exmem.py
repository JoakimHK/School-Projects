import unittest
from cpuElement import CPUElement
from testElement import TestElement

class EXMEM(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 5), 'EX/MEM should have five input'
        assert(len(outputValueNames) == 5), 'EX/MEM has five output'
        assert(len(control) == 8), 'EX/MEM has eight control signals'
        assert(len(outputSignalNames) == 8), 'EX/MEM has eight control outputs'


        self.memtoReg = control[0][1]
        self.regWrite = control[1][1]
        self.memRead = control[2][1]
        self.memWrite = control[3][1]
        self.branchEQ = control[4][1]
        self.branchNE = control[5][1]
        self.loadImm = control[6][1]
        self.zero = control[7][1]


        self.adder2 = inputSources[0][1]    # Branch address
        self.alu = inputSources[1][1]       # Result from the ALU
        self.reg2 = inputSources[2][1]      # Data from second register
        self.shift16 = inputSources[3][1]   # Immidiate shift lefted 16 bits
        self.wReg = inputSources[4][1]      # Write register


    def writeOutput(self):

        self.outputControlSignals[self.memtoReg] = self.controlSignals.get(self.memtoReg, 0)
        self.outputControlSignals[self.regWrite] = self.controlSignals.get(self.regWrite, 0)
        self.outputControlSignals[self.memRead] = self.controlSignals.get(self.memRead, 0)
        self.outputControlSignals[self.memWrite] = self.controlSignals.get(self.memWrite, 0)
        self.outputControlSignals[self.branchEQ] = self.controlSignals.get(self.branchEQ, 0)
        self.outputControlSignals[self.branchNE] = self.controlSignals.get(self.branchNE, 0)
        self.outputControlSignals[self.loadImm] = self.controlSignals.get(self.loadImm, 0)
        self.outputControlSignals[self.zero] = self.controlSignals.get(self.zero, 0)


        self.outputValues[self.adder2] = self.inputValues.get(self.adder2, 0)
        self.outputValues[self.alu] = self.inputValues.get(self.alu, 0)
        self.outputValues[self.reg2] = self.inputValues.get(self.reg2, 0)
        self.outputValues[self.shift16] = self.inputValues.get(self.shift16, 0)
        self.outputValues[self.wReg] = self.inputValues.get(self.wReg, 0)
