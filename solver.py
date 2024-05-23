import numpy as np
import time

# return columns' lists of cells
allColumns = [[(i, j) for j in range(9)] for i in range(9)]

# return rows' list of cells
allRows = [[(i, j) for i in range(9)] for j in range(9)]

# return blocks' list of cells
alllocks = [[((i//3) * 3 + j//3, (i % 3)*3+j % 3)
               for j in range(9)] for i in range(9)]

# combine three
allHouses = allColumns+allRows+alllocks

# returns list [(0,0), (0,1) .. (a-1,b-1)], kind of like "range" but for 2d array
def range2(a, b):
    permutations = []
    for j in range(b):
        for i in range(a):
            permutations.append((i, j))
    return permutations


# Adding candidates instead of zeros
def pencilInNumbers(puzzle):
    sudoku = np.empty((9, 9), dtype=object)
    for (j, i) in range2(9, 9):
        if puzzle[i, j] != 0:
            sudoku[i][j] = [puzzle[i, j], ]
        else:
            sudoku[i][j] = [i for i in range(1, 10)]
    return sudoku

# Count solved cells
def nSolved(sudoku):
    solved = 0
    for (i, j) in range2(9, 9):
        if len(sudoku[i, j]) == 1:
            solved += 1
    return solved

# Count remaining unsolved candidates to remove
def nToRemove(sudoku):
    toRemove = 0
    for (i, j) in range2(9, 9):
        toRemove += len(sudoku[i, j])-1
    return toRemove

"""
# Print full sudoku, with all candidates (rather messy)
def print_sudoku(sudoku):
    for j in range(9):
        out_string = "|"
        out_string2 = " " * 10 + "|"
        for i in range(9):
            if len(sudoku[i, j]) == 1:
                out_string2 += str(sudoku[i, j][0])+" "
            else:
                out_string2 += "  "

            for k in range(len(sudoku[i, j])):
                out_string += str(sudoku[i, j][k])
            for k in range(10 - len(sudoku[i, j])):
                out_string += " "
            if (i + 1) % 3 == 0:
                out_string += " | "
                out_string2 += "|"

        if (j) % 3 == 0:
            print ("-" * 99, " " * 10, "-" * 22)
        print (out_string, out_string2)
    print ("-" * 99,  " " * 10, "-" * 22)
"""
# Simple Elimination
# If there is one number in cell - remove it from the house
def simpleElimination(sudoku):
    count = 0
    for group in allHouses:
        for cell in group:
            if len(sudoku[cell]) == 1:
                for cell2 in group:
                    if sudoku[cell][0] in sudoku[cell2] and cell2 != cell:
                        sudoku[cell2].remove(sudoku[cell][0])
                        count += 1
    return count

# CSP
# brute force CSP solution for each cell: it covers hidden and naked pairs, triples, quads
def cspList(inp):

    perm = []

    # recursive func to get all permutations
    def appendPermutations(sofar):
        nonlocal inp
        for n in inp[len(sofar)]:
            if len(sofar) == len(inp) - 1:
                perm.append(sofar + [n])
            else:
                appendPermutations(sofar + [n])

    appendPermutations([])

    # filter out impossibble ones
    for i in range(len(perm))[::-1]:
        if len(perm[i]) != len(set(perm[i])):
            del perm[i]

    # which values are still there?
    out = []
    for i in range(len(inp)):
        out.append([])
        for n in range(10):
            for p in perm:
                if p[i] == n and n not in out[i]:
                    out[i].append(n)
    return out

def csp(s):
    count = 0
    for group in allHouses:
        house = []
        for cell in group:
            house.append(s[cell])
        house_csp = cspList(house)
        if house_csp != house:
            for i in range(len(group)):
                if s[group[i]] != house_csp[i]:
                    count += len(s[group[i]]) - len(house_csp[i])
                    s[group[i]] = house_csp[i]
    return count

# Backtracking
# Helper: list of houses of each cell
# To optimize checking for broken puzzle
def cellInHouse():
    out = {(-1, -1):[]}
    for (i, j) in range2(9, 9):
        out[(i,j)] = []
        for h in allHouses:
            if (i, j) in h:
                out[(i, j)].append(h)
    return out

def getNextCellToForce(s):
    for (i, j) in range2(9, 9):
        if len(s[i, j])>1:
            return (i, j)


def bruteForce(s, verbose):
    solution = []
    t = time.time()
    iterCounter = 0

    cellHouse = cellInHouse()
    
    def isBroken(s, lastCell):
        for house in cellHouse[lastCell]:
            houseData = []
            for cell in house:
                if len(s[cell]) == 1:
                    houseData.append(s[cell][0])
            if len(houseData) != len(set(houseData)):
                return True
        return False

    def iteration(s, lastCell=(-1,-1)):
        nonlocal solution
        nonlocal iterCounter

        iterCounter += 1
        if iterCounter%100000 == 0 and verbose:
            print ("Iteration", iterCounter)

        # is broken - return fail
        if isBroken(s, lastCell):
            return -1

        # is solved - return success
        if nToRemove(s) == 0:
            #print ("Solved")
            solution = s
            return 1

        # find next unsolved cell
        nextCell = getNextCellToForce(s)

        # apply all options recursively
        for n in s[nextCell]:
            scopy = s.copy()
            scopy[nextCell] = [n]
            result = iteration(scopy, nextCell)
            if result == 1:
                return

    iteration(s)

    if len(solution)>0:
        if verbose:
            print ("Backtracking took:", time.time()-t, "seconds, with", iterCounter, "attempts made")
        return solution

    # this is only if puzzle is broken and couldn't be forced
    print ("The puzzle appears to be broken")
    return s


# Main Solver
def solve(originalPuzzle, verbose):

    report = [0]*10

    puzzle = pencilInNumbers(originalPuzzle)
    solved = nSolved(puzzle)
    toRemove = nToRemove(puzzle)
    if verbose:
        print ("Initial puzzle: complete cells", solved, "/81. Candidates to remove:", toRemove)

    t = time.time()

    # Control how solver goes thorugh metods:
    # False - go back to previous method if the next one yeld results
    # True - try all methods one by one and then go back
    allAtOnce = True

    while toRemove != 0:
        rStep = 0
        r0 = simpleElimination(puzzle)
        report[0] += r0
        rStep += r0

        if allAtOnce or rStep == 0:
            r2 = csp(puzzle)
            report[2] += r2
            rStep += r2

        # check state
        solved = nSolved(puzzle)
        toRemove = nToRemove(puzzle)

        # Nothing helped, logic failed
        if rStep == 0:
            break

    #printSudoku(puzzle)
    if verbose:
        print ("Solved with logic: number of complete cells", solved, "/81. Candidates to remove:", toRemove)
        print ("Logic part took:", time.time() - t)

    if toRemove > 0:
        forBrute = nToRemove(puzzle)
        puzzle = bruteForce(puzzle, verbose)
        report[9] += forBrute

    # Report:
    legend = [
            'Simple elimination',
            'CSP',
            'Backtracking']
    if verbose:
        print ("Methods used:")
        for i in range(len(legend)):
            print ("\t", i, legend[i], ":", report[i])
    return puzzle

# Interface to convert line format to internal format and back
def lineFromSolution(sol):
    out = ""
    for a in sol:
        for b in a:
            out += str(b[0])
    return out
def solveFromLine(line, verbose=False):
    sStr = ""
    rawS = line[0:81]
    for ch in rawS:
        sStr += ch + " "
    sNp1 = np.fromstring(sStr, dtype=int, count=-1, sep=' ')
    sNp = np.reshape(sNp1, (9, 9))
    return lineFromSolution(solve(sNp, verbose))             


if __name__ == "__main__":

    print ("Sudoku Solver Demo")

    puzzles = [
        ("Easy",
        '000000000000003085001020000000507000004000100090000000500000073002010000000040009'
        ),
        ("Medium",
        '100070009008096300050000020010000000940060072000000040030000080004720100200050003'
        ),
        ("Escargot",
        "100007090030020008009600500005300900010080002600004000300000010041000007007000300"
        ),
        ("Steering Wheel",
        "000102000060000070008000900400000003050007000200080001009000805070000060000304000"
        ),
        ("Arto Inkala",
        "800000000003600000070090200050007000000045700000100030001000068008500010090000400"
        )
    ]

    for puzzleName, puzzle in puzzles:
        print ("Puzzle", puzzleName)
        print (puzzle)
        solution = solveFromLine(puzzle, verbose=True)
        print (solution)
        print ("="*80)
