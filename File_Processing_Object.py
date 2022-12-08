from __future__ import print_function

'''
John Griffin Harrington

Project - File Processing Object

The script below to does the following:
1) Creates a class named FileProcessor
   a) The Init method shall:
      i) verify the file exists
      ii) Extract key file system metadata from the file
          and store them as instance attribute
          i.e. FilePath, FileSize, MAC Times, Owner, Mode etc.
   b) Creates a GetFileHeader Method which will
      i) Extract the first 20 bytes of the header
         and store them in an instance attribute
   c) Creates a PrintFileDetails Method which will
      i) Print the metadata
      ii) Print the hex representation of the header
      
2) Demonstrates the use of the new class
   a) prompt the user for a directory path
   b) using the os.listdir() method extract the filenames from the directory path
   c) Loop through each filename and instantiate and object using the FileProcessor Class
   d) Using the object
      i) invoke the GetFileHeader Method
      ii) invoke the PrintFileDetails Method

'''

import os
import hashlib 
import time
import sys
from binascii import hexlify

class FileProcessor:
    #FileProcessor Class Definition
    
    def __init__(self, filePath): # Provide path
        
        try: 
            self.filePath = filePath
            self.absPath = os.path.abspath(filePath)
            
            if os.path.isfile(self.absPath) and os.access(self.absPath, os.R_OK):
                
                stats = os.stat(self.absPath)
                self.filePath = self.absPath
                self.fileSize = stats.st_size
                self.fileCreateTime = time.ctime(stats.st_ctime)
                self.fileModifiedTime = time.ctime(stats.st_mtime)
                self.fileAccessTime = time.ctime(stats.st_atime)
                self.fileMode = '{:016b}'.format(stats.st_mode)
                self.fileUID = stats.st_uid
                self.fileHeader = ''
                
                self.status = 'OK'
                
            else:
                self.status = "File not accessible"
                
        except Exception as err:
            self.status = err 
            
    def GetFileHeader (self):
        with open(self.absPath, 'rb') as binFile:
            header = binFile.read(20)
            self.fileHeader = hexlify(header)
            
    def PrintFileDetails(self):
        if os.path.isfile(self.absPath):
            print("Path:                ", self.absPath)
            print("File Size:           ", '{:,}'.format(self.fileSize), 'Bytes')
            print("File Created Time:   ", self.fileCreateTime)
            print("File Modified Time:  ", self.fileModifiedTime)
            print("File Access Time:    ", self.fileAccessTime)
            print("File Mode:           ", self.fileMode)
            print("File Owner:          ", self.fileUID)
            print("File Header:         ", self.fileHeader)
            
        else:
            print("Skip:   ", self.absPath)
            
            
def main():
    
    directory = input("Enter directory to process: ")
    fileList = os.listdir(directory)
    
    for eachFile in fileList:
        
        print("\nProcessing File...", eachFile)
        obj = FileProcessor(eachFile)
        if obj.status == 'OK':
            obj.GetFileHeader()
            obj.PrintFileDetails()
        else:
            print("Exception: ", eachFile, obj.status)
            
    print("\nScript End")
    
if __name__ == '__main__':
    main()