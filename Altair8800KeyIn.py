# to prevent the programm from going to fast
from time import sleep

# for the pynput library
from pynput.mouse import Button, Controller

# from the google services api
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('', scope) # replace with your own key

# authorize the clientsheet 
client = gspread.authorize(creds)
sheet = client.open("").sheet1 # replace with your own google spreadsheet

# variables

mouse = Controller()

# get the values of a specific colum in the google sheet as input

getValues = sheet.col_values(1)

# format is (x, y) pixels for a 1080 x 1920 screen
dataInSwitches = {
    '0':1611,'1':1555, '2':1487,        # this is the x position for the data switches. There is no y position because the switches are on the same y axis
    '3':1392,'4':1324, '5':1258,
    '6':1157, '7':1096,
    }

operationSwitchesX = {
    'DEPOSIT':859, 
    'DEPOSIT NEXT': 862,            # this is the x and y positions for the operation/instruction switches. Unlike the data switches, their y and x positions are different
    'RESET': 994,
    'EXAMINE': 725,
    }

operationSwitchesY = {
    'DEPOSIT':596, 
    'DEPOSIT NEXT': 650, 
    'RESET': 589,
    'EXAMINE': 596,
}

# Function to flip the instruction switches, grabs data from the operation swiches x and y dictionarys. This is not a complete list

def returnSwitch(instruction, counter):
    if(instruction == 'DEPOSIT' or counter == 1):
        mouse.position = (operationSwitchesX['DEPOSIT'], operationSwitchesY['DEPOSIT'])
        sleep(0.06)
        mouse.click(Button.left, 1)
        sleep(0.06)

    elif(instruction == 'DEPOSIT NEXT' or counter > 1):
        mouse.position = (operationSwitchesX['DEPOSIT NEXT'], operationSwitchesY['DEPOSIT NEXT'])
        sleep(0.06)
        mouse.click(Button.left, 1)
        sleep(0.06)

    elif(instruction == 'RESET' or counter == 0):
        mouse.position = (operationSwitchesX['RESET'], operationSwitchesY['RESET'])
        sleep(0.06)
        mouse.click(Button.left, 1)
        sleep(0.06)

    elif(instruction == 'EXAMINE'):
        mouse.position = (operationSwitchesX['EXAMINE'], operationSwitchesY['EXAMINE'])
        sleep(0.06)
        mouse.click(Button.left, 1)
        sleep(0.06)

    elif(instruction == 'None'):
        print('no deposit, deposit next or reset instructions')

# This function flips the data switches if the number inputed is a 1 or a zero. Re-runing this function will un-flip the data switches reseting them to their original position

def inputDataSwitch(instruction):
    counter = 7                     # used to search the x coordinate in the dataSwitches dictionary
    for number in instruction:
        if(number == '1'):
            mouse.position = (dataInSwitches[str(counter)], 495)
            sleep(0.06)
            mouse.click(Button.left, 1)     # click on the data switch
            sleep(0.06)
            counter -= 1
        elif(number == '0'):
             counter -= 1       # skip to the next number
        else:
            counter = counter   # used to handle white spaces or other characters

# the proggram begings

for index, elem in enumerate(getValues):
    counter = 0
    if (index + 1 < len(getValues) and index - 1 >= 0):    # get the next and current element from getValues
        curr_el = str(elem)
        next_el = str(getValues[index + 1])
        if(curr_el != 'DEPOSIT' or curr_el != 'DEPOSIT NEXT' or curr_el != 'RESET' or curr_el != 'EXAMINE'):    # check if we are in a binary number and if we are then we input that binary number
            print('we are in a binary')
            inputDataSwitch(curr_el)
            if(next_el == 'DEPOSIT' or next_el == 'DEPOSIT NEXT' or next_el == 'RESET'  or next_el != 'EXAMINE'):
                print('the next elemet is a instruction, lets execute it ')                    
                returnSwitch(next_el)                                                     # check if the next element is a instruction, execute that instruction and reset the data switches back to their original state
                print('its been executed, now lets reset the data swiches')
                inputDataSwitch(curr_el)

