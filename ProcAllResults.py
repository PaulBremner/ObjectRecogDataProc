import os

datadir = 'G:\Python_ws\ObjectRecorDataProc\\response_data'
datafiles = os.listdir(datadir)

for datafile in datafiles:
    os.system("python DataProcMain " + datadir + '\\' + datafile)