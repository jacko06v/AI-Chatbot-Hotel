import xmlrpc.client


# wubook credentials
token = 'token'
lcode = 'lcode'
server = xmlrpc.client.Server('https://wired.wubook.net/xrws/')


def trova_camera(obj):
    res, rooms = server.fetch_rooms(token, lcode)
    idRoom = []
    nameRoom = []
    for room in rooms:
        if room["occupancy"] == int(obj["ROOM"]):
            idRoom.append(room["id"])
            nameRoom.append(room["name"])
    return idRoom, nameRoom


def trova_prezzo(obj):
    try:
        idRoom, nameRoom = trova_camera(obj)
        res, rooms = server.fetch_plan_prices(token, lcode, 0, obj["DATE"], obj["DATE2"], idRoom)
        prezzo = []
        for i in range(len(idRoom)):
            prezzi = rooms[str(idRoom[i])]
            #prezzi è un array di float, sommo tutti i prezzi
            prezzo.append(sum(prezzi))

        #check if prezzo, nameRoom and idRoom have the same length
        if len(prezzo) == len(nameRoom) and len(prezzo) == len(idRoom):
            #create an obj with the name of the room and the price
            objectRooms = []
            for i in range(len(prezzo)):
                objectRooms.append({"name": nameRoom[i], "price": prezzo[i], "id": idRoom[i]})
            return objectRooms
        else:
            return False
    except:
        return False
    




    