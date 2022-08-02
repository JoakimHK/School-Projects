import unittest
from cpuElement import CPUElement
from testElement import TestElement

class ForwardingUnit(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 4), 'Forwarding Unit should have four inputs'
        assert(len(outputValueNames) == 0), 'Forwarding Unit has no output'
        assert(len(control) == 2), 'Forwarding Unit has two control signals'
        assert(len(outputSignalNames) == 2), 'Forwarding Unit has two control outputs'

        self.inputIDEXRs = inputSources[0][1]
        self.inputIDEXRt = inputSources[1][1]
        self.inputEXMEMRd = inputSources[2][1]
        self.inputMEMWBRd = inputSources[3][1]
        self.controlName1 = control[0][1]
        self.controlName2 = control[1][1]

        self.controlOutA = outputSignalNames[0]
        self.controlOutB = outputSignalNames[1]


    def writeOutput(self):
        IDEXRegRs = self.inputValues[self.inputIDEXRs]
        IDEXRegRt = self.inputValues[self.inputIDEXRt]
        EXMEMRegRd = self.inputValues[self.inputEXMEMRd]
        MEMWBRegRd = self.inputValues[self.inputMEMWBRd]

        EXMEMRegWrite = self.controlSignals[self.controlName1]
        MEMWBRegWrite = self.controlSignals[self.controlName2]

        #print('\nID/EX register rs: %d' % IDEXRegRs)
        #print('ID/EX register rt: %d' % IDEXRegRt)
        #print('EX/MEM register rd: %d' % EXMEMRegRd)
        #print('MEM/WB register rd: %d\n' % MEMWBRegRd)



        forwardA = 0
        forwardB = 0

        if (EXMEMRegWrite
            and (EXMEMRegRd != 0)
            and (EXMEMRegRd == IDEXRegRs)):
            forwardA = 2

        if (EXMEMRegWrite
            and (EXMEMRegRd != 0)
            and (EXMEMRegRd == IDEXRegRt)):
            forwardB = 2

        if (MEMWBRegWrite
            and (MEMWBRegRd != 0)
            and not(EXMEMRegWrite and (EXMEMRegRd != 0)
                and (EXMEMRegRd != IDEXRegRs))
            and (MEMWBRegRd == IDEXRegRs)):
            forwardA = 1

        if (MEMWBRegWrite
            and (MEMWBRegRd != 0)
            and not(EXMEMRegWrite and (EXMEMRegRd != 0)
                and (EXMEMRegRd != IDEXRegRs))
            and (MEMWBRegRd == IDEXRegRt)):
            forwardB = 1

        self.outputControlSignals[self.controlOutA] = forwardA
        self.outputControlSignals[self.controlOutB] = forwardB

    #    print('\nForwardA: %d' % forwardA)
    #    print('ForwardB: %d\n' % forwardB)


class TestForwardingUnit(unittest.TestCase):
    def setUp(self):
        pass

    def test_correct_behavior(self):
        pass
