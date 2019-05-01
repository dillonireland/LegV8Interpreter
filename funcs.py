from state import REG, STK, LBS, MEM, flags, printLabels
import state as s

rM = 0
rN = 0
rD = 0
iM = 0

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def get_byte(value, n=0):
    goal = 0xFF
    byte = ((value >> (8 * n)) & goal)
    return byte

#Takes a uint and returns a int64. If the original value would
#require more than 64 bits, MSBs will be dropped until result
#is within range
def s64(value):
    return -(value & 0x8000000000000000) | (value & 0x7fffffffffffffff)

#tested
def add(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    rM = int(args[2][1::])
    REG[rD].int = s64(REG[rN].int + REG[rM].int)
    return

#tested
def addi(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    REG[rD].int = s64(REG[rN].int + s64(iM))
    return

#tested
def adds(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    rM = int(args[2][1::])
    flags = [0]*4
    REG[rD].int = s64(REG[rN].int + REG[rM].int)
    if not REG[rD].int:
        flags[0] = 1
    if REG[rD].int < 0:
        flags[1] = 1
    if(REG[rD].uint < REG[rN].uint or REG[rD].uint < REG[rM].uint):
        flags[2] = 1
    if (REG[rD].int != REG[rN].int + REG[rM].int):
        flags[3] = 1
    #show flags: [0] = Z, [1] = N, [2] = C, [3] = V
    print(flags)
    return

#tested
def addis(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    flags = [0]*4
    REG[rD].int = s64(REG[rN].int + s64(iM))
    if not REG[rD].int:
        flags[0] = 1
    if REG[rD].int < 0:
        flags[1] = 1
    if(REG[rD].uint < REG[rN].uint or REG[rD] < s64(iM).uint):
        flags[2] = 1
    if (REG[rD].int != REG[rN].int + iM):
        flags[3] = 1
    #show flags: [0] = Z, [1] = N, [2] = C, [3] = V
    print(flags)
    return

#tested
def aand(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    rM = int(args[2][1::])
    REG[rD].int = REG[rN].int & REG[rM].int
    return

#tested
def andi(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    REG[rD].int = s64(REG[rN].int & s64(iM))
    return

#tested
def ands(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    rM = int(args[2][1::])
    flags = [0]*4
    REG[rD].int = s64(REG[rN].int & REG[rM].int)
    #show stored result as int and hex
    if not REG[rD].int:
        flags[0] = 1
    if REG[rD].int < 0:
        flags[1] = 1
    print(flags)
    return

#tested
def andis(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    flags = [0]*4
    REG[rD].int = s64(REG[rN].int & s64(iM))
    #show stored result as int and hex
    print(REG[rD].int, ' ', REG[rD])
    if not REG[rD].int:
        flags[0] = 1
    if REG[rD].int < 0:
        flags[1] = 1
    #show flags: [0] = Z, [1] = N, [2] = C, [3] = V
    print(flags)
    return

#tested
def b(args):
    # Find the label location
    if args[0] in LBS:
        s.ip = LBS[args[0]]
    return

#tested
def beq(args):
    if flags[0]:
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def bne(args):
    if not flags[0]:
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def blt(args):
    if flags[1] != flags[3]:
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def ble(args):
    if not(flags[0] == 0 and flags[1] == flags[3]):
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def bgt(args):
    if flags[0] == 0 and flags[1] == flags[3]:
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def bge(args):
    if flags[1] == flags[3]:
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def bhs(args):
    if flags[2]:
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def blo(args):
    if not flags[2]:
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def bls(args):
    if not(flags[0] == 0 and flags[2] == 1):
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def bhi(args):
    if not flags[0] and flags[2]:
        if args[0] in LBS:
            s.ip = LBS[args[0]]
    return

def bl(args):
    REG[30].int = s.ip + 1
    if args[0] in LBS:
        s.ip = LBS[args[0]]
    return

#tested
def br(args):
    rD = int(args[0][1::])
    s.ip = rD
    return

#tested
def cbz(args):
    rT = int(args[0][1::])
    if REG[rT].int == 0:
        if args[1] in LBS:
            s.ip = LBS[args[1]]
    return

#tested
def cbnz(args):
    rT = int(args[0][1::])
    if REG[rT].int != 0:
        if args[1] in LBS:
            s.ip = LBS[args[1]]
    return

def cmpi(args):
    print(args)
    rT = int(args[0][1::])
    if REG[rT].int == int(args[1]):
        if args[1] in LBS:
            s.ip = LBS[args[1]]
    return

def eor(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    rM = int(args[2][1::])
    REG[rD].int = REG[rN].int ^ REG[rM].int
    return

def eori(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    REG[rD].int = REG[rN].int ^ iM
    return

def ldur(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])

    REG[rT].int = mem[s64(REG[rN].int + iM)]

    return

def ldurb(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])

    REG[rT].int = get_byte(mem[s64(REG[rN].int + iM)], 0)

    return

def ldurh(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])


    REG[rT].int = get_byte(mem[s64(REG[rN].int + iM)], 1)
    return

def ldursw(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])

    REG[rT].int = s64(get_byte(mem[s64(REG[rN].int + iM)], 2))
    return

def ldxr(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])

    REG[rT].int = mem[s64(REG[rN].int + iM)]
    REG[9] = 1
    return

def lsl(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    REG[rD].int = REG[rN].int << iM
    return

def lsr(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    REG[rD].int = REG[rN].int >> iM
    return

def orr(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    rM = int(args[2][1::])
    REG[rD].int = REG[rN].int | REG[rM].int
    return

def orri(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    REG[rD].int = REG[rN].int | s64(iM)
    return

def sub(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    rM = int(args[2][1::])
    REG[rD].int = s64(REG[rN].int - REG[rM].int)
    return

#tested
def subi(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    REG[rD].int = s64(REG[rN].int - s64(iM))
    return

#tested
def subs(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    rM = int(args[2][1::])
    flags = [0]*4
    REG[rD].int = s64(REG[rN].int - REG[rM].int)
    if not REG[rD].int:
        flags[0] = 1
    if REG[rD].int < 0:
        flags[1] = 1
    if(REG[rN].uint < REG[rM].uint):
            flags[2] = 1
    if (REG[rD].int != REG[rN].int - REG[rM].int):
        flags[3] = 1
    return

#tested
def subis(args):
    rD = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    flags = [0]*4
    REG[rD].int = s64(REG[rN].int - s64(iM))
    if not REG[rD].int:
        flags[0] = 1
    if REG[rD].int < 0:
        flags[1] = 1
    if(REG[rN].uint < iM):
        flags[2] = 1
    if (REG[rD].int != REG[rN].int - s64(iM)):
        flags[3] = 1
    return

def stur(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])
    print(rT, rN, iM)
    print(REG[rN].int + iM)
    if rN == 28:
        STK[REG[rN].int + iM].int = REG[rT].int
    else:
        mem[REG[rN].int + iM].int = REG[rT].int
    return

def sturb(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])

    if rN == 28:
        STK[REG[rN].int + iM] = get_byte(REG[rT].int, 0)
    else:
        mem[REG[rN].int + iM]= get_byte(REG[rT].int, 0)

    return

def sturh(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])

    if rN == 28:
        STK[REG[rN].int + iM] = get_byte(REG[rT].int, 1)
    else:
        mem[REG[rN].int + iM]= get_byte(REG[rT].int, 1)
    return

def sturw(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])
    iM = int(args[2])

    if rN == 28:
        STK[REG[rN].int + iM] = get_byte(REG[rT].int, 2)
    else:
        mem[REG[rN].int + iM]= get_byte(REG[rT].int, 2)
    return

def stxr(args):
    rT = int(args[0][1::])
    rN = int(args[1][1::])

    if not REG[9]:
        if rN == 28:
            STK[REG[rN].int] = rT
        else:
            mem[REG[rN].int]= REG[rT].int
    return
