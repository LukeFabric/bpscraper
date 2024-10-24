#!/home/rizzler/bp/.venv/bin/python3
import pytest, csv
import asyncio
import time
from playwright.async_api import async_playwright, expect

def resize2dArray(oldArray):
    rows = len(oldArray)
    cols = len(oldArray[0])
    newArray = [[0 for i in range(cols)] for j in range(rows*2)]
    for i in range(rows):
        newArray[i] = oldArray[i]
    return newArray
def createInjuryTable(newTable):
    injuryTable = newTable.splitlines()
    injuryTable = injuryTable[35:]
    toDelete = 0
    for i in range(len(injuryTable)):
        injuryTable[i] = injuryTable[i].lstrip()
        if injuryTable[i] == '':
            toDelete += 1
    for i in range(toDelete):
        injuryTable.remove('')
    newerTable = [[0 for i in range(cols)] for j in range(rows)]
    count = 0
    for i in range(len(injuryTable) // 8):
        for j in range(8):
            newerTable[i][j] = injuryTable[count]
            count += 1
        if i+2 > len(newerTable):
            newerTable = resize2dArray(newerTable)
    return newerTable
async def main(firstName, lastName, playerID):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        lastName = lastName.lower()
        firstName = firstName.lower()
        await page.goto(f"https://www.baseballprospectus.com/player/{playerID}/{firstName}-{lastName}/")
        try:
            await expect(page.get_by_text("INJURIES Date On When the")).to_be_visible() #Check for different element?
            texts = await page.get_by_text("INJURIES Date On When the").all() #Need to check if player actually has injury data
            for row in texts:
                data = await row.all_text_contents()
                completeTable = data[0]
        except AssertionError:
            completeTable = [0]
        await browser.close()
        return completeTable
def createCSV(newTable, firstName, lastName, playerID):
    print(firstName, lastName)
    if newTable[0] == 0:
        injuryTable = newTable
        partFile = open("noInjury.csv", 'a')
        tableWrite = csv.writer(partFile, delimiter=',', quotechar='|')
        tableWrite.writerow([firstName, lastName, playerID])
    else:
        injuryTable = createInjuryTable(newTable)
        for i in range(len(injuryTable)):
            if injuryTable[i][0] != 0:
                if '/' in injuryTable[i][6]:
                    injuryTable[i][6] = injuryTable[i][6].replace('/', '_')
                partFile = open(f"{injuryTable[i][6].lower()}.csv", 'a', newline='\n')
                tableWriter = csv.writer(partFile, delimiter=',', quotechar='|')
                injuryTable[i].insert(0, ' '.join([firstName, lastName]))
                injuryTable[i].insert(1, playerID)
                tableWriter.writerow(injuryTable[i])
                partFile.close()
with open('playerid_list.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        rows, cols = (5, 8)
        if len(row) != 6 or row[5] == '':
            continue
        else:
            time.sleep(5)
            newTable = asyncio.run(main(row[1], row[0], row[2]))
            createCSV(newTable, row[1], row[0], row[2])
