
import pysftp
import os 
from datetime import datetime
import sys
from time import sleep
import pyodbc
class SFTPCLIENT:
    def __init__(self, IP: str = None, USER: str = None,PASS: str = None, LOCATION: str = os.getcwd()) -> None:
        self.IP = IP
        self.USER= USER
        self.PASS= PASS
        self.NOW = datetime.now()
        self.LOCATION = LOCATION
        self.__DoesLOCATIONExist__()
        if IP and USER and PASS and self.LOCATION:
            pass
            self.CUR = self.__DIRECTCONNECT__()
            self.SelectFolder()
            self.main()
    #connect to SFTP server
    def __DIRECTCONNECT__(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        try:
            RT = pysftp.Connection(host=self.IP, username=self.USER, password=self.PASS,cnopts=cnopts, port=22)  
            print('Logged In Successfully')
            return RT
        except pysftp.exceptions.ConnectionException:
            #LOG sftp line 34 LOST CONNECTION pysftp.exceptions.ConnectionException
            self.flag = False
            return
        except pysftp.paramiko.ssh_exception.AuthenticationException:
            #LOG sftp line 38 AUTH FAIL pysftp.paramiko.ssh_exception.AuthenticationException
            print('Failed To Login Please Try Again')
    @staticmethod
    def __getSERVERFileList__(CURSOR):
            try:
                SERVERDIR__ = CURSOR.listdir('outbound')
            except FileNotFoundError:
                #LOG sftp line 48 FileNotFoundError COULD NOT GRAB FILE LSIT FROM SERVER
                return -1
            else:
                return SERVERDIR__
    def __DoesLOCATIONExist__(self):
        if os.path.isdir(self.LOCATION):
            #LocationGood!
            pass
        else:
            self.LOCATION = None # <--- Will end Program
    def SelectFolder(self):
        self.TODAYFOLDER = self.LOCATION + '\\' + str(self.NOW.year)
        if os.path.isdir(self.TODAYFOLDER):
            #LocationGood!
            pass
        else:
            os.mkdir(self.TODAYFOLDER)
        self.TODAYFOLDER += '\\' + str(self.NOW.month)
        if os.path.isdir(self.TODAYFOLDER):
            #LocationGood!
            pass
        else:
            os.mkdir(self.TODAYFOLDER)
        self.TODAYFOLDER +=  '\\' + str(self.NOW.day)
        if os.path.isdir(self.TODAYFOLDER):
            #LocationGood!
            pass
        else:
            os.mkdir(self.TODAYFOLDER)
    #wrapper function to run "module"
    def main(self) -> None:
        SERVERFileList = self.__getSERVERFileList__(self.CUR)
        TodaysFiles = os.listdir(self.TODAYFOLDER)
        print(SERVERFileList)
        print(TodaysFiles)
        for SERVERFileName in SERVERFileList:
            if SERVERFileName not in TodaysFiles:
                with self.CUR.cd('outbound'):
                        self.CUR.get(SERVERFileName, self.TODAYFOLDER+'\\'+str(SERVERFileName))
                        self.CUR.remove(SERVERFileName)
#added functionality to be ran from command line
if __name__ == '__main__':
    try:
        argIP = sys.argv[1]
        argUSER = sys.argv[2]
        argPASS = sys.argv[3]    
    except:
        #defaulting to command mode 
        #SFTPCLIENT()
        pass
    else:
        try:
            argLOCATION = sys.argv[4]
        except:
            SFTPCLIENT(argIP, argUSER, argPASS)
        else:
            SFTPCLIENT(argIP, argUSER, argPASS, argLOCATION)
