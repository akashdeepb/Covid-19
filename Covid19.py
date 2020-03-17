#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request as req
import os
import datetime
import sys
import webbrowser
import time

# Method for Displaying Banner
def banner():
    print('''
        \033[31m
  / ____| \ \    / (_)  __ \      /_ |/ _ \ 
 | |     __\ \  / / _| |  | |______| | (_) |
 | |    / _ \ \/ / | | |  | |______| |\__, |
 | |___| (_) \  /  | | |__| |      | |  / / 
  \_____\___/ \/   |_|_____/       |_| /_/                                          
         The Global Panic 2020
         \033[0m
    ''')
        

# Method for Clearing Screen
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


# Method for Updating the Dataset
def update(auto=True):
    # Check if automatic update is True and last update was less than 3 hours ago
    if auto and os.path.isfile('covid_confirmed.csv') and ((datetime.datetime.now()-datetime.datetime.fromtimestamp(os.stat('covid_confirmed.csv').st_mtime))<datetime.timedelta(hours=3)) and os.name !='Windows':
        print("Last Update : 3 hours ago\nUpdate Skipped. (You can Manually Update from the Menu)")
    else:
        # URLs to fetch the Data
        CONFIRMED_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
        RECOVERED_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
        DEATHS_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

        # Update the Data Files
        print("\033[33mUpdating Database ... ")
        try:
            req.urlopen('https://sosc.org.in')          # Free Promo :P
            updatedFile = open("covid_confirmed.csv",'w')
            print("Fetching Confirmed Infection Data ...")
            updatedFile.write(((req.urlopen(CONFIRMED_URL)).read()).decode('utf-8'))
            updatedFile = open("covid_recovered.csv",'w')
            print("Fetching Recovered Data ...")
            updatedFile.write(((req.urlopen(RECOVERED_URL)).read()).decode('utf-8'))
            updatedFile = open("covid_deaths.csv",'w')
            print("Fetching Deaths Data ...")
            updatedFile.write(((req.urlopen(DEATHS_URL)).read()).decode('utf-8'))
            updatedFile.close()
            print("\033[35mUpdate Completed\033[0m")
        except:
            print("An Error Occurred while Updating the Data :(\nPress any key to continue...")

# Method to Plot Complete Time Line Graph
def plotTimeline(dates,confirm_sum,death_sum,recover_sum):
    dates_ = []
    for i in range(0,len(dates)):
        dates_.append(dates[i].split('/20')[0])
    plt.title("Covid-19 Timeline")
    plt.xlabel('Dates')
    plt.plot(dates_,confirm_sum,label="Confirmed Cases("+str(confirm_sum[len(confirm_sum)-1])+")")
    plt.plot(dates_,death_sum,label="Deaths("+str(death_sum[len(death_sum)-1])+")("+str(round(((death_sum[len(death_sum)-1]/confirm_sum[len(confirm_sum)-1])*100),2))+"%)")
    plt.plot(dates_,recover_sum,label="Recovered("+str(recover_sum[len(recover_sum)-1])+")("+str(round(((recover_sum[len(recover_sum)-1]/confirm_sum[len(confirm_sum)-1])*100),2))+"%)")
    plt.legend()
    plt.show()


# Method to Plot Datewise Graph
def plotDaily(dates,confirm_sum,death_sum,recover_sum):
    dates_ = []
    for i in range(0, len(dates)):
        dates_.append(dates[i].split('/20')[0])
    plt.title("Covid-19 Daily")
    plt.xlabel('Dates')
    plt.plot(dates_,confirm_sum,label="Confirmed Cases("+str(sum(confirm_sum))+")")
    plt.plot(dates_,death_sum,label="Deaths("+str(sum(death_sum))+")")
    plt.plot(dates_,recover_sum,label="Recovered("+str(sum(recover_sum))+")")
    plt.legend()
    plt.show()

# Method to Return List containing Timeline Data
def getTimeInfo(dates,data,country=None):
    total = []
    if country == None:
        for i in range(0,len(dates)):
            total.append(data[dates[i]].sum())
    else:
        for i in range(0,len(dates)):
            total.append(data[data['Country/Region']==country][dates[i]].sum())
    return total

# Method to Return List containing Daywise Data
def getDayInfo(dates,data,country=None):
    total=[]
    if country == None:
        total.append(data[dates[0]].sum())
        for i in range(1,len(dates)):
            total.append(data[dates[i]].sum()-data[dates[i-1]].sum())
    else:
        total.append(data[data['Country/Region']==country][dates[0]].sum())
        for i in range(1,len(dates)):
            total.append(data[data['Country/Region']==country][dates[i]].sum()-data[data['Country/Region']==country][dates[i-1]].sum())
    return total

# Menu for User 
def menu():
    try:
        # Initialize DataFrame containing Covid19 data
        confirmed_data = pd.read_csv('covid_confirmed.csv')
        deaths_data = pd.read_csv('covid_deaths.csv')
        recovered_data = pd.read_csv('covid_recovered.csv')
    except:
        print("Error Retrieving Data. Exiting...")
        exit()

    # Menu 
    while(True):
        clear()
        banner()
        print('''
        Select from the Following
        1. World Timeline 
        2. Daywise Graph
        3. Country Stats
        4. Versus Stats
        5. Visual World Map*

        9. Update Data

        0. Exit 

        ''')
        selection = input("Enter your Selection : ")
        dates = [i for i in confirmed_data.columns][4:]     # Initialize Dates

        # Initialize Sum lists
        confirm_sum = []
        death_sum = []
        recover_sum = []

        plt.figure('Covid - 19')    # Graph Figure Name

        # Validate User Selection
        # World Timeline
        if selection == '1':
            confirm_sum = getTimeInfo(dates,confirmed_data)
            death_sum = getTimeInfo(dates,deaths_data)
            recover_sum = getTimeInfo(dates,recovered_data)
            plotTimeline(dates,confirm_sum,death_sum,recover_sum)
        # World Daily Graph
        elif selection == '2':
            clear()
            banner()
            confirm_sum = getDayInfo(dates,confirmed_data)
            death_sum = getDayInfo(dates,deaths_data)
            recover_sum = getDayInfo(dates,recovered_data)
            plotDaily(dates,confirm_sum,death_sum,recover_sum)
        # Country Wise Stats
        elif selection == '3':
            clear()
            banner()
            while(True):
                print("\n\033[33mEnter -c or --countries to see the List of Countries/Regions\n\033[36mEnter -x or exit to go back to Main Menu\033[0m\n\n")
                sel = input("Enter Country/Region : ")
                sel = sel.lower()
                countries = confirmed_data['Country/Region'].sort_values().unique()
                if sel == '-c' or sel == '--countries':
                    # Display All Country Names
                    for country in countries:
                        print(country)
                # Exit back to Main Menu
                elif sel == '-x' or sel == 'exit' or sel == '0':
                    break
                else:
                    # Search for Country with similar name
                    similar = [country for country in countries if sel == country.lower()]
                    if len(similar)<1:
                        similar = [country for country in countries if sel in country.lower()]
                    if len(similar) < 1:
                        print("Country Not Found.")
                    elif len(similar) == 1:
                        confirm_sum = confirmed_data[confirmed_data['Country/Region']==similar[0]][dates[len(dates)-1]].sum()
                        death_sum = deaths_data[deaths_data['Country/Region']==similar[0]][dates[len(dates)-1]].sum()
                        recover_sum = recovered_data[recovered_data['Country/Region']==similar[0]][dates[len(dates)-1]].sum()
                        print("\033[34mData found for ",similar[0])
                        print("Confirmed Cases : ",confirm_sum)
                        print("Deaths : ",death_sum)
                        print("Recovered : ",recover_sum,"\033[0m")
                        print('''
                    Options
                    1. Generate Timeline Graph
                    2. Generate Daily Graph

                    0. Exit
                    ''')
                        sel = input("Enter you Selection : ")
                        confirm_sum = []
                        death_sum = []
                        recover_sum = []
                        # Generate Selected Country's Timeline Graph
                        if sel == '1':
                            confirm_sum = getTimeInfo(dates,confirmed_data,similar[0])
                            death_sum = getTimeInfo(dates,deaths_data,similar[0])
                            recover_sum = getTimeInfo(dates,recovered_data,similar[0])
                            plotTimeline(dates,confirm_sum,death_sum,recover_sum)
                        # Generate Selected Country's Daily Graph
                        elif sel == '2':
                            confirm_sum = getDayInfo(dates,confirmed_data,similar[0])
                            death_sum = getDayInfo(dates,deaths_data,similar[0])
                            recover_sum = getDayInfo(dates,recovered_data,similar[0])
                            plotDaily(dates,confirm_sum,death_sum,recover_sum)
                    else:
                        # Display Possible Matches
                        print("Found ",len(similar)," Matches")
                        for country in similar:
                            print(country)
        # Versus Stats [Feature Idea by @j0el (https://github.com/j0el)]
        elif selection == '4':
            clear()
            banner()
            exitFlag=False
            while(not exitFlag):
                print("\n\033[33mEnter -c or --countries to see the List of Countries/Regions\nPress 'Enter key' or '-g' or Type 'go' once you're done entering countries\nType 'show' or '-s' to See countries in List\n\033[35mEnter -d or --delete to remove delete the last country added\nType 'clear' to Remove all Countries from List\n\033[36mEnter -x or exit to go back to Main Menu\033[0m\n\n")
                countries = confirmed_data['Country/Region'].sort_values().unique()
                versusCountries = []
                while(True):
                    if len(versusCountries) > 0:
                        print("\033[34mCountries in List : ")
                        for country in versusCountries:
                            print(country)
                        print("\033[0m")
                    sel = input("Enter Country/Region : ")
                    sel = sel.lower()
                    if sel == '-c' or sel =='--countries':
                        for country in countries:
                            print(country)
                    elif sel == '-s' or sel == 'show':
                        if len(versusCountries) < 1:
                            print("\033[31mNo Countries in the List.\033[0m")
                    elif sel == '-x' or sel == 'exit' or sel == '0':
                        exitFlag=True
                        break
                    elif sel == "" or sel == 'go' or sel == '-g':
                        if len(versusCountries) < 1:
                            print("\nEnter Atleast 1 country into List\n\n")
                        else:
                            while(True):
                                print('''
                Select from the Following
                        
                \033[33mConfirmed\033[0m
                    1. Generate Confirmed Timeline Graph
                    2. Generate Confirmed Daily Graph
                        
                \033[31mDeaths\033[0m
                    3. Generate Deaths Timeline Graph
                    4. Generate Deaths Daily Graph

                \033[32mRecovered\033[0m
                    5. Generate Recovered Timeline Graph
                    6. Generate Recovered Daily Graph

                0. Exit
                                ''')
                                select = input("Enter your selection : ")
                                plt.figure('Covid - 19')
                                if select == '1':
                                    for country in versusCountries:
                                        confirm_sum  = []
                                        confirm_sum = getTimeInfo(dates,confirmed_data,country)
                                        plt.plot(dates,confirm_sum,label=country+"("+str(confirm_sum[len(confirm_sum)-1])+")")
                                    plt.title('Versus Graph - Confirmed Data')
                                    plt.legend()
                                    plt.show()
                                elif select == '2':
                                    for country in versusCountries:
                                        confirm_sum = []
                                        confirm_sum = getDayInfo(dates,confirmed_data,country)
                                        plt.title('Versus Graph - Daywise Confirmation')
                                        plt.plot(dates,confirm_sum,label=country+"("+str(sum(confirm_sum))+")")
                                    plt.legend()
                                    plt.show()
                                elif select == '3':
                                    for country in versusCountries:
                                        death_sum = []
                                        death_sum = getTimeInfo(dates,deaths_data,country)
                                        plt.plot(dates,death_sum,label=country+"("+str(death_sum[len(death_sum)-1])+")")
                                    plt.title('Versus Graph - Deaths Data')
                                    plt.legend()
                                    plt.show()
                                elif select == '4':
                                    for country in versusCountries:
                                        death_sum = []
                                        death_sum = getDayInfo(dates,deaths_data,country)
                                        plt.plot(dates,death_sum,label=country+"("+str(sum(death_sum))+")")
                                    plt.title('Versus Graph - Daywise Deaths')
                                    plt.legend()
                                    plt.show()
                                elif select == '5':
                                    for country in versusCountries:
                                        recover_sum = []
                                        recover_sum = getTimeInfo(dates,recovered_data,country)
                                        plt.plot(dates, recover_sum,label=country+"("+str(recover_sum[len(recover_sum)-1])+")")
                                    plt.title('Versus Graph - Recover Data')
                                    plt.legend()
                                    plt.show()
                                elif select == '6':
                                    for country in versusCountries:
                                        recover_sum = []
                                        recover_sum = getDayInfo(dates,recovered_data,country)
                                        plt.plot(dates,recover_sum,label=country+"("+str(sum(recover_sum))+")")
                                    plt.title('Versus Graph - Recover Graph')
                                    plt.legend()
                                    plt.show()
                                elif select == '0':
                                    break
                    elif sel == '-d' or sel == '--delete' or sel == 'del':
                        if len(versusCountries) == 0:
                            print("\033[31mList Aleady Empty \033[0m")
                        else:
                            print("\033[35mRemoved ",versusCountries[len(versusCountries)-1]," from List\033[0m")
                            versusCountries.pop()
                    elif sel == 'clear':
                        versusCountries = []
                        print("\033[32mCleared Country List.\033[0m")
                    else:
                        similar = [country for country in countries if sel == country.lower()]
                        if len(similar) < 1:
                            similar = [country for country in countries if sel in country.lower()]
                        if len(similar) < 1:
                            print("\033[31mCountry Not Found.\033[0m")
                        elif len(similar) == 1:
                            versusCountries.append(similar[0])
                        else:
                            print("Found ",len(similar)," Matches")
                            for country in similar:
                                print(country)
                            

        # Another Free Promo :3
        elif selection == '5':
            webbrowser.open_new('https://covid19.locale.ai')
            print('Powered by : haxzie [ https://github.com/haxzie ]\nGitHub: https://github.com/localeai/covid19-live-visualization\nURL: https://covid19.locale.ai')
            input()
        elif selection == '9':
            update(False)
            clear()
        elif selection == '0' or selection == 'exit':
            print("Exiting ... bye <3")
            exit()

if __name__ == '__main__':
    upFlag = True       # Default Update Flag as True
    for opt in sys.argv:
        opt = opt.lower()
        if opt == '-nu' or opt == '--no-update': 
            upFlag=False
            break    
        elif opt == '--fix':
            os.system('rm *.csv')
            upFlag=True
            break
        elif opt == '-h' or opt == '--help':
            print('''
-nu, --no-update   : Skip Initial Update of Dataset
--fix              : Reinitialize Datasets/ Troubleshoot
-h, --help         : What you're currently seeing on your screen
            ''')
            exit()
    if upFlag == True:
        update()
    time.sleep(1)
    clear()
    banner()
    menu()
