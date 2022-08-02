import unittest
from cpuElement import CPUElement
from testElement import TestElement

class JumpAddress(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'Jump Address should have two inputs'
        assert(len(outputValueNames) == 1), 'Jump Address has one output'
        assert(len(control) == 0), 'Jump Address does not have any control signal'
        assert(len(outputSignalNames) == 0), 'Jump Address does not have any control output'

        self.inputZero = inputSources[0][1]
        self.inputOne = inputSources[1][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        PCAddr = self.inputValues[self.inputZero]
        jmpAddr = self.inputValues[self.inputOne]

        PCAddr = PCAddr & 0xf0000000    # Get the 4 highest bits of the address
        jmpAddr = jmpAddr << 2

        self.outputValues[self.outputName] = PCAddr + jmpAddr


class TestJumpAddress(unittest.TestCase):
    def setUp(self):
        self.jumpAddress = JumpAddress()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['PCAddr', 'jmpAddr'],
        [],
        []
        )

        self.jumpAddress.connect(
        [(self.testInput, 'PCAddr'), (self.testInput, 'jmpAddr')],
        ['jumpAddress'],
        [],
        []
        )

        self.testOutput.connect(
        [(self.jumpAddress, 'jumpAddress')],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('PCAddr', 0xbfc00004)
        self.testInput.setOutputValue('jmpAddr', 0x3f00080)

        self.jumpAddress.readInput()
        self.jumpAddress.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['jumpAddress']

        self.assertEqual(output, 0xbfc00200)

if __name__ == '__main__':
    unittest.main()
