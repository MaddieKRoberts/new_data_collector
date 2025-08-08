import sqlite3
import xml.etree.ElementTree as ET
import requests
import os
import time


def downloadfiles(year, num):
    
    sc = 0

    #make url 
    urlnum = str(num).zfill(3)
    urlyear = f"https://clerk.house.gov/evs/{year}/roll"
    url = f"{urlyear}{urlnum}.xml"
    
    if fileexists(year, urlnum):
        return "already done"

    #make file name
    filename = f"xmlfiles/{year}{urlnum}.xml"
    
    #trying to download the file
    try:
        
        #finds if anything screwed up
        response = requests.get(url, stream=True)
        #response.raise_for_status()
        sc = response.status_code
        print(response.ok)
        #time.sleep(1)
        if int(sc) == 403:
            response.raise_for_status()
       
        #creates and downloads file

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File '{filename}' downloaded successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        #puts failed url into a file to pull from later
        with open("failedurls.txt", "a") as file:
            file.write(url+"\n")

        #return
    return (sc)


def fileexists(year, num):
    return os.path.exists(f"xmlfiles/{year}{num}.xml")



counter = 0
for i in range(1990, 2026):
    for b in range(1,1200):
        if not fileexists(i, str(b).zfill(3)):
            sc = downloadfiles(i, b)
            print (sc)
            if sc == 403:
                time.sleep(1)
                counter = counter+1
                if counter == 10:
                    counter = 0
                    break

            #time.sleep(.75)