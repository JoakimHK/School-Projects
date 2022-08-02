import unittest
from cpuElement import CPUElement
from testElement import TestElement

class MuxTriple(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect mux to input sources and controller

        Note that the first inputSource is input zero, and the second is input 1
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 3), 'Mux should have three inputs'
        assert(len(outputValueNames) == 1), 'Mux has only one output'
        assert(len(control) == 1), 'Mux has one control signal'
        assert(len(outputSignalNames) == 0), 'Mux does not have any control output'

        self.inputZero = inputSources[0][1]
        self.inputOne = inputSources[1][1]
        self.inputTwo = inputSources[2][1]
        self.outputName = outputValueNames[0]
        self.controlName = control[0][1]

    def writeOutput(self):
        muxControl = self.controlSignals[self.controlName]

        assert(isinstance(muxControl, int))
        assert(not isinstance(muxControl, bool))  # ...  (not bool)
        assert(muxControl == 0 or muxControl == 1 or muxControl == 2), 'Invalid mux control signal value: %d' % (muxControl,)

        if muxControl == 0:
            self.outputValues[self.outputName] = self.inputValues[self.inputZero]
        elif muxControl == 1:  # muxControl == 1
            self.outputValues[self.outputName] = self.inputValues[self.inputOne]
        else:
            self.outputValues[self.outputName] = self.inputValues[self.inputTwo]

        #print('%s: %d' % (self.inputZero, self.inputValues[self.inputZero]))
        #print('%s: %d' % (self.inputOne, self.inputValues[self.inputOne]))
        #print('%s: %d' % (self.inputTwo, self.inputValues[self.inputTwo]))

        #print('%s: %d' % (self.controlName, muxControl))
    #    self.printOutput()
    #    print()

    def printOutput(self):
        '''
        Debug function that prints the output value
        '''
        print('mux.output = %d' % (self.outputValues[self.outputName],))


class TestMuxTriple(unittest.TestCase):
    def setUp(self):
        self.mux = MuxTriple()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['dataA', 'dataB', 'dataC'],
            [],
            ['muxControl']
        )

        self.mux.connect(
            [(self.testInput, 'dataA'), (self.testInput, 'dataB'), (self.testInput, 'dataC')],
            ['muxData'],
            [(self.testInput, 'muxControl')],
            []
        )

        self.testOutput.connect(
            [(self.mux, 'muxData')],
            [],
            [],
            []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('dataA', 10)
        self.testInput.setOutputValue('dataB', 20)
        self.testInput.setOutputValue('dataC', 30)

        self.testInput.setOutputControl('muxControl', 0)

        self.mux.readInput()
        self.mux.readControlSignals()
        self.mux.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues['muxData']

        self.assertEqual(output, 10)

        self.testInput.setOutputControl('muxControl', 1)

        self.mux.readInput()
        self.mux.readControlSignals()
        self.mux.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues['muxData']

        self.assertEqual(output, 20)

        self.testInput.setOutputControl('muxControl', 2)

        self.mux.readInput()
        self.mux.readControlSignals()
        self.mux.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues['muxData']

        self.assertEqual(output, 30)

    def assert_callback(self, arg):
        self.testInput.setOutputControl('muxControl', arg)
        self.mux.readControlSignals()
        self.mux.writeOutput()

    def test_assert_on_incorrect_input(self):
        self.testInput.setOutputValue('dataA', 10)
        self.testInput.setOutputValue('dataB', 20)
        self.mux.readInput()

        self.assertRaises(AssertionError, self.assert_callback, '1')
        self.assertRaises(AssertionError, self.assert_callback, '0')
        self.assertRaises(AssertionError, self.assert_callback, True)
        self.assertRaises(AssertionError, self.assert_callback, False)

if __name__ == '__main__':
    unittest.main()
