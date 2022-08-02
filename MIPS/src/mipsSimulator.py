'''
Code written for inf-2200, University of Tromso
'''

from pc import PC
from add import Add
from mux import Mux
from registerFile import RegisterFile
from instructionMemory import InstructionMemory
from dataMemory import DataMemory
from constant import Constant
from alu import ALU
from branchCheck import BranchCheck
from controlUnit import ControlUnit
from jumpAddress import JumpAddress
from shiftLeft import ShiftLeft
from signExtend import SignExtend


class MIPSSimulator():
    '''Main class for MIPS pipeline simulator.

    Provides the main method tick(), which runs pipeline
    for one clock cycle.

    '''
    def __init__(self, memoryFile):
        self.nCycles = 0 # Used to hold number of clock cycles spent executing instructions

        self.pc = PC(0xbfc00000) # hard coded "boot" address
        self.constant4 = Constant(4)
        self.adder1 = Add()
        self.adder2 = Add()
        self.mux1 = Mux()
        self.mux2 = Mux()
        self.mux3 = Mux()
        self.mux4 = Mux()
        self.mux5 = Mux()
        self.mux6 = Mux()
        self.instructionMemory = InstructionMemory(memoryFile)
        self.dataMemory = DataMemory(memoryFile)
        self.registerFile = RegisterFile()
        self.signExtend = SignExtend()
        self.shiftLeft16 = ShiftLeft(16)
        self.controlUnit = ControlUnit()
        self.alu = ALU()
        self.jumpAddress = JumpAddress()
        self.shiftLeft2 = ShiftLeft(2)
        self.branchCheck = BranchCheck()

        self.elements = [self.constant4,
                        self.adder1, self.instructionMemory, self.jumpAddress,
                        self.controlUnit, self.mux1, self.registerFile, self.signExtend, self.shiftLeft16,
                        self.mux2, self.shiftLeft2, self.adder2, self.alu, self.branchCheck,
                        self.mux3, self.mux4, self.dataMemory, self.mux5, self.mux6,
                        self.registerFile]

        self._connectCPUElements()

    def _connectCPUElements(self):
        self.constant4.connect(
            [],
            ['constant'],
            [],
            []
        )

        self.adder1.connect(
            [(self.pc, 'pcAddress'), (self.constant4, 'constant')],
            ['nextAddress'],
            [],
            []
        )

        self.instructionMemory.connect(
            [(self.pc, 'pcAddress')],
            ['inst31-26', 'inst25-21', 'inst20-16', 'inst15-11', 'inst15-0', 'inst5-0', 'inst25-0'],
            [],
            []
        )

        self.jumpAddress.connect(
            [(self.adder1, 'nextAddress'), (self.instructionMemory, 'inst25-0')],
            ['jumpAddress'],
            [],
            []
        )

        self.controlUnit.connect(
            [(self.instructionMemory, 'inst31-26'), (self.instructionMemory, 'inst5-0')],
            [],
            [],
            ['RegDst', 'ALUSrc', 'MemtoReg', 'RegWrite', 'MemRead', 'MemWrite', 'BranchEQ', 'BranchNE', 'Jump', 'LoadImm', 'ALUOp']
        )

        self.mux1.connect(
            [(self.instructionMemory, 'inst20-16'), (self.instructionMemory, 'inst15-11')],
            ['mux1Data'],
            [(self.controlUnit, 'RegDst')],
            []
        )

        self.registerFile.connect(
            [(self.instructionMemory, 'inst25-21'), (self.instructionMemory, 'inst20-16'), (self.mux1, 'mux1Data'), (self.mux6, 'mux6Data')],
            ['reg1Data', 'reg2Data'],
            [(self.controlUnit, 'RegWrite')],
            []
        )

        self.signExtend.connect(
            [(self.instructionMemory, 'inst15-0')],
            ['signExAddress'],
            [],
            []
        )

        self.shiftLeft16.connect(
            [(self.instructionMemory, 'inst15-0')],
            ['shiftedImmAddress'],
            [],
            []
        )

        self.mux2.connect(
            [(self.registerFile, 'reg2Data'), (self.signExtend, 'signExAddress')],
            ['mux2Data'],
            [(self.controlUnit, 'ALUSrc')],
            []
        )

        self.shiftLeft2.connect(
            [(self.signExtend, 'signExAddress')],
            ['shiftedAddress'],
            [],
            []
        )

        self.adder2.connect(
            [(self.adder1, 'nextAddress'), (self.shiftLeft2, 'shiftedAddress')],
            ['branchAddress'],
            [],
            []
        )

        self.alu.connect(
            [(self.registerFile, 'reg1Data'), (self.mux2, 'mux2Data')],
            ['aluResult'],
            [(self.controlUnit, 'ALUOp')],
            ['Zero']
        )

        self.branchCheck.connect(
            [],
            [],
            [(self.controlUnit, 'BranchEQ'), (self.controlUnit, 'BranchNE'), (self.alu, 'Zero')],
            ['BranchSignal']
        )

        self.mux3.connect(
            [(self.adder1, 'nextAddress'), (self.adder2, 'branchAddress')],
            ['mux3Data'],
            [(self.branchCheck, 'BranchSignal')],
            []
        )

        self.mux4.connect(
            [(self.mux3, 'mux3Data'), (self.jumpAddress, 'jumpAddress')],
            ['mux4Data'],
            [(self.controlUnit, 'Jump')],
            []
        )

        self.dataMemory.connect(
            [(self.alu, 'aluResult'), (self.registerFile, 'reg2Data')],
            ['memoryData'],
            [(self.controlUnit, 'MemRead'), (self.controlUnit, 'MemWrite')],
            []
        )

        self.mux5.connect(
            [(self.alu, 'aluResult'), (self.shiftLeft16, 'shiftedImmAddress')],
            ['mux5Data'],
            [(self.controlUnit, 'LoadImm')],
            []
        )

        self.mux6.connect(
            [(self.mux5, 'mux5Data'), (self.dataMemory, 'memoryData')],
            ['mux6Data'],
            [(self.controlUnit, 'MemtoReg')],
            []
        )

        self.pc.connect(
            [(self.mux4, 'mux4Data')],
            ['pcAddress'],
            [],
            []
        )

    def clockCycles(self):
        '''Returns the number of clock cycles spent executing instructions.'''

        return self.nCycles

    def dataMemory(self):
        '''Returns dictionary, mapping memory addresses to data, holding
        data memory after instructions have finished executing.'''

        return self.dataMemory.memory

    def registerFile(self):
        '''Returns dictionary, mapping register numbers to data, holding
        register file after instructions have finished executing.'''

        return self.registerFile.register

    def printDataMemory(self):
        self.dataMemory.printAll()

    def printRegisterFile(self):
        self.registerFile.printAll()

    def tick(self):
        '''Execute one clock cycle of pipeline.'''

        self.nCycles += 1

        self.pc.writeOutput()

        for elem in self.elements:
            elem.readControlSignals()
            elem.readInput()
            elem.writeOutput()
            elem.setControlSignals()

        self.pc.readInput()
