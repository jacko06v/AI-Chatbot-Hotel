
import datetime

months = {
    "gennaio": 1,
    "febbraio": 2,
    "marzo": 3,
    "aprile": 4,
    "maggio": 5,
    "giugno": 6,
    "luglio": 7,
    "agosto": 8,
    "settembre": 9,
    "ottobre": 10,
    "novembre": 11,
    "dicembre": 12
}

def elaborate_info(obj):
   #check wich keys are present in the object
    if "DATE" in obj:
        #convert obj["DATE"] to lower case
        obj["DATE"] = obj["DATE"].lower()
        monthsForDate = []
        daysForDate = []
        yearsForDate = []
        #split the string in a list of words
        date = obj["DATE"].split()
        for i in range(len(date)):
            if date[i].isdigit():
                #check if the number is a day
                if int(date[i]) > 0 and int(date[i]) < 32:
                    daysForDate.append(date[i])
                    #check if the next word is a month
                    if date[i+1] in months.keys():
                        monthsForDate.append(months[date[i+1]])
                    #check if the previous word is a month
                    elif date[i-1] in months.keys():
                        monthsForDate.append(months[date[i-1]])
                #check if the number is a year
                elif int(date[i]) > 2020 and int(date[i]) < 2100:
                    yearsForDate.append(date[i])
            #elif date[i] is number/number 
            elif "/" in date[i]:
                #check if the number is a day
                if int(date[i].split("/")[0]) > 0 and int(date[i].split("/")[0]) < 32:
                    daysForDate.append(date[i].split("/")[0])
                    #check if the number is a month
                    if int(date[i].split("/")[1]) > 0 and int(date[i].split("/")[1]) < 13:
                        monthsForDate.append(date[i].split("/")[1])
                     #check if date[i].split("/")[2] exists
                    if len(date[i].split("/")) > 2:
                        if int(date[i].split("/")[2]) > 2020 and int(date[i].split("/")[2]) < 2100:
                            yearsForDate.append(date[i].split("/")[2])
               
        if len(monthsForDate) < 2 or len(daysForDate) < 2:
            if len(daysForDate) == 2 and daysForDate[0] < daysForDate[1]:
                    monthsForDate.append(monthsForDate[0])
            else:
                return False
                    
        #check if there are more than 2 years in the sentence
        if len(yearsForDate) < 2:
            if len(yearsForDate) == 0:
                for i in range(2):
                    yearsForDate.append(datetime.datetime.now().year)
            else:
                yearsForDate.append(yearsForDate[0])
        
        #create date object dd/mm/yyyy
        if len(daysForDate) > 0 and len(monthsForDate) > 0 and len(yearsForDate) > 0:
            obj["DATE"] = datetime.date(int(yearsForDate[0]), int(monthsForDate[0]), int(daysForDate[0])).strftime("%d/%m/%Y")
            if len(daysForDate) > 1 and len(monthsForDate) > 1 and len(yearsForDate) > 1:
                obj["DATE2"] = datetime.date(int(yearsForDate[1]), int(monthsForDate[1]), int(daysForDate[1])).strftime("%d/%m/%Y")
                #sottraggo un giorno alla data2
                obj["DATE2"] = (datetime.datetime.strptime(obj["DATE2"], "%d/%m/%Y") - datetime.timedelta(days=1)).strftime("%d/%m/%Y")
            else:
                obj["DATE2"] = datetime.date(int(yearsForDate[0]), int(monthsForDate[0]), int(daysForDate[0])).strftime("%d/%m/%Y")
        else:
            print("data non valida")

    if "ROOM" in obj:
        obj["ROOM"] = obj["ROOM"].lower()
        
        if "matrimoniale" in obj["ROOM"]:
            obj["ROOM"] = "2"
            obj["room_type"] = "matrimoniale"
        elif "singola" in obj["ROOM"]:
            obj["ROOM"] = "1"
            obj["room_type"] = "singola"
        elif "doppia" in obj["ROOM"]:
            obj["ROOM"] = "2"
            obj["room_type"] = "doppia"
        elif "tripla" in obj["ROOM"]:
            obj["ROOM"] = "3"
            obj["room_type"] = "tripla"
        elif "quadrupla" in obj["ROOM"]:
            obj["ROOM"] = "4"
            obj["room_type"] = "quadrupla"

        frase = "Ecco il preventivo per una camera {room_type} dal {DATE} al {DATE2}".format(**obj)
        

    return obj, frase

        
