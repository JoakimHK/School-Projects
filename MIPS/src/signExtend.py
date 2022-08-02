import unittest
from cpuElement import CPUElement
from testElement import TestElement

class SignExtend(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'Sign Extend should have one input'
        assert(len(outputValueNames) == 1), 'Sign Extend has one output'
        assert(len(control) == 0), 'Sign Extend does not have any control signal'
        assert(len(outputSignalNames) == 0), 'Sign Extend does not have any control output'

        self.inputName = inputSources[0][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        address = self.inputValues[self.inputName]
        if (address & 0x8000) and address > 0:      # Check if most significant bit is one
            address = -(((~address) & 0xffff) + 1)  # from unsigned 16bit to signed 16bit

        self.outputValues[self.outputName] = address

class TestSignExtend(unittest.TestCase):
    def setUp(self):
        self.signExtend = SignExtend()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['address'],
        [],
        []
        )

        self.signExtend.connect(
        [(self.testInput, 'address')],
        ['signExAddress'],
        [],
        []
        )

        self.testOutput.connect(
        [(self.signExtend, 'signExAddress')],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('address', 0xfffd)

        self.signExtend.readInput()
        self.signExtend.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['signExAddress']
        self.assertEqual(output, -3)

        self.testInput.setOutputValue('address', 0x0008)

        self.signExtend.readInput()
        self.signExtend.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['signExAddress']
        self.assertEqual(output, 8)




if __name__ == '__main__':
    unittest.main()
