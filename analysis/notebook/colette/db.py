from tkinter import *
from tkinter import filedialog
import csv
from csv import writer

################################################################################
#                   HELPER FUNCTIONS
################################################################################
behaviorList = ['rt-bil', 'locomotion', 'face-groom', 'rt-ipsi', 'rt-contra']
header = ['Mouse', 'Genotype', 'Session Number', 
          'Real Time Stim Count During 30 Minute Stim Period', 'Bout Count', 
          'Total Stim Count', 'Average Duration', 
          'Stim Count During 30 Minute Stim Period', 'Real Time Accuracy', 
          'Real Time Time Period (minutes)', 'Sham', 'Behavior']

#takes a string and returns a list, where an element is a value separated by comma
def strToList(string):
    result = []
    start = 0
    for i in range(0, len(string)):
        if (i == len(string)-1):
            result.append(string[start:i+1:1])
        if (string[i] == ','):
            result.append(string[start:i:1])
            start = i+1
    return result

# filters given db (database) with given list of mice names, genotype, sham
def filterDB(db, mouseList, genotype, sham):
    result = []

    with open(db, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if (len(mouseList) != 0):
                for mouse in mouseList:
                    if mouse == row[0]:
                        if (genotype == '') or (genotype == row[1]):
                            if (sham == '') or (sham == row[10]):
                                result.append(row)
            else:
                if (genotype == '') or (genotype == row[1]):
                    if (sham == '') or (sham == row[10]):
                        result.append(row)
        csvfile.close()
                            
    print(header)
    for row in result:
        if 'Total Stim Count' not in row:
            print(row)


def addManual(db):
    mouse = str.upper(input('\nenter mouse name\n'))
    genotype = str.upper(input('\nenter mouse genotype\n'))
    sessionNum = input('\nenter session number\n')
    realTimeStimPeriodCount = input('\nenter real time stim count during 30 minute stim period\n')
    boutCount = input('\nenter bout count\n')
    totalStimCount = input('\nenter total stim count\n')
    averageDuration = input('\nenter average duration of behavior\n')
    stimPeriodCount = input('\nenter stim count during 30 min stim period\n')
    realTimeAccuracy = input('\nenter real time accuracy\n')
    realTimeLength = input('\nenter real time timestamp file length (minutes)\n')
    sham = str.lower(input('enter sham? (y/n)\n'))
    print(behaviorList)
    behavior = str.lower(input('\nenter a behavior\n'))
    while(behavior not in behaviorList):
        behavior = str.lower(input('\ninvalid input, try again\n'))
    row = [mouse, genotype, sessionNum, realTimeStimPeriodCount, boutCount,
           totalStimCount, averageDuration, stimPeriodCount, realTimeAccuracy,
           realTimeLength, sham, behavior]
    print('\n',row)
    confirm = str.lower(input('\ndoes this look right? (y/n) once added, cannot be undone\n'))
    if confirm == 'y':
        with open(db, 'a', newline = '') as csvfile:
            writer_object = writer(csvfile)
            writer_object.writerow(row)
            csvfile.close()
        print('\nsuccessfully added a new session')
    else:
        print('\ndid not add session')

def addUpload(db):
    file = filedialog.askopenfilename(multiple = True, title = 'upload data csv\'s')

################################################################################


#db = filedialog.askopenfile(multiple = False, title = 'load db csv')
db = 'csv-db - Sheet1.csv'
option = str.lower(input('\nfilter sessions or add? or end (f/a/e)\n'))

while (option != 'e'):
    while (option != 'f') and (option != 'a') and (option != 'e'):
        option = str.lower(input('\ninvalid input, try again (f/a/e)\n'))
    if (option == 'f'):
        '''
        option 1: filter
        '''
        mouseInput = str.upper(input('\nenter multiple mice names separated by commas (AD6, AD8), or leave blank, or b for back\n'))
        mouseList = []
        while (mouseInput != 'B'):
            if (mouseInput != ''):
                mouseInput = mouseInput.replace(' ', '')
                mouseList = strToList(mouseInput)

            genotypeInput = str.upper(input('\nenter a genotype D1 or D2 or leave blank (D1/D2/)\n'))
            while (genotypeInput != 'D1') and (genotypeInput != 'D2') and (genotypeInput != ''):
                genotypeInput = str.upper(input('\ninvalid, try again (1/2/)\n'))

            shamInput = str.lower(input('\nsham? enter or leave blank (y/n/)\n'))
            while (shamInput != 'y') and (shamInput != 'n') and (shamInput != ''):
                shamInput = str.lower(input('\ninvalid, try again (y/n/)\n'))

            filterDB(db, mouseList, genotypeInput, shamInput)
            mouseInput = str.upper(input('\nenter multiple mice names separated by commas (AD6, AD8), or leave blank, or b for back\n'))

        option = str.lower(input('\nfilter sessions or add? or end (f/a/e)\n'))

    if (option == 'a'):
        '''
        opton 2: add
        '''
        addManual(db)
        option = str.lower(input('\nfilter sessions or add? or end (f/a/e)\n'))

print('\n\nDone!')