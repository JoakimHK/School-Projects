import unittest
from cpuElement import CPUElement
from testElement import TestElement

class MEMWB(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 4), 'MEM/WB should have four input'
        assert(len(outputValueNames) == 4), 'MEM/WB has four output'
        assert(len(control) == 3), 'MEM/WB has three control signals'
        assert(len(outputSignalNames) == 3), 'MEM/WB has three control outputs'


        self.memtoReg = control[0][1]
        self.regWrite = control[1][1]
        self.loadImm = control[2][1]


        self.memData = inputSources[0][1]    # Data extrected from data memory
        self.alu = inputSources[1][1]       # Result from the ALU
        self.shift16 = inputSources[2][1]   # Immidiate shift lefted 16 bits
        self.wReg = inputSources[3][1]      # Write register

        self.wRegOut = outputValueNames[3]      # Different name out so forwarding unit doesnt get duplicate input names
        self.regWriteOut = outputSignalNames[1] # Same as above

    def writeOutput(self):

        self.outputControlSignals[self.memtoReg] = self.controlSignals.get(self.memtoReg, 0)
        self.outputControlSignals[self.regWriteOut] = self.controlSignals.get(self.regWrite, 0)
        self.outputControlSignals[self.loadImm] = self.controlSignals.get(self.loadImm, 0)


        self.outputValues[self.memData] = self.inputValues.get(self.memData, 0)
        self.outputValues[self.alu] = self.inputValues.get(self.alu, 0)
        self.outputValues[self.shift16] = self.inputValues.get(self.shift16, 0)
        self.outputValues[self.wRegOut] = self.inputValues.get(self.wReg, 0)

    '''    print('\n%s: %d' % (self.memData, self.inputValues[self.memData]))
        print('%s: %d' % (self.alu, self.inputValues[self.alu]))
        print('%s: %d' % (self.shift16, self.inputValues[self.shift16]))
        print('%s: %d' % (self.wRegOut, self.outputValues[self.wRegOut]))

        print('%s: %d' % (self.memtoReg, self.controlSignals[self.memtoReg]))
        print('%s: %d' % (self.regWriteOut, self.outputControlSignals[self.regWriteOut]))
        print('%s: %d\n' % (self.loadImm, self.controlSignals[self.loadImm]))
'''
