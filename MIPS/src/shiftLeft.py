import unittest
from cpuElement import CPUElement
from testElement import TestElement

class ShiftLeft(CPUElement):
    def __init__(self, shift):
        self.shift = shift

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'Shift Left should have one input'
        assert(len(outputValueNames) == 1), 'Shift Left has one output'
        assert(len(control) == 0), 'Shift Left does not have any control signal'
        assert(len(outputSignalNames) == 0), 'Shift Left does not have any control output'

        self.inputName = inputSources[0][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        address = self.inputValues[self.inputName] << self.shift
        #print(hex(address))
        self.outputValues[self.outputName] = address

class TestShiftLeft(unittest.TestCase):
    def setUp(self):
        self.shiftLeft = ShiftLeft(2)
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['address'],
        [],
        []
        )

        self.shiftLeft.connect(
        [(self.testInput, 'address')],
        ['address'],
        [],
        []
        )

        self.testOutput.connect(
        [(self.shiftLeft, 'address')],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('address', 10)

        self.shiftLeft.readInput()
        self.shiftLeft.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['address']

        self.assertEqual(output, 40)


if __name__ == '__main__':
    unittest.main()
