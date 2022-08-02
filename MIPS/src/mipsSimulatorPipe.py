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
from ifid import IFID
from idex import IDEX
from exmem import EXMEM
from memwb import MEMWB
from forwardingUnit import ForwardingUnit
from muxTriple import MuxTriple


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
        self.muxBranch = Mux()
        self.muxJump = Mux()
        self.muxALU = Mux()
        self.muxWReg = Mux()
        self.muxImm = Mux()
        self.muxDMem = Mux()
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
        self.ifid = IFID()
        self.idex = IDEX()
        self.exmem = EXMEM()
        self.memwb = MEMWB()
        self.forwardingUnit = ForwardingUnit()
        self.muxTripleA = MuxTriple()
        self.muxTripleB = MuxTriple()

        self.elements = [self.memwb, self.muxImm, self.muxDMem, self.registerFile,
                        self.exmem, self.branchCheck, self.dataMemory,
                        self.idex, self.forwardingUnit, self.muxTripleA, self.muxTripleB, self.muxWReg, self.muxALU, self.shiftLeft2, self.adder2, self.alu,
                        self.ifid, self.jumpAddress, self.controlUnit, self.registerFile, self.signExtend, self.shiftLeft16,
                        self.constant4, self.adder1, self.muxBranch, self.muxJump, self.instructionMemory]

        self._connectCPUElements()

    def _connectCPUElements(self):
        self.muxBranch.connect(
            [(self.adder1, 'nextAddress'), (self.exmem, 'branchAddress')],
            ['muxBranchData'],
            [(self.branchCheck, 'BranchSignal')],
            []
        )

        self.muxJump.connect(
            [(self.muxBranch, 'muxBranchData'), (self.jumpAddress, 'jumpAddress')],
            ['muxJumpData'],
            [(self.controlUnit, 'Jump')],
            []
        )

        self.pc.connect(
            [(self.muxJump, 'muxJumpData')],
            ['pcAddress'],
            #[(self.instructionMemory, 'StallSignal')],
            [],
            []
        )

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
            #['StallSignal']
            []
        )

        self.ifid.connect(
            [(self.adder1, 'nextAddress'), (self.instructionMemory, 'inst31-26'),
            (self.instructionMemory, 'inst25-21'), (self.instructionMemory, 'inst20-16'),
            (self.instructionMemory, 'inst15-11'), (self.instructionMemory, 'inst15-0'),
            (self.instructionMemory, 'inst5-0'), (self.instructionMemory, 'inst25-0')],
            ['nextAddress', 'inst31-26', 'inst25-21', 'inst20-16',
            'inst15-11', 'inst15-0', 'inst5-0', 'inst25-0'],
            [],
            []
        )

        self.jumpAddress.connect(
            [(self.ifid, 'nextAddress'), (self.ifid, 'inst25-0')],
            ['jumpAddress'],
            [],
            []
        )

        self.controlUnit.connect(
            [(self.ifid, 'inst31-26'), (self.ifid, 'inst5-0')],
            [],
            [],
            ['RegDst', 'ALUSrc', 'MemtoReg', 'RegWrite', 'MemRead', 'MemWrite', 'BranchEQ', 'BranchNE', 'Jump', 'LoadImm', 'ALUOp']
        )

        self.registerFile.connect(
            [(self.ifid, 'inst25-21'), (self.ifid, 'inst20-16'), (self.memwb, 'muxWRegData1'), (self.muxDMem, 'muxDMemData')],
            ['reg1Data', 'reg2Data'],
            [(self.memwb, 'RegWrite1')],
            []
        )

        self.signExtend.connect(
            [(self.ifid, 'inst15-0')],
            ['signExAddress'],
            [],
            []
        )

        self.shiftLeft16.connect(
            [(self.ifid, 'inst15-0')],
            ['shiftedImmAddress'],
            [],
            []
        )

        self.idex.connect(
            [(self.adder1, 'nextAddress'), (self.registerFile, 'reg1Data'),
            (self.registerFile, 'reg2Data'), (self.signExtend, 'signExAddress'),
            (self.shiftLeft16, 'shiftedImmAddress'), (self.ifid, 'inst25-21'),
            (self.ifid, 'inst20-16'), (self.ifid, 'inst15-11')],
            ['nextAddress', 'reg1Data', 'reg2Data', 'signExAddress',
            'shiftedImmAddress', 'inst25-21', 'inst20-16', 'inst15-11'],
            [(self.controlUnit, 'RegDst'), (self.controlUnit, 'ALUSrc'),
            (self.controlUnit, 'MemtoReg'), (self.controlUnit, 'RegWrite'),
            (self.controlUnit, 'MemRead'), (self.controlUnit, 'MemWrite'),
            (self.controlUnit, 'BranchEQ'), (self.controlUnit, 'BranchNE'),
            (self.controlUnit, 'LoadImm'), (self.controlUnit, 'ALUOp'), ],
            ['RegDst', 'ALUSrc', 'MemtoReg', 'RegWrite', 'MemRead',
            'MemWrite', 'BranchEQ', 'BranchNE', 'LoadImm', 'ALUOp']
        )

        self.muxWReg.connect(
            [(self.idex, 'inst20-16'), (self.idex, 'inst15-11')],
            ['muxWRegData'],
            [(self.idex, 'RegDst')],
            []
        )

        self.forwardingUnit.connect(
            [(self.idex, 'inst25-21'), (self.idex, 'inst20-16'),
            (self.exmem, 'muxWRegData'), (self.memwb, 'muxWRegData1')],
            [],
            [(self.exmem, 'RegWrite'), (self.memwb, 'RegWrite1')],
            ['ForwardA', 'ForwardB']
        )

        self.muxTripleA.connect(
            [(self.idex, 'reg1Data'), (self.muxDMem, 'muxDMemData'), (self.exmem, 'aluResult')],
            ['muxTripleAData'],
            [(self.forwardingUnit, 'ForwardA')],
            []
        )

        self.muxTripleB.connect(
            [(self.idex, 'reg2Data'), (self.muxDMem, 'muxDMemData'), (self.exmem, 'aluResult')],
            ['muxTripleBData'],
            [(self.forwardingUnit, 'ForwardB')],
            []
        )

        self.muxALU.connect(
            [(self.muxTripleB, 'muxTripleBData'), (self.idex, 'signExAddress')],
            ['muxALUData'],
            [(self.idex, 'ALUSrc')],
            []
        )

        self.shiftLeft2.connect(
            [(self.idex, 'signExAddress')],
            ['shiftedAddress'],
            [],
            []
        )

        self.adder2.connect(
            [(self.idex, 'nextAddress'), (self.shiftLeft2, 'shiftedAddress')],
            ['branchAddress'],
            [],
            []
        )

        self.alu.connect(
            [(self.muxTripleA, 'muxTripleAData'), (self.muxALU, 'muxALUData')],
            ['aluResult'],
            [(self.idex, 'ALUOp')],
            ['Zero']
        )

        self.exmem.connect(
            [(self.adder2, 'branchAddress'), (self.alu, 'aluResult'),
            (self.idex, 'reg2Data'), (self.idex, 'shiftedImmAddress'),
            (self.muxWReg, 'muxWRegData')],
            ['branchAddress', 'aluResult', 'reg2Data', 'shiftedImmAddress', 'muxWRegData'],
            [(self.idex, 'MemtoReg'), (self.idex, 'RegWrite'),
            (self.idex, 'MemRead'), (self.idex, 'MemWrite'),
            (self.idex, 'BranchEQ'), (self.idex, 'BranchNE'),
            (self.idex, 'LoadImm'), (self.alu, 'Zero')],
            ['MemtoReg', 'RegWrite', 'MemRead', 'MemWrite',
            'BranchEQ', 'BranchNE', 'LoadImm', 'Zero', ]
        )

        self.branchCheck.connect(
            [],
            [],
            [(self.exmem, 'BranchEQ'), (self.exmem, 'BranchNE'), (self.exmem, 'Zero')],
            ['BranchSignal']
        )

        self.dataMemory.connect(
            [(self.exmem, 'aluResult'), (self.exmem, 'reg2Data')],
            ['memoryData'],
            [(self.exmem, 'MemRead'), (self.exmem, 'MemWrite')],
            []
        )

        self.memwb.connect(
            [(self.dataMemory, 'memoryData'), (self.exmem, 'aluResult'),
            (self.exmem, 'shiftedImmAddress'), (self.exmem, 'muxWRegData')],
            ['memoryData', 'aluResult', 'shiftedImmAddress', 'muxWRegData1'],
            [(self.exmem, 'MemtoReg'), (self.exmem, 'RegWrite'),
            (self.exmem, 'LoadImm')],
            ['MemtoReg', 'RegWrite1', 'LoadImm']
        )

        self.muxImm.connect(
            [(self.memwb, 'aluResult'), (self.memwb, 'shiftedImmAddress')],
            ['muxImmData'],
            [(self.memwb, 'LoadImm')],
            []
        )

        self.muxDMem.connect(
            [(self.muxImm, 'muxImmData'), (self.memwb, 'memoryData')],
            ['muxDMemData'],
            [(self.memwb, 'MemtoReg')],
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
        self.pc.readControlSignals()
