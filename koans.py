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
currentMTime  = ""

def clear():
    return u'\033[2J'

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

    currentTime = getKoanTime()

    f = open("current", "w")
    f.write(str(currentKoan))
    f.close()

    loadKoan()
    print(currentText)

def loadKoan():
    global currentKoan, currentCmd, currentMD5, currentText, inputString, outputString

    readInput    = False
    readOutput   = False
    inputString  = ""
    outputString = ""
    currentText = clear()

    if os.path.exists("./koans/koan%s" % currentKoan ):
        for line in open("./koans/koan%s" % currentKoan):

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

            if line[0:2] == "==":
                currentText = currentText + color("35", bold(line[2:].upper().strip() )) + "\n"
            elif line[0:1] == "=":
                currentText = currentText + color("36", bold(line[1:].upper().strip() )) + "\n"
            elif line[0] == "*":
                currentText = currentText + "\t" + color("31", "*") + line[1:]
            elif line[0:5] == "#CMD:":
                currentCmd = line.split(':')[1].strip().replace("%PATH%",os.path.abspath("."))
            elif line[0:7] == "##INPUT":
                readInput = True
            elif line[0:8] == "##OUTPUT":
                readOutput = True
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


    else:
        print("Koan %s doesn't exist" % currentKoan)
        sys.exit()


def getCurrent():
    if os.path.exists("current"):
        return int(open("current").read().strip())
    else:
        return 1

def getKoanTime():
    if os.path.exists("editme/koan%s.awk" % currentKoan ):
        return os.path.getmtime("editme/koan%s.awk" % currentKoan )
    else:
        return 0

def testCommand():
    proc = subprocess.Popen(["awk","-f", "editme/koan%s.awk" % currentKoan], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.stdin.write(inputString)
    out, err = proc.communicate()

    return out == outputString

if __name__ == "__main__":
    currentKoan = getCurrent()
    currentTime = getKoanTime()
    loadKoan()
    print(currentText)

    while True:
        if getKoanTime() != currentTime:
            currentTime = getKoanTime()
            if testCommand():
                nextKoan()
            else:
                print("booo")

        time.sleep(1)
