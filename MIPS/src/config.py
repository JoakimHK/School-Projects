"""
This file contains global configuration constants
Author: Brede Eder Murberg
"""



# ALU Operations
ALU_ADD = 2
ALU_ADDU = 3 #CHECK
ALU_SUB = 6
ALU_SUBU = 5 #CHECK
ALU_AND = 0
ALU_OR = 1
ALU_NOR = 4 #CHECK
ALU_SLT = 7

# Opcode
R_TYPE = 0
LW = 35
SW = 43
BEQ = 4
BNE = 5
JMP = 2
LUI = 15
ADDI = 8
ADDIU = 9
NOP = 63



# Funct
ADD = 0x20
ADDU = 0x21
SUB = 0x22
SUBU = 0x23
AND = 0x24
OR = 0x25
NOR = 0x27
SLT = 0x2a

BREAK = 0xd

FIRST_5_BITS = 0x1f
FIRST_6_BITS = 0x3f
FIRST_16_BITS = 0xffff
FIRST_26_BITS = 0x3ffffff
