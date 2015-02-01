import pandas as pd
import nltk
import re
import csv
import operator
import pygal

def cleanChatData(inFile, outFile, n_cols):
    with open(inFile,"rb") as source:
        rdr= csv.reader( source )
        with open(outFile,"wb") as result:
            wtr = csv.writer( result )
            for r in rdr:
                if len(r) == n_cols:
                    #print r[0:n_cols]
                    wtr.writerow( (r[0:n_cols]) )
    print "Cleaned!"

def getChatData(chatFile):    
    data = pd.read_csv(chatFile,index_col=["Chat ID"],usecols=["Chat ID", "Chat Message", "UNIX Time Stamp", "chat_location_context"])
    #print data.shape data.head()
    return data

def getChatMessage(chatDf):
    return chatDf['Chat Message']

def performNLTK(cleanText):
    tokens = nltk.word_tokenize(cleanText)
    text = nltk.Text(tokens)
    #text.common_contexts(["travel", "accomodation"])
    countAccom = 0
    countTravel = 0
    countAccom = text.count('accomodation')
    countTravel = text.count('travel')
    return countAccom+countTravel
    #text.concordance("accomodation") # default text.concordance output
    #text.dispersion_plot(["travel", "accomodation"])

def cleanChatMsg(msg):
    cleanText = re.sub('[^a-zA-Z0-9\n\.]', ' ', msg) #replacing special charaters for text mining
    cleanText = cleanText.lower()
    return cleanText

def operateOnDf(df):
    myDict1 = {}
    for index, row in df.iterrows():
        chatMsg = str(row['Chat Message'])
        #print chatMsg
        cleanMsg = cleanChatMsg(chatMsg)
        getCount = performNLTK(cleanMsg)
        if getCount > 0:
            location = row['chat_location_context'].strip().split(":")[0]
            if index in myDict1.keys() and location not in myDict1[index]:
                myDict1[index].append(location)
            else:
                myDict1[index] = [location]

    return myDict1
                
def getLocIdDf(locIdFile):
    myDict = {}
    with open(locIdFile,"rb") as source:
        rdr= csv.reader( source )
        for r in rdr:
           myDict[r[0]] = r[1]
    return myDict

            
def mapLocChat(chatDict, locDb):
    myDict = {}
    for k in chatDict.keys():
        myList = []
        #print k,"=>",chatDict[k]
        cdict = chatDict[k]
        for locId in cdict:
            if locId in locDb.keys():
                myList.append(locDb[locId])
        if len(myList) > 0:
            myDict[k] = myList
        #print myList
    return myDict
        
                    
def initalizeAll():
    
    #cleanChatData("hackathon_chat_data\hackathon_chat_data.csv","cleanDataA\hackathon_chat_data.csv", 4)

    chatData = getChatData("cleanDataA\hackathon_chat_data.csv")
    getDict = operateOnDf(chatData)
    #print getDict
    #cleanChatData("hackathon_chat_data\chat_location_mapping.csv","cleanDataA\chat_location_mapping.csv", 2)
    locIdData = getLocIdDf("cleanDataA\chat_location_mapping.csv")

    #print locIdData.keys()[0:5]
    getMaps = mapLocChat(getDict, locIdData)
    #print getMaps # key:chatid value: Location talking about
    return getMaps



def callExit():
    exit()
    
def call1():
    countUsers = 0
    for users in myMap.keys():
        countUsers += 1
        print countUsers,") ",users
    pass
def call2():
    locDict = {}
    for users in myMap.keys():
        for loc in myMap[users]:
            if loc in locDict.keys():
                locDict[loc].append(users)
            else:
                locDict[loc] = [users]
                
    freqDict = {}
    for each in locDict.keys():
        freqDict[each] = len(locDict[each])
        
    sorted_cities = sorted(freqDict.items(), key=operator.itemgetter(1),reverse=True)
    print "Location\t\t# of users"
    for k,v in sorted_cities[0:5]:
        print k,"\t\t",v
    pass
def call3():
    locDict = {}
    for users in myMap.keys():
        for loc in myMap[users]:
            if loc in locDict.keys():
                locDict[loc].append(users)
            else:
                locDict[loc] = [users]
    freqDict = {}
    for each in locDict.keys():
        freqDict[each] = len(locDict[each])
    bar_chart = pygal.Bar()
    bar_chart.title = '# of users in a location'
    #bar_chart.x_labels = locDict.keys()
    for each in freqDict.keys():
        bar_chart.add(each, freqDict[each])
    bar_chart.render_to_file('AnalyticsBar.svg')
    print "Please find the out file by opening AnalyticsBar.svg"
    pass
def call4():
    print "coming soon...."
    pass

myMap = None
if __name__ == '__main__':
    myMap = initalizeAll()
    while True:
        print "Stayzilla MENU:"
        print "1. Users talking about Travel/Accomodation"
        print "2. Top 5 Location with Maximum Users"
        print "3. Bar chart of the distribution of the users"
        print "4. Yet to come"
        print "0 Exit"
        option = int(raw_input("Select an Option: "))
        options = {0: callExit,
                   1: call1,
                   2: call2,
                   3: call3,
                   4: call4
        }
        options[option]()
        pass
    



