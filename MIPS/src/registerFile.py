'''
Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
from testElement import TestElement
import common

class RegisterFile(CPUElement):
    def __init__(self):
        # Dictionary mapping register number to register value
        self.register = {}

        # All registers default to 0
        for i in range(0, 32):
            self.register[i] = 0

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 4), 'ReMuxgister file should have 4 inputs'
        assert(len(outputValueNames) == 2), 'Register file has 2 outputs'
        assert(len(control) == 1), 'Register file has one control signal'
        assert(len(outputSignalNames) == 0), 'Register file does not have any control output'

        self.inputReg1 = inputSources[0][1]
        self.inputReg2 = inputSources[1][1]
        self.inputWReg = inputSources[2][1]
        self.inputData = inputSources[3][1]
        self.outputReg1 = outputValueNames[0]
        self.outputReg2 = outputValueNames[1]
        self.controlName = control[0][1]

    def writeOutput(self):
        RegWrite = self.controlSignals[self.controlName]
        #print('regwrite: %d' % RegWrite)

        assert(isinstance(RegWrite, int))
        assert(not isinstance(RegWrite, bool))  # ...  (not bool)
        assert(RegWrite == 0 or RegWrite == 1), 'Invalid register control signal value: %d' % (RegWrite,)

        reg1 = self.inputValues[self.inputReg1]
        reg2 = self.inputValues[self.inputReg2]

        self.outputValues[self.outputReg1] = self.register[reg1]
        self.outputValues[self.outputReg2] = self.register[reg2]

        if RegWrite == 1:
            wReg = self.inputValues[self.inputWReg]
            #print('\nwReg: %d' % wReg)
            self.register[wReg] = self.inputValues[self.inputData]
            #print('Write data: %d\n' % self.inputValues[self.inputData])

    def printAll(self):
        '''
        Print the name and value in each register.
        '''

        # Note that we won't actually use all the registers listed here...
        registerNames = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                        '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                        '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                        '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']

        print()
        print("Register file")
        print("================")
        for i in range(0, 32):
            print("%s \t=> %s (%s)" % (registerNames[i], common.fromUnsignedWordToSignedWord(self.register[i]), hex(int(self.register[i]))[:-1]))
        print("================")
        print()
        print()

class TestRegisterFile(unittest.TestCase):
    def setUp(self):
        self.registerFile = RegisterFile()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['reg1', 'reg2', 'wReg', 'wData'],
            [],
            ['RegWrite']
        )

        self.registerFile.connect(
            [(self.testInput, 'reg1'),
            (self.testInput, 'reg2'),
            (self.testInput, 'wReg'),
            (self.testInput, 'wData')],
            ['reg1Data', 'reg2Data'],
            [(self.testInput, 'RegWrite')],
            []
        )

        self.testOutput.connect(
            [(self.registerFile, 'reg1Data'),
            (self.registerFile, 'reg2Data')],
            [],
            [],
            []
        )


    def cycle(self):
        self.registerFile.readInput()
        self.registerFile.readControlSignals()
        self.registerFile.writeOutput()
        self.testOutput.readInput()
    #    self.registerFile.printAll()



    def test_correct_behavior(self):
        self.testInput.setOutputValue('reg1', 9)
        self.testInput.setOutputValue('reg2', 10)
        self.testInput.setOutputValue('wReg', 9)
        self.testInput.setOutputValue('wData', 256)
        self.testInput.setOutputControl('RegWrite', 1)

        self.cycle()

        output = self.registerFile.register[9]
        self.assertEqual(output, 256)

        self.testInput.setOutputValue('wReg', 10)
        self.testInput.setOutputValue('wData', 128)

        self.cycle()

        output = self.registerFile.register[10]
        self.assertEqual(output, 128)

        self.testInput.setOutputControl('RegWrite', 0)

        self.cycle()

        output1 = self.testOutput.inputValues['reg1Data']
        self.assertEqual(output1, 256)
        output2 = self.testOutput.inputValues['reg2Data']
        self.assertEqual(output2, 128)





if __name__ == '__main__':
    unittest.main()
