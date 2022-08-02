import unittest
from common import *
from config import *
from cpuElement import CPUElement
from testElement import TestElement


class ALU(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'ALU should have two inputs'
        assert(len(outputValueNames) == 1), 'ALU has two outputs'
        assert(len(control) == 1), 'ALU has one control signal'
        assert(len(outputSignalNames) == 1), 'ALU has one control output'

        self.inputZero = inputSources[0][1]
        self.inputOne = inputSources[1][1]
        self.outputName = outputValueNames[0]
        self.controlName = control[0][1]
        self.outputControlName = outputSignalNames[0]

    def writeOutput(self):
        ALUOp = self.controlSignals[self.controlName]

        inputDataZero = self.inputValues[self.inputZero]
        inputDataOne = self.inputValues[self.inputOne]


    #    print('%d  %d' % (inputDataZero, inputDataOne))

        if ALUOp == ALU_ADD:
            result = inputDataZero + inputDataOne
        if ALUOp == ALU_ADDU:
            result = ((inputDataZero & 0xffffffff) + (inputDataOne & 0xffffffff)) & 0xffffffff
        if ALUOp == ALU_SUB:
            result = inputDataZero - inputDataOne
        if ALUOp == ALU_SUBU:
            result = (inputDataZero & 0xffffffff) - (inputDataOne & 0xffffffff)
            if result < 0:
                result = 0
        if ALUOp == ALU_AND:
            result = inputDataZero & inputDataOne
        if ALUOp == ALU_OR:
            result = inputDataZero | inputDataOne
        if ALUOp == ALU_NOR:
            result = (inputDataZero | inputDataOne) ^ 0xffffffff
        if ALUOp == ALU_SLT:
            if fromUnsignedWordToSignedWord(inputDataZero) < fromUnsignedWordToSignedWord(inputDataOne):
                result = 1
            else:
                result = 0

        self.outputValues[self.outputName] = result
        if result == 0:
            zero = 1
        else:
            zero = 0

        self.outputControlSignals[self.outputControlName] = zero

class TestALU(unittest.TestCase):
    def setUp(self):
        self.alu = ALU()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['dataA', 'dataB'],
        [],
        ['ALUOp']
        )

        self.alu.connect(
        [(self.testInput, 'dataA'), (self.testInput, 'dataB')],
        ['result'],
        [(self.testInput, 'ALUOp')],
        ['zeroSignal']
        )

        self.testOutput.connect(
        [(self.alu, 'result')],
        [],
        [(self.alu, 'zeroSignal')],
        []
        )

    def cycle(self):
        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.testOutput.readInput()
        self.testOutput.readControlSignals()

    def test_correct_behavior(self):
        # Add and sub
        self.testInput.setOutputValue('dataA', 32)
        self.testInput.setOutputValue('dataB', 20)
        self.testInput.setOutputControl('ALUOp', ALU_ADD)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 52)
        self.assertEqual(cOutput, 0)

        self.testInput.setOutputControl('ALUOp', ALU_SUB)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 12)
        self.assertEqual(cOutput, 0)

        self.testInput.setOutputValue('dataA', 30)
        self.testInput.setOutputValue('dataB', -32)
        self.testInput.setOutputControl('ALUOp', ALU_ADD)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, -2)
        self.assertEqual(cOutput, 0)

        self.testInput.setOutputControl('ALUOp', ALU_SUB)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 62)
        self.assertEqual(cOutput, 0)

        # addu og subu
        self.testInput.setOutputValue('dataA', 32)
        self.testInput.setOutputValue('dataB', -20)
        self.testInput.setOutputControl('ALUOp', ALU_ADDU)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 12)
        self.assertEqual(cOutput, 0)

        self.testInput.setOutputValue('dataA', -32)
        self.testInput.setOutputValue('dataB', 20)
        self.testInput.setOutputControl('ALUOp', ALU_SUBU)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 4294967244)
        self.assertEqual(cOutput, 0)


        # and, or og nor
        self.testInput.setOutputValue('dataA', 0b111100)
        self.testInput.setOutputValue('dataB', 0b001111)
        self.testInput.setOutputControl('ALUOp', ALU_AND)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 0b001100)
        self.assertEqual(cOutput, 0)

        self.testInput.setOutputControl('ALUOp', ALU_OR)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 0b111111)
        self.assertEqual(cOutput, 0)

        self.testInput.setOutputValue('dataA', 0xfffffff0)
        self.testInput.setOutputValue('dataB', 0xfffffff8)
        self.testInput.setOutputControl('ALUOp', ALU_NOR)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 7)
        self.assertEqual(cOutput, 0)

        # slt
        self.testInput.setOutputValue('dataA', 20)
        self.testInput.setOutputValue('dataB', 30)
        self.testInput.setOutputControl('ALUOp', ALU_SLT)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 1)
        self.assertEqual(cOutput, 0)

        self.testInput.setOutputValue('dataA', 20)
        self.testInput.setOutputValue('dataB', -20)

        self.cycle()

        output = self.testOutput.inputValues['result']
        cOutput = self.testOutput.controlSignals['zeroSignal']

        self.assertEqual(output, 0)
        self.assertEqual(cOutput, 1)

if __name__ == '__main__':
    unittest.main()
