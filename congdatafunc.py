import sqlite3
import xml.etree.ElementTree as ET
import requests
import os

def addhousebill(year, num):
    # Ensure the database directory exists
    os.makedirs(os.path.dirname('hrdata.db') or '.', exist_ok=True)

    # Connect to database and create table (with error handling)
    conn = sqlite3.connect('hrdata.db')
    c = conn.cursor()
    
    
    c.execute("""CREATE TABLE IF NOT EXISTS repvotes (
            vote text, 
            name text
            year integer,
            bill integer
        )""")
    
    
    urlnum = str(num).zfill(3) 
    urlyear = f"https://clerk.house.gov/evs/{year}/roll"
    url = f"{urlyear}{urlnum}.xml"

    # Create filename 
    filename = f"{year}_houserollcall_{num}.xml"

    try:
        # Download file
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File '{filename}' downloaded successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        conn.close()
        return

    try:
        # Parse XML file
        tree = ET.parse(filename)
        root = tree.getroot()

        # Process votes
        for v in root.findall("./vote-data/recorded-vote"):
            legisname = v[0].text
            legisvote = v[1].text
            
            # Insert vote record
            c.execute("INSERT INTO repvotes VALUES (?, ?, ?, ?)", (legisvote, legisname, year, num))
        
        # Commit changes
        conn.commit()

        # Print all records
        c.execute("SELECT rowid, * FROM crittervote")
        print(c.fetchall())

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    
    finally:
        # close the connection
        conn.close()
	
def deletehousebill(year, num):

	# Establish connection to hrdata.db
    conn = sqlite3.connect('hrdata.db')

    # Creates cursor
    c = conn.cursor()

    # Deletes all vote data in the bill arguments
    c.execute("DELETE from hrdata WHERE year = (?) AND bill = (?)", (year, num))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close

def emergencydeletetable():
    #deletes table in emergency
    conn = sqlite3.connect('housedata.db')
    c = conn.cursor()
    c.execute("DROP TABLE repvotes")
	


