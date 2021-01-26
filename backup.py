import os
import time
import shutil

def main():
    print("Loading backup queue...")
    tasks = ""
    with open("TASKS.txt", "r") as taskList:
        tasks = taskList.readlines()
    taskCount = len(tasks) // 3
    print("Done. " + str(taskCount) + " backups queued.")
    print()

    for i in range(taskCount):
        source = tasks[(i * 3)].replace("\n", "")
        destination = tasks[(i * 3) + 1].replace("\n", "")
        printDetails = True
        if int(tasks[(i * 3) + 2]) == 0:
            printDetails = False
        print("Loading backup " + str(i + 1) + "/" + str(taskCount) + " details...")
        printTaskSummary(source, destination)
        print("Detailed reporting:", printDetails)
        print("Beginning backup " + str(i + 1) + "/" + str(taskCount) + " in 10 seconds.")
        time.sleep(10)
        print("Running backup #" + str(i + 1) + "...")
        print("-" * 50)
        startTime = time.time()
        resultTuple = consolDirectories(source, destination, "  ", 1, printDetails)
        print("-" * 50)
        print("Backup #" + str(i + 1) + " finished. (" + "{:.2f}".format(time.time() - startTime) + " sec.)")
        print(str(resultTuple[1]) + " folder and " + str(resultTuple[0]) + " file operations completed.")
        print("\n\n")
        
    
def consolDirectories(src, dst, indent, depth, printDetails):
    startTime = time.time()
    depthFormat = "Depth: {:<2} ".format(depth)
    fileActions = 0
    folderActions = 0
    print(depthFormat + indent + "[@] Checking " + src + "...")
    #look over src files and copy over
    for file in os.listdir(src):
        srcPath = os.path.join(src, file)
        dstPath = os.path.join(dst, file)
        #if src file is file
        if os.path.isfile(srcPath):
            #check if copy exists by name
            if os.path.isfile(dstPath):
                None
            #if no copy found, copy over
            else:
                if(printDetails):
                    print(depthFormat + indent + "[+] Copying  " + srcPath)
                fileActions = fileActions + 1
                shutil.copy2(srcPath, dstPath)
        elif os.path.isdir(srcPath):
            #check if copy of dir exists by name
            if os.path.isdir(dstPath):
                None
            #if no copy found, copy over
            else:
                if(printDetails):
                    print(depthFormat + indent + "[+] Copying  " + srcPath)
                folderActions = folderActions + 1
                os.mkdir(dstPath)
            #in both cases check that directory
            folderTuple = consolDirectories(srcPath, dstPath, indent + " ", depth + 1, printDetails)
            fileActions = fileActions + folderTuple[0]
            folderActions = folderActions + folderTuple[1]
    #look over dst files and remove ones not found in src
    for file in os.listdir(dst):
        srcPath = os.path.join(src, file)
        dstPath = os.path.join(dst, file)
        #if dst file is file
        if os.path.isfile(dstPath):
            #check if copy exists by name
            if os.path.isfile(srcPath):
                None
            #if no copy found, remove
            else:
                if(printDetails):
                    print(depthFormat + indent + "[-] Removing  " + dstPath)
                fileActions = fileActions + 1
                os.remove(dstPath)
        elif os.path.isdir(dstPath):
            if os.path.isdir(srcPath):
                None
            else:
                if(printDetails):
                    print(depthFormat + indent + "[-] Removing  " + dstPath)
                folderActions = folderActions + 1
                shutil.rmtree(dstPath)
            
            
                
            
        
    print(depthFormat + indent + "[X] Finished " + src)
    formatTime = "{:.2f}".format(time.time() - startTime)
    print((" " * len(depthFormat)) + indent + "    (" + formatTime + " sec.)")
    return (fileActions, folderActions)
    
def getSize(path):
    size = 0
    for file in os.listdir(path):
        full = os.path.join(path, file)
        if os.path.isdir(full):
            size = size + getSize(full)
        else:
            size = size + os.path.getsize(full)
    return size

def printTaskSummary(source, destination):
    startTime = time.time()
    srcSizeInt = getSize(source)
    dstSizeInt = getSize(destination)
    labelLength = max(len(source), len(destination), len(str(srcSizeInt)) + 3, len(str(dstSizeInt)) + 3)
    srcFormat = ("{:<" + str(labelLength) + "}").format(source)
    srcSize = ("{:>" + str(labelLength - 3) + "} MB").format(srcSizeInt // 1000000)
    destFormat = ("{:<" + str(labelLength) + "}").format(destination)
    destSize = ("{:>" + str(labelLength - 3) + "} MB").format(dstSizeInt // 1000000)
    print("  +-" + ("-" * (labelLength + 13)) + "-+")
    print("  | Source:      " + srcFormat + " |")
    print("  |    Size:     " + srcSize + " |")
    separator = (" -" * ((labelLength + 15) // 2)) + (" " * ((labelLength + 1) % 2))
    print("  |" + separator + "|")
    print("  | Destination: " + destFormat + " |")
    print("  |    Size:     " + destSize + " |")
    print("  +-" + ("-" * (labelLength + 13)) + "-+")
    print("  ({:.2f}".format(time.time() - startTime) + " sec.)")

main()