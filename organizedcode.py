import sqlite3
import xml.etree.ElementTree as ET
import requests
import os


def downloadfiles(year, num)
    
    #make url
    urlnum = str(num).zfill(3)
    urlyear = f"https://clerk.house.gov/evs/{year}/roll"
    url = f"{urlyear}{urlnum}.xml"

    #make file name
    filename = f"{urlyear}{urlnum}.xml"
    
    #trying to download the file
    try:
        
        #finds if anything screwed up
        response = requests.get(url, stream=True)
        response.raise_for_status()
        print(response)
        
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

        return


downloadfiles(2003, 95)