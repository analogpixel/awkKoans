import sys
import time
import os.path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html
# http://www.darkcoding.net/software/pretty-command-line-console-output-on-unix-in-python-and-go-lang/

class handleKoanChange(FileSystemEventHandler):
  def on_modified(self, event):
        print "hello:" + event.src_path
        print event.event_type

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
    x = currentKoan() + 1
    open("current", "w").write(str(x))
    
def currentKoan():
    """
    returns the current koan you are working on
    """
    if os.path.exists("current"):
        return int(open("current").read().strip())
    else:
        return 1
        
def readKoan(num):
    data = clear()
    for line in open("./koans/koan%s" % num):
        if line[0:2] == "==":
            data = data + color("35", bold(line[2:].upper().strip() )) + "\n"
        elif line[0:1] == "=":
            data = data + color("36", bold(line[1:].upper().strip() )) + "\n"
        elif line[0] == "*":
            data = data + "\t" + color("31", "*") + line[1:]
        elif line[0] == "#":
            continue
        else:
            data = data + "\t" + line
            
    return data

def printKoan(num):
    """
    print out koan number num to the screen
    """
    if os.path.exists("./koans/koan%s" % num ):
        data = readKoan(num)
        print data
    else:
        print "Koan %s doesn't exist" % num
        
if __name__ == "__main__":
    
    printKoan( currentKoan() )
    
    observer = Observer()
    observer.schedule(handleKoanChange(), "./editme", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()