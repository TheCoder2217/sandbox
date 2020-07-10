#Uses selenium - firefox browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import random
import PySimpleGUI as sg
import os
import sys
sg.theme('DarkAmber')
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
layout = [  [sg.Text('Username'), sg.InputText()],
            [sg.Text('Password'), sg.InputText()],
            [sg.Text('Number of Races'), sg.InputText()],
            [sg.Text('Speed')],
            [sg.Slider(range=(30,170),default_value=100,size=(20,10),orientation='horizontal',font=('Helvetica', 12))],
            [sg.Text('Accuracy')], 
            [sg.Slider(range=(70,100),default_value=85,size=(20,10),orientation='horizontal',font=('Helvetica', 12))],
            [sg.Text('Nitros')],
            [sg.Combo(['True', 'False', 'Random'])],
            [sg.Button('Ok'), sg.Button('Cancel')]
            ]
window = sg.Window('Sandbox', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    if(event == 'Ok'):
        break
window.close()




#Settings:

username = values[0]
password = values[1]
races = int(values[2])
WPM = int(values[3])
accuracy = int(values[4]) / 100
nitros = False

if(str(values[5]) == 'True'):
    nitros = True
if(str(values[5]) == 'Random'):
    nitros = 'rand'


debug = False
errorKeys = ['[',']','=', '+', '`']
delay1 = 0.7
delay2 = 1.3




driver = webdriver.Firefox(executable_path = resource_path('geckodriver.exe')) #Open firefox

#Logging in
driver.get("https://www.nitrotype.com/login") #go to login page

#Enter credidentials:
element_username = driver.find_element_by_name("username")
element_username.send_keys(username)
element_password = driver.find_element_by_name("password")
element_password.send_keys(password)
#Login to account
element_password.send_keys(Keys.RETURN)
time.sleep(3)
#Go to race page
driver.get("https://www.nitrotype.com/race")

currentRaces = 0
finished = False
while finished == False:
    #Consistently look for the html on the page to see what we want
    soup = BeautifulSoup(driver.page_source, features = 'lxml')
    try:
        characters = [str(line).split('>')[1].split('<')[0] for line in soup.find_all("span", class_= "dash-letter")]
        words = ''.join(characters).split("\xa0")
        wordString = ' '.join(words)
        if(wordString != ''): #If the text has appeared onto the page (or else wordString = [] because there are no words)
            print(wordString)
            biggestWord = max([len(w) for w in (words[0:len(words)-1])]) #Finds biggest word to use Nitro on
            words = [w + ' ' for w in words[0:len(words)-1]] + [words[len(words)-1]] #Puts space at every word except last word
            numOfChars = len(wordString)
            numOfWords = numOfChars/5
            numOfSecs = (numOfWords/WPM) * 60
            sleepTime = numOfSecs / numOfChars

            sleep1 = round((sleepTime * delay1), 6) * 1000000
            sleep2 = round((sleepTime * delay2), 6) * 1000000

            if(nitros == True):
                usedNitro = False
            else:
                usedNitro = True
            if(nitros == 'rand'):
                randn = random.randrange(1,3)
                if(randn == 1):
                    usedNitro = False
                else:
                    usedNitro = True
            time.sleep(4.3) #Time to wait while it says (3...2...1...Go!)
            for w in words:
                if(int(len(w)) >= int(biggestWord) and usedNitro == False):
                    ActionChains(driver).send_keys(Keys.RETURN).perform()
                    time.sleep(0.2)
                    ActionChains(driver).send_keys(Keys.SPACE).perform()
                    #Press SPACE
                    if debug == True:
                        print("Using NITRO")
                    usedNitro = True
                else:
                    for c in w:
                        errorProbability = random.randrange(0,100) / 100
                        accuracyWrongPercentage = 1 - accuracy
                        if(accuracyWrongPercentage >= errorProbability):
                            randomErrorKey = errorKeys[random.randrange(0,len(errorKeys))]
                            ActionChains(driver).send_keys(randomErrorKey).perform()
                            if debug == True:
                                print("Sending Error: " + randomErrorKey)
                        if c == ' ':
                            ActionChains(driver).send_keys(Keys.SPACE).perform()
                            if debug == True:
                                print("Sending SPACE")
                        else:
                            if(c.isupper() == False): #If it is NOT uppercase
                                ActionChains(driver).send_keys(c).perform()
                            else:
                                ActionChains(driver).send_keys(Keys.SHIFT, c).perform()
                            if debug == True:
                                print("Sending " + c)
                            
                            sleeptime = random.randrange(sleep1, sleep2)
                            time.sleep(sleeptime / 1000000)
            time.sleep(random.randrange(4,8))
            currentRaces += 1
            if(currentRaces >= races):
                finished = True
                break

            driver.refresh()
    except Exception as E:
        print(E)


driver.quit()
