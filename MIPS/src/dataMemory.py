'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
from memory import Memory
from testElement import TestElement
import common
import unittest

class DataMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'Data memory should have two inputs'
        assert(len(outputValueNames) == 1), 'Data memory has only one output'
        assert(len(control) == 2), 'Data memory has two control signal'
        assert(len(outputSignalNames) == 0), 'Data memory does not have any control output'

        self.inputALU = inputSources[0][1]
        self.inputReg = inputSources[1][1]
        self.controlNameRead = control[0][1]
        self.controlNameWrite = control[1][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        memRead = self.controlSignals[self.controlNameRead]
        memWrite = self.controlSignals[self.controlNameWrite]
        assert(not (memRead == 1 and memWrite == 1)), 'MemRead and MemWrite cant both be 1'

        address = self.inputValues[self.inputALU]
        writeData = self.inputValues[self.inputReg]
        output = 0

#        print(hex(address)
#        print(writeData)

        if memRead == 1:
            output = self.memory.get(address, 0)
        elif memWrite == 1:
            self.memory[address] = writeData

        self.outputValues[self.outputName] = output


class TestDataMemory(unittest.TestCase):
    def setUp(self):
        self.dataMemory = DataMemory('add.mem')
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['ALUresult', 'RegisterData'],
        [],
        ['MemRead', 'MemWrite']
        )

        self.dataMemory.connect(
        [(self.testInput, 'ALUresult'), (self.testInput, 'RegisterData')],
        ['memoryData'],
        [(self.testInput, 'MemRead'), (self.testInput, 'MemWrite')],
        []
        )
        
        self.testOutput.connect(
        [(self.dataMemory, 'memoryData')],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('ALUresult', 0xbfc00234)
        self.testInput.setOutputValue('RegisterData', 42)
        self.testInput.setOutputControl('MemRead', 0)
        self.testInput.setOutputControl('MemWrite', 1)

        self.dataMemory.readInput()
        self.dataMemory.readControlSignals()
        self.dataMemory.writeOutput()
        self.testOutput.readInput()

        output = self.dataMemory.memory[0xbfc00234]

        self.assertEqual(output, 42)

        self.testInput.setOutputControl('MemRead', 1)
        self.testInput.setOutputControl('MemWrite', 0)

        self.dataMemory.readInput()
        self.dataMemory.readControlSignals()
        self.dataMemory.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['memoryData']
        self.assertEqual(output, 42)

        self.testInput.setOutputValue('ALUresult', 0xbfc00008)

        self.dataMemory.readInput()
        self.dataMemory.readControlSignals()
        self.dataMemory.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['memoryData']
        self.assertEqual(output, 100)

if __name__ == '__main__':
    unittest.main()
