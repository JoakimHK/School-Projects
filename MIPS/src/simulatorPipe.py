'''
Code written for inf-2200, University of Tromso
'''

import sys
import time
from mipsSimulatorPipe import MIPSSimulator

def runSimulator(sim):
    total_time = 0

    while (1):
        t1 = time.time()
        sim.tick()
        t2 = time.time()

        total_time += t2 - t1
        sim.printRegisterFile()
        print()
        print('Current address:\t%s' % hex(sim.pc.currentAddress()))
        print('Clock cycles:\t\t%d' % sim.clockCycles())
        print('Time:\t\t\t%f' % total_time)
        #print('\na: %d\tb: %d\n' % (sim.registerFile.register[9], sim.registerFile.register[10]))
        #print()

if __name__ == '__main__':
    assert(len(sys.argv) == 2), 'Usage: python %s memoryFile' % (sys.argv[0],)
    memoryFile = sys.argv[1]

    simulator = MIPSSimulator(memoryFile)
    runSimulator(simulator)
