#!/usr/bin/python

import sys
import time
import os.path
import subprocess

# http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html
# http://www.darkcoding.net/software/pretty-command-line-console-output-on-unix-in-python-and-go-lang/

currentKoan  = 0
currentCmd   = ""
currentMD5   = ""
currentText  = ""
inputString  = ""
outputString = ""
currentMTime = ""
sampleString = ""

# the order the Koans are given
koanIndex    =  [
                "catText",              # echo every line that comes in
                "simplePatternMatch",   # match a word
                "beginingOfLineMatch"   # match a word that starts at begining of line
                ]

def clear():
    return u'\033[0;0H\033[2J'

def bold(msg):
    return u'\033[1m%s\033[0m' % msg

def color(this_color, string):
    """
    http://ascii-table.com/ansi-escape-sequences.php
    colors 30-37
    """
    return "\033[" + this_color + "m" + string + "\033[0m"

def nextKoan():
    global currentKoan, currentTime

    currentKoan = int(currentKoan) + 1

    f = open("current", "w")
    f.write(str(currentKoan))
    f.close()

    if currentKoan >= len(koanIndex):
        print("Solved all")
        sys.exit()

    loadKoan()
    currentTime = getKoanTime()

    print(currentText)

def loadKoan():
    global currentKoan, currentCmd, currentMD5, currentText, inputString, outputString, sampleString, currentMTime

    readInput    = False
    readOutput   = False
    readSample   = False
    inputString  = ""
    outputString = ""
    sampleString = ""
    currentText  = clear()

    if os.path.exists("./koans/%s" % koanIndex[currentKoan] ):
        for line in open("./koans/%s" % koanIndex[currentKoan] ):

            if readInput:
                if line[0:5] == "##EOI":
                    readInput = False
                    continue
                else:
                    inputString = inputString + line
                    continue

            if readOutput:
                if line[0:5] == "##EOO":
                    readOutput = False
                    continue
                else:
                    outputString = outputString + line
                    continue

            if readSample:
                if line[0:5] == "##EOS":
                    readSample = False
                    continue
                else:
                    sampleString = sampleString + line
                    continue


            if line[0:2] == "==":
                currentText = currentText + color("35", bold(line[2:].upper().strip() )) + "\n"
            elif line[0:1] == "=":
                currentText = currentText + color("36", bold(line[1:].upper().strip() )) + "\n"
            elif line[0] == "*":
                currentText = currentText + "\t" + color("31", "*") + line[1:]
            elif line[0:5] == "#FILE":
                currentText = currentText + color("35", bold("File To edit")) + "\n\t" +  koanIndex[currentKoan] + ".awk"
            elif line[0:5] == "#CMD:":
                currentCmd = line.split(':')[1].strip().replace("%PATH%",os.path.abspath("."))
            elif line[0:7] == "##INPUT":
                readInput = True
            elif line[0:8] == "##OUTPUT":
                readOutput = True
            elif line[0:8] == "##SAMPLE":
                readSample = True
            elif line[0] == "#":
                continue
            else:
                currentText = currentText + "\t" + line

        currentText = currentText + color("35", bold("Sample Input")) + "\n"
        for line in  inputString.split("\n")[0:3]:
            currentText = currentText + "\t%s\n" % line

        currentText = currentText + color("35", bold("Sample Output")) + "\n"
        for line in  outputString.split("\n")[0:3]:
            currentText = currentText + "\t%s\n" % line

        # load the current time and create the file if
        # it doesn't already exist
        currentMTime = getKoanTime()

    else:
        print("Koan %s doesn't exist" % currentKoan)
        sys.exit()


def getCurrent():
    """
    Load the current koan from the file current
    if you are at the end of the koans, then stop
    """
    current = -1

    if os.path.exists("current"):
        current = int(open("current").read().strip())
    else:
        current =  0

    if current >= len(koanIndex):
        print("Solved all")
        sys.exit()

    return current

def getKoanTime():
    """
    If the file exists return the curent mtime for the file
    otherwise create the file from the currentKoan index
    and then return the mtime.
    """
    if not os.path.exists("%s.awk" % koanIndex[currentKoan] ):
        f = open("%s.awk" % koanIndex[currentKoan] ,"w")
        print(sampleString)
        f.write(sampleString)
        f.close()
    return os.path.getmtime("%s.awk" % koanIndex[currentKoan] )

def testCommand():
    """
    Test the current Koan
    """
    proc = subprocess.Popen(["awk","-f", "%s.awk" % koanIndex[currentKoan]], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.stdin.write(inputString)
    out, err = proc.communicate()

    return out == outputString

if __name__ == "__main__":
    currentKoan = getCurrent()
    loadKoan()
    print(currentText)

    while True:
        if getKoanTime() != currentMTime:
            currentMTime = getKoanTime()
            if testCommand():
                nextKoan()
            else:
                print("booo")

        time.sleep(1)
