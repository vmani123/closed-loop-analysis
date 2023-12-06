from tkinter import *
from tkinter import filedialog
import csv
from csv import writer

################################################################################
#                   HELPER FUNCTIONS
################################################################################
behaviorList = ['right-turn', 'locomotion', 'face-groom']
fiberList = ['bilateral', 'ipsilateral', 'contralateral']
header = ['Mouse', 'Genotype', 'Date (if known)', 'Stim Behavior', 'Sham y/n',
          'Session Number', 'Fiber Connection', 'right-turn Bout Count', 
          'right-turn Stim Count', 'right-turn Average Duration', 
          'right-turn Stim in 30 min Stim Period', 'locomotion Bout Count',
          'locomotion Stim Count', 'locomotion Average Duration',
          'locomotion Stim in 30 min Stim Period', 'face-groom Bout Count',
          'face-groom Stim Count', 'face-groom Average Duration',
          'face-groom Stim in 30 min Stim Period', 'other-groom Bout Count',
          'other-groom Stim Count', 'other-groom Average Duration']

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
# behavior
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
                    if (sham == '') or (sham == row[4]):
                        result.append(row)
        csvfile.close()
                            
    print(header)
    for row in result:
        if 'Total Stim Count' not in row:
            print(row)


def addManual(db):
    mouse = str.upper(input('\nenter mouse name\n'))
    genotype = str.upper(input('\nenter mouse genotype\n'))
    date = input('\nenter a date if known (mm/dd/yy)\n')
    print(behaviorList)
    stimBehavior = str.lower(input('\nenter a behavior\n'))
    while(stimBehavior not in behaviorList):
        behavior = str.lower(input('\ninvalid input, try again\n'))
    sham = str.lower(input('enter sham? (y/n)\n'))
    sessionNum = input('\nenter session number\n')
    print(fiberList)
    fiberConnection = str.lower(input('\nenter a connection\n'))
    while(fiberConnection not in fiberList):
        fiberConnection = str.lower(input('\ninvalid input, try again\n'))
    rtBoutCount = input('\nenter right-turn Bout Count\n')
    rtStimCount = input('\nenter right-turn Stim Count\n')
    rtAD = input('\nenter right-turn Average Duration (s)\n')
    rtStimPeriodCount = input('\nenter right-turn Stim Count during 30 minute Stim Period')
    locoBoutCount = input('\nenter locomotion Bout Count\n')
    locoStimCount = input('\nenter locomotion Stim Count\n')
    locoAD = input('\nenter locomotion Average Duration (s)\n')
    locoStimPeriodCount = input('\nenter locomotion Stim Count during 30 minute Stim Period')
    fgBoutCount = input('\nenter face-groom Bout Count\n')
    fgStimCount = input('\nenter face-groom Stim Count\n')
    fgAD = input('\nenter face-groom Average Duration (s)\n')
    fgStimPeriodCount = input('\nenter face-groom Stim Count during 30 minute Stim Period')
    ogBoutCount = input('\nenter other-groom Bout Count\n')
    ogStimCount = input('\nenter other-groom Stim Count\n')
    ogAD = input('\nenter other-groom Average Duration (s)\n')
    ogStimPeriodCount = input('\nenter other-groom Stim Count during 30 minute Stim Period')
    aoBoutCount = input('\nenter all-other Bout Count\n')
    aoStimCount = input('\nenter all-other Stim Count\n')
    aoAD = input('\nenter all-other Average Duration (s)\n')
    aoStimPeriodCount = input('\nenter all-other Stim Count during 30 minute Stim Period')
    
    row = [mouse, genotype, date, stimBehavior, sham, sessionNum, fiberConnection,
           rtBoutCount, rtStimCount, rtAD, rtStimPeriodCount, locoBoutCount,
           locoStimCount, locoAD, locoStimPeriodCount, fgBoutCount, fgStimCount,
           fgAD, fgStimPeriodCount, ogBoutCount, ogStimCount, ogAD, ogStimPeriodCount,
           aoBoutCount, aoStimCount, aoAD, aoStimPeriodCount]
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
    '''
    create list of names and dates, list(name, date) is the row num
    go through upload csv, if name and date in list of names and dates, skip
    '''
    nameDateList = []
    with open(db, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if row[0] != 'Mouse':
                nameDate = (row[0], row[2])
                nameDateList.append(nameDate)
        csvfile.close()
    #print(nameDateList)
    file = filedialog.askopenfilename(multiple = False, title = 'upload data csv\'s')
    toAdd = []
    with open(file, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            nameDate = (row[0], row[2])
            if nameDate not in nameDateList:
                toAdd.append(row)
        csvfile.close()
    #print(toAdd)
    with open(db, 'a', newline = '') as csvfile:
        writer_object = writer(csvfile)
        for row in toAdd:
            writer_object.writerow(row)
        csvfile.close()

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
        addOption = str.lower(input('\nadd manually or upload csv? (m/u)\n'))
        while (addOption != 'm') and (addOption != 'u'):
            addOption = str.lower(input('\ninvalid input, try again (m/u)\n'))
        if addOption == 'm':
            addManual(db)
        elif addOption == 'u':
            addUpload(db)
        option = str.lower(input('\nfilter sessions or add? or end (f/a/e)\n'))

print('\n\nDone!')