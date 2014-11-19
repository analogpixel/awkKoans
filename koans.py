import sys
import time
import os.path
import md5
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html
# http://www.darkcoding.net/software/pretty-command-line-console-output-on-unix-in-python-and-go-lang/

currentKoan = 0
currentCmd  = ""
currentMD5  = ""
currentText = ""

class handleKoanChange(FileSystemEventHandler):
  def on_modified(self, event):
        print "hello:" + event.src_path
        print event.event_type

        if currentMD5 == md5.new(str(os.system(currentCmd))).hexdigest():
            nextKoan()

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
    global currentKoan

    currentKoan = int(currentKoan) + 1

    f = open("current", "w")
    f.write(str(currentKoan))
    f.close()

    loadKoan()
    print(currentText)

def loadKoan():
    global currentKoan, currentCmd, currentMD5, currentText

    currentText = clear()
    if os.path.exists("./koans/koan%s" % currentKoan ):
        for line in open("./koans/koan%s" % currentKoan):
            if line[0:2] == "==":
                currentText = currentText + color("35", bold(line[2:].upper().strip() )) + "\n"
            elif line[0:1] == "=":
                currentText = currentText + color("36", bold(line[1:].upper().strip() )) + "\n"
            elif line[0] == "*":
                currentText = currentText + "\t" + color("31", "*") + line[1:]
            elif line[0:5] == "#CMD:":
                currentCmd = line.split(':')[1].strip().replace("%PATH%",os.path.abspath("."))
            elif line[0:5] == "#MD5:":
                currentMD5 = line.split(':')[1].strip()
            elif line[0] == "#":
                continue
            else:
                currentText = currentText + "\t" + line
    else:
        print("Koan %s doesn't exist" % currentKoan)
        sys.exit()

def getCurrent():
    if os.path.exists("current"):
        return int(open("current").read().strip())
    else:
        return 1

if __name__ == "__main__":
    currentKoan = getCurrent()
    loadKoan()
    print(currentText)

    observer = Observer()
    observer.schedule(handleKoanChange(), "./editme", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
