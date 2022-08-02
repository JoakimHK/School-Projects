'''
This version tries to implement control hazard detection, but I didn't get it to work :/
'''

from cpuElement import CPUElement

class PC(CPUElement):
    def __init__(self, baseaddr):
        self.baseaddr = baseaddr

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'PC should have one input'
        assert(len(outputValueNames) == 1), 'PC has only one output'
        assert(len(control) == 1), 'PC has one control input'
        assert(len(outputSignalNames) == 0), 'PC should not have any control output'

        self.inputField_newPcAddress = inputSources[0][1]
        self.outputField_pcAddress = outputValueNames[0]
        self.controlName = control[0][1]

        self.inputValues[self.inputField_newPcAddress] = self.baseaddr # initialize PC
        self.prevAddress = self.baseaddr

    def writeOutput (self):
        stallSignal = self.controlSignals[self.controlName]
        #print(stallSignal)

        #print('Prev: %s' % hex(self.prevAddress))
        #print('Input: %s' % hex(self.inputValues[self.inputField_newPcAddress]))
        if stallSignal == 1:
            self.outputValues[self.outputField_pcAddress] = self.prevAddress
        else:
            self.outputValues[self.outputField_pcAddress] = self.inputValues[self.inputField_newPcAddress]
            self.prevAddress = self.inputValues[self.inputField_newPcAddress]

        print('Output: %s' % hex(self.outputValues[self.outputField_pcAddress]))


    def currentAddress (self):
        return self.inputValues[self.inputField_newPcAddress]
