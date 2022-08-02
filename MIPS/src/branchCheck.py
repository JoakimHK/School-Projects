import unittest
from cpuElement import CPUElement
from testElement import TestElement

class BranchCheck(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0), 'Branch Check does not have any inputs'
        assert(len(outputValueNames) == 0), 'Branch Check does not have any outputs'
        assert(len(control) == 3), 'Branch Check has three control signal'
        assert(len(outputSignalNames) == 1), 'Branch Check has one control output'

        self.inputNameBeq = control[0][1]
        self.inputNameBne = control[1][1]
        self.inputNameZero = control[2][1]
        self.outputName = outputSignalNames[0]

    def writeOutput(self):
        beqSig = self.controlSignals[self.inputNameBeq]
        bneSig = self.controlSignals[self.inputNameBne]
        zeroSig = self.controlSignals[self.inputNameZero]

        assert(not (beqSig == 1 and bneSig == 1)), 'Beq and bne signal cant both be 1'

        if (beqSig == 1 and zeroSig == 1) or (bneSig == 1 and zeroSig == 0):
            outSig = 1
        else:
            outSig = 0

        self.outputControlSignals[self.outputName] = outSig


class TestBranchCheck(unittest.TestCase):
    def setUp(self):
        self.branchCheck = BranchCheck()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        [],
        [],
        ['beq', 'bne', 'zero']
        )

        self.branchCheck.connect(
        [],
        [],
        [(self.testInput, 'beq'), (self.testInput, 'bne'), (self.testInput, 'zero')],
        ['branch']
        )

        self.testOutput.connect(
        [],
        [],
        [(self.branchCheck, 'branch')],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputControl('beq', 1)
        self.testInput.setOutputControl('bne', 0)
        self.testInput.setOutputControl('zero', 0)

        self.branchCheck.readControlSignals()
        self.branchCheck.writeOutput()
        self.testOutput.readControlSignals()

        output = self.testOutput.controlSignals['branch']
        self.assertEqual(output, 0)

        self.testInput.setOutputControl('zero', 1)

        self.branchCheck.readControlSignals()
        self.branchCheck.writeOutput()
        self.testOutput.readControlSignals()

        output = self.testOutput.controlSignals['branch']
        self.assertEqual(output, 1)

        self.testInput.setOutputControl('beq', 0)
        self.testInput.setOutputControl('bne', 1)

        self.branchCheck.readControlSignals()
        self.branchCheck.writeOutput()
        self.testOutput.readControlSignals()

        output = self.testOutput.controlSignals['branch']
        self.assertEqual(output, 0)

        self.testInput.setOutputControl('zero', 0)

        self.branchCheck.readControlSignals()
        self.branchCheck.writeOutput()
        self.testOutput.readControlSignals()

        output = self.testOutput.controlSignals['branch']
        self.assertEqual(output, 1)


if __name__ == '__main__':
    unittest.main()
