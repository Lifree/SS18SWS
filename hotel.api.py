import json
from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from collections import defaultdict
from validate_email import validate_email
import requests
from countries import Countries
from math import sin, cos, sqrt, atan2, radians
from random import randint
from dateutil import parser as dateparse
from datetime import date, datetime
R = 6373.0 #earth radius


#TODO accept utf 8 code

app = Flask(__name__)
api = Api(app)

# Resources
rooms = defaultdict(list)
hotels = {}
users = {}
websites = defaultdict(list)
locations = {}
reservations = defaultdict(list)
bookings = defaultdict(list)
bookmarks = defaultdict(list)
reviews = defaultdict(list)

#################################################################################################
#################################################################################################
#################################################################################################
############################################## ROOM #############################################
#################################################################################################
#################################################################################################

#Room is created by the creation of an hotel
class Room(Resource):
    def __init__(self,number,hotel,price): #init one room
        self.number = number    #room number
        self.price = price      #price for one night incl concurrency symbol ($,€...)
        self.id = id(self)      #unique id of room
        rooms[hotel].append(self)  #append to dictory list


    #returns list of all rooms or filtered version with rooms of a hotel
    @app.route("/room/list",methods=['GET'],endpoint='room/listGet')
    def get():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):         #checks if parameter hotel was given and of correct type
            return json.dumps([[ob.__dict__ for ob in rooms[x]] for x in rooms],ensure_ascii=False) ,200, {'ContentType':'application/json'} #if not -> return all rooms
        if(hotels.get(int(hotel_id)) == None):                  #if hotel was given but it has no rooms
            return abort(404)
        response = json.dumps([ob.__dict__ for ob in rooms[int(hotel_id)]],ensure_ascii=False) #return rooms of one hotel
        return response ,200, {'ContentType':'application/json'}


#################################################################################################
#################################################################################################
#################################################################################################
############################################## HOTEL ###########################################
#################################################################################################
#################################################################################################
class Hotel(Resource):
    def __init__(self,name,location,rooms,stars,price):
        self.id = id(self)
        self.name = name
        self.location = location #id of location
        for a in str(rooms).split("|"):
            if(a.isdigit()):
                Room(int(a),self.id,price)
        self.stars = stars
        hotels[self.id] = self

    #tested
    @app.route("/hotel",methods=['POST'],endpoint='hotelPost')
    def create():
        user = request.args.get('user')
        user_key = request.args.get('key')
        location = request.args.get('location')
        rooms = request.args.get('rooms')
        stars = request.args.get('stars')
        price = request.args.get('price')
        name = request.args.get('name')

        if(user == None or not user.isdigit() or
            user_key == None or
            location == None or not location.isdigit() or
            rooms == None or
            stars == None or not stars.isdigit() or
            price == None or
            name == None):
            abort(404)
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            abort(403)
        for a in str(rooms).split("|"):
            if(not a.isdigit):
                abort(404)
        if(locations.get(int(location))==None):
            abort(404)

        return json.dumps(Hotel(name,int(location),rooms,float(stars),price).__dict__)


    #tested
    @app.route("/hotel",methods=['GET'],endpoint='hotelGet')
    def get():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):
            abort(404)
        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            abort(404)
        return json.dumps(hotel.__dict__)


    #tested
    @app.route("/hotel/list",methods=['GET'],endpoint='hotel/listGet')
    def getList():
        location = request.args.get('location')
        distance = request.args.get('distance')
        if(location == None or not location.isdigit() or
            distance == None or not distance.isdigit()):
            return json.dumps([ob.__dict__ for key, ob in hotels.items()],ensure_ascii=False)

        response = []
        loc = locations.get(int(location))
        if(loc == None):
            abort(404)
        for key, hotel in hotels.items():
            loc2 = locations.get(hotel.location)
            if(Location.getDistance(loc.lat,loc.long,loc2.lat,loc2.long) <= int(distance)):
                response.append(hotel)
        return json.dumps([ob.__dict__ for ob in response])


    #tested
    @app.route("/hotel",methods=['PUT'],endpoint='hotelUpdate')
    def update():
        hotel_id = request.args.get('hotel')
        stars = request.args.get('stars')
        user = request.args.get('user')
        user_key = request.args.get('key')
        if(user == None or not user.isdigit() or
            user_key == None or
            hotel_id == None or not hotel_id.isdigit() or
            stars == None or not stars.isdigit()):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            abort(403)

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            abort(404)
        hotel.stars = float(stars)
        return json.dumps(hotel.__dict__)


    #tested
    @app.route("/hotel",methods=['DELETE'],endpoint='hotelDel')
    def delete():
        hotel_id = request.args.get('hotel')
        user = request.args.get('user')
        user_key = request.args.get('key')
        if(user == None or not user.isdigit() or
            user_key == None or
            hotel_id == None or not hotel_id.isdigit()):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            abort(403)

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            abort(404)
        del hotels[int(hotel_id)]
        del rooms[int(hotel_id)]
        del reviews[int(hotel_id)]
        #TODO maybe delete more or cancle if the rest isnt deleted jet
        return json.dumps(hotel.__dict__)


#################################################################################################
#################################################################################################
#################################################################################################
############################################## USER #############################################
#################################################################################################
#################################################################################################
class User(Resource):
    def __init__(self, firstname, lastname, email, is_creator, passkey, Uid=None):
        self.firstname = firstname
        self.lastname = lastname
        #is_valid = validate_email('example@example.com') check in put
        self.email = email
        self.passkey = passkey
        self.is_creator = is_creator
        if(Uid == None):
            self.id = id(self)
        else:
            self.id = Uid
        users[self.id] = self

    #tested
    @app.route("/user",methods=['POST'],endpoint='userPost')
    def create():
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')
        email = request.args.get('email')
        is_creator = request.args.get('creator')
        passkey = request.args.get('passkey')
        user = request.args.get('user')
        user_key = request.args.get('key')
        if(user == None or not user.isdigit() or
            user_key == None or
            firstname == None or
            lastname == None or
            email == None or
            passkey == None):
            abort(404)

        if(is_creator == "True" or is_creator == "1"):
            is_creator = True
        else:
            is_creator = False

        if(not validate_email(email)):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            abort(403)

        return json.dumps(User(firstname,lastname,email,is_creator,passkey).__dict__)

    #tested
    @app.route("/user",methods=['DELETE'],endpoint='userDelete')
    def delete():
        user1 = request.args.get('user1')
        user2 = request.args.get('user2')
        user_key = request.args.get('key')
        if(user1 == None or not user1.isdigit() or
            user2 == None or not user2.isdigit() or
            user_key == None):
            abort(404)

        curr_user = users.get(int(user1))
        if(curr_user == None or curr_user.passkey != user_key or (user1 != user2 and curr_user.is_creator != True)):
            abort(403)

        user = users.get(int(user2))
        if(user == None):
            abort(404)
        del users[int(user2)]
        return json.dumps(user.__dict__)

    #tested
    @app.route("/user",methods=['PUT'],endpoint='userUpdate')
    def update():
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')
        email = request.args.get('email')
        is_creator = request.args.get('creator')
        passkey = request.args.get('passkey')
        user1 = request.args.get('user1')
        user2 = request.args.get('user2')
        user_key = request.args.get('key')
        if(user1 == None or not user1.isdigit() or
            user2 == None or not user2.isdigit() or
            user_key == None):
            abort(404)

        if(is_creator == "True" or is_creator == "1"):
            is_creator = True
        elif(is_creator == "False" or is_creator == "0"):
            is_creator = False

        curr_user = users.get(int(user1))
        user = users.get(int(user2))
        if(curr_user == None or curr_user.passkey != user_key or user == None):
            abort(403)

        if(curr_user.is_creator):
            if(is_creator != None):
                user.is_creator = is_creator

        if(email != None):
            if(not validate_email(email)):
                abort(404)
            user.email = email

        if(firstname != None):
            user.firstname = firstname

        if(lastname != None):
            user.lastname = lastname

        if(passkey != None):
            user.passkey = passkey

        return json.dumps(user.__dict__)


#################################################################################################
#################################################################################################
#################################################################################################
########################################### WEBSITE #############################################
#################################################################################################
#################################################################################################
class Website(Resource):
    def __init__(self,hotel,url):
        self.id = id(self)
        self.url = url
        websites[hotel].append(self)

    #tested
    @app.route("/website",methods=['PUT'],endpoint='websiteUpdate')
    def update():
        hotel_id = request.args.get('hotel')
        website_id = request.args.get('website')
        url = request.args.get('url')
        user = request.args.get('user')
        user_key = request.args.get('key')
        if(user == None or not user.isdigit() or
            user_key == None or
            hotel_id == None or not hotel_id.isdigit() or
            website_id == None or not website_id.isdigit() or
            url == None):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            abort(403)
        try:
            req = requests.get(url)
        except Exception as e:
            abort(404)
         #check in put
        if (req.status_code != 200):
            abort(404)
        hotelSites = websites.get(int(hotel_id))
        if(hotelSites == None):
            abort(404)
        for website in hotelSites:
            if(website.id == int(website_id)):
                website.url = url;
                return json.dumps(website.__dict__)
        abort(404)


    #tested
    @app.route("/website",methods=['DELETE'],endpoint='websiteDelete')
    def update():
        hotel_id = request.args.get('hotel')
        website_id = request.args.get('website')
        user = request.args.get('user')
        user_key = request.args.get('key')
        if(user == None or not user.isdigit() or
            user_key == None or
            hotel_id == None or not hotel_id.isdigit() or
            website_id == None or not website_id.isdigit()):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            abort(403)

        hotelSites = websites.get(int(hotel_id))
        if(hotelSites == None):
            abort(404)
        i = 0
        for website in hotelSites:
            if(website.id == int(website_id)):
                if(len(hotelSites)==1):
                    del websites[int(hotel_id)]
                else:
                    del websites[int(hotel_id)][i]
                return json.dumps(website.__dict__)
            i += 1
        abort(404)


    #tested
    @app.route("/website",methods=['POST'],endpoint='websitePost')
    def create():
        hotel_id = request.args.get('hotel')
        url = request.args.get('url')
        user = request.args.get('user')
        user_key = request.args.get('key')
        if(user == None or not user.isdigit() or
            user_key == None or
            hotel_id == None or not hotel_id.isdigit() or
            url == None):
            abort(404)
        try:
            req = requests.get(url)
        except Exception as e:
            abort(404)
         #check in put
        if (req.status_code != 200):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            abort(403)

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            abort(404)
        return json.dumps(Website(hotel.id,url).__dict__)

    #tested
    @app.route("/website/list",methods=['GET'],endpoint='website/listGet')
    def create():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):
            abort(404)

        hotelSites = websites.get(int(hotel_id))
        if(hotelSites == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in hotelSites])


#################################################################################################
#################################################################################################
#################################################################################################
########################################### LOCATION ############################################
#################################################################################################
#################################################################################################
class Location(Resource):
    def __init__(self, location, lat, long, country):
        self.location = location
        self.lat = lat
        self.long = long
        self.country = country
        self.id = id(self)
        locations[self.id] = self


    def getShortcut(country):
        for a,b in Countries:
            if(a==country or b==country):
                return a
        return None

    def getFullname(country):
        for a,b in Countries:
            if(a==country or b==country):
                return b
        return None

    def getDistance(la1, lo1, la2, lo2):
        lon2 = radians(lo2)
        lon1 = radians(lo1)
        lat2 = radians(la2)
        lat1 = radians(la1)
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    #tested
    @app.route("/location",methods=['POST'],endpoint='locationPost')
    def put():
        location = request.args.get('location')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        country = request.args.get('country')

        if(lat == None or not lat.isdigit() or
            lon == None or not lon.isdigit() or
            country == None or
            location == None):
            abort(404)

        countryName = Location.getFullname(country)
        if(countryName == None):
            abort(404)

        return json.dumps(Location(location,int(lat),int(lon),countryName).__dict__)


    #tested
    @app.route("/location",methods=['GET'],endpoint='locationǴet')
    def get():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):
            abort(404)
        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            abort(404)
        location = locations.get(hotel.location)
        if(location == None):
            abort(404)
        return json.dumps(location.__dict__)

    #tested
    @app.route("/location/list",methods=['GET'],endpoint='location/listǴet')
    def getList():
        return json.dumps( [location.__dict__ for key, location in locations.items()])

    #tested
    @app.route("/location",methods=['DELETE'],endpoint='locationDelete')
    def delete():
        location_id = request.args.get('location')
        if(location_id == None or not location_id.isdigit()):
            abort(404)
        location = locations.get(int(location_id))
        if(location==None):
            abort(404)
        del locations[int(location_id)]
        return json.dumps(location.__dict__)


#################################################################################################
#################################################################################################
#################################################################################################
###########################################  REVIEW  ############################################
#################################################################################################
#################################################################################################
class Review(Resource):
    def __init__(self, hotel, user, msg):
        self.hotel = hotel
        self.user = user
        self.msg = msg
        self.id = id(self)
        reviews[hotel].append(self)

    #tested
    @app.route("/review",methods=['POST'],endpoint='reviewPost')
    def put():
        hotel_id = request.args.get('hotel')
        msg = request.args.get('msg')
        user = request.args.get('user')
        user_key = request.args.get('key')

        if(user == None or not user.isdigit() or
            user_key == None or
            hotel_id == None or not hotel_id.isdigit() or
            msg == None):
            abort(404)

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)
        return json.dumps(Review(int(hotel_id),int(user),msg).__dict__)


    #tested
    @app.route("/review/list",methods=['GET'],endpoint='review/listGet')
    def get():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):
            abort(404)
        hotelReviews = reviews.get(int(hotel_id))
        if(hotelReviews == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in hotelReviews])



#################################################################################################
#################################################################################################
#################################################################################################
########################################  BOOKMARKS  ############################################
#################################################################################################
#################################################################################################
class Bookmark(Resource):
    def __init__(self, hotel, user):
        self.hotel = hotel
        self.user = user
        self.id = id(self)
        bookmarks[user].append(self)

    #tested
    @app.route("/bookmark",methods=['POST'],endpoint='bookmarkPost')
    def put():
        hotel_id = request.args.get('hotel')
        user = request.args.get('user')
        user_key = request.args.get('key')

        if(user == None or not user.isdigit() or
            user_key == None or
            hotel_id == None or not hotel_id.isdigit()):
            abort(404)

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)
        return json.dumps(Bookmark(int(hotel_id),int(user)).__dict__)


    #tested
    @app.route("/bookmark/list",methods=['GET'],endpoint='bookmark/listGet')
    def get():
        user = request.args.get('user')
        user_key = request.args.get('key')
        if(user == None or not user.isdigit() or
            user_key == None):
            abort(404)
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)
        userBookmarks = bookmarks.get(int(user))
        if(userBookmarks == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in userBookmarks])


    #tested
    @app.route("/bookmark",methods=['DELETE'],endpoint='bookmarkDelete')
    def get():
        user = request.args.get('user')
        user_key = request.args.get('key')
        bookmark_id = request.args.get('bookmark')
        if(user == None or not user.isdigit() or
            bookmark_id == None or not bookmark_id.isdigit() or
            user_key == None):
            abort(404)
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)
        userBookmarks = bookmarks.get(int(user))
        if(userBookmarks == None):
            abort(404)
        i = 0
        for ob in userBookmarks:
            if(ob.id == int(bookmark_id)):
                if(len(userBookmarks) == 1):
                    del bookmarks[int(user)]
                else:
                    del bookmarks[int(user)][i]
                return json.dumps(ob.__dict__)
            i += 1
        abort(404)


#################################################################################################
#################################################################################################
#################################################################################################
#####################################  RESERVATIONS  ############################################
#################################################################################################
#################################################################################################
class Reservation(Resource):
    def __init__(self, room, user, start, end):
        self.room = room
        self.user = user
        self.start_date = start
        self.end_date = end
        self.id = id(self)
        reservations[room].append(self)

    #tested
    @app.route("/reservation",methods=['POST'],endpoint='reservationPOST')
    def put():
        hotel_id = request.args.get('hotel')
        room_id = request.args.get('room')
        user = request.args.get('user')
        user_key = request.args.get('key')
        start = request.args.get('start')
        end = request.args.get('end')

        if(user == None or not user.isdigit() or
            user_key == None or
            start == None or
            end == None or
            hotel_id == None or not hotel_id.isdigit() or
            room_id == None or not room_id.isdigit()):
            abort(404)

        try:
            start = dateparse.parse(start).timestamp()
            end = dateparse.parse(end).timestamp()
        except Exception as e:
            abort(404)

        hotelRooms = rooms.get(int(hotel_id))
        if(hotelRooms == None):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)

        for ob in hotelRooms:
            if(ob.id == int(room_id)):
                roomReservations = reservations.get(int(room_id))
                if(roomReservations == None):
                    return json.dumps(Reservation(int(room_id),int(user),start,end).__dict__)
                else:
                    for res in roomReservations:
                        if ((res.start_date <= start and res.end_date >= start) or
                            (res.start_date <= end and res.end_date >= end)):
                            print(res.__dict__)
                            abort(404)
                    return json.dumps(Reservation(int(room_id),int(user),start,end).__dict__)
        abort(404)

    #tested
    @app.route("/reservation/list",methods=['GET'],endpoint='reservation/listGet')
    def get():
        room_id = request.args.get('room')
        if(room_id == None or not room_id.isdigit()):
            abort(404)
        roomReservations = reservations.get(int(room_id))
        if(roomReservations == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in roomReservations])


    #tested
    @app.route("/reservation",methods=['DELETE'],endpoint='reservationDelete')
    def get():
        user = request.args.get('user')
        user_key = request.args.get('key')
        room_id = request.args.get('room')
        res_id = request.args.get('reservation')
        if(user == None or not user.isdigit() or
            room_id == None or not room_id.isdigit() or
            res_id == None or not res_id.isdigit() or
            user_key == None):
            abort(404)
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)
        roomReservations = reservations.get(int(room_id))
        if(roomReservations == None):
            abort(404)
        i = 0
        for ob in roomReservations:
            if(ob.id == int(res_id)):
                if(ob.user != int(user) and curr_user.is_creator != True):
                    abort(403)
                if(len(roomReservations) == 1):
                    del reservations[int(room_id)]
                else:
                    del reservations[int(room_id)][i]
                return json.dumps(ob.__dict__)
            i += 1
        abort(404)


#################################################################################################
#################################################################################################
#################################################################################################
#####################################     BOOKING    ############################################
#################################################################################################
#################################################################################################
class Booking(Resource):
    def __init__(self, room, user, start, end):
        self.room = room
        self.user = user
        self.start_date = start
        self.end_date = end
        self.id = id(self)
        bookings[user].append(self)

    #tested
    @app.route("/booking",methods=['POST'],endpoint='bookingPOST')
    def put():
        hotel_id = request.args.get('hotel')
        room_id = request.args.get('room')
        user = request.args.get('user')
        user_key = request.args.get('key')
        start = request.args.get('start')
        end = request.args.get('end')

        if(user == None or not user.isdigit() or
            user_key == None or
            start == None or
            end == None or
            hotel_id == None or not hotel_id.isdigit() or
            room_id == None or not room_id.isdigit()):
            abort(404)

        try:
            start = dateparse.parse(start).timestamp()
            end = dateparse.parse(end).timestamp()
        except Exception as e:
            abort(404)

        hotelRooms = rooms.get(int(hotel_id))
        if(hotelRooms == None):
            abort(404)

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)

        for ob in hotelRooms:
            if(ob.id == int(room_id)):
                roomReservations = reservations.get(int(room_id))
                if(roomReservations == None):
                    Reservation(int(room_id),int(user),start,end)
                    return json.dumps(Booking(int(room_id),int(user),start,end).__dict__)
                else:
                    for res in roomReservations:
                        if ((res.start_date <= start and res.end_date >= start) or
                            (res.start_date <= end and res.end_date >= end)):
                            print(res.__dict__)
                            abort(404)
                    Reservation(int(room_id),int(user),start,end)
                    return json.dumps(Booking(int(room_id),int(user),start,end).__dict__)
        abort(404)

    #tested
    @app.route("/booking/list",methods=['GET'],endpoint='booking/listGet')
    def get():
        user = request.args.get('user')
        if(user == None or not user.isdigit()):
            abort(404)
        userBookings = bookings.get(int(user))
        if(userBookings == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in userBookings])


    #tested
    @app.route("/booking",methods=['DELETE'],endpoint='bookingDelete')
    def get():
        user1 = request.args.get('booker')
        user2 = request.args.get('user')
        user_key = request.args.get('key')
        booking_id = request.args.get('booking')
        if(user2 == None or not user2.isdigit() or
            user1 == None or not user1.isdigit() or
            booking_id == None or not booking_id.isdigit() or
            user_key == None):
            abort(404)
        curr_user = users.get(int(user2))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            abort(403)
        userBookings = bookings.get(int(user1))
        if(userBookings == None):
            abort(404)
        i = 0
        for ob in userBookings:
            if(ob.id == int(booking_id)):
                if(len(userBookings) == 1):
                    del bookings[int(user1)]
                else:
                    del bookings[int(user1)][i]
                return json.dumps(ob.__dict__)
            i += 1
        abort(404)

#################################################################################################
#################################################################################################
#################################################################################################
#####################################      OFFER     ############################################
#################################################################################################
#################################################################################################
class Offer(Resource):
    def __init__(self, room, hotel, start, end, price):
        self.room = room
        self.start_date = start
        self.end_date = end
        self.hotel = hotel
        self.id = id(self)
        delta = datetime.fromtimestamp(int(end)) - datetime.fromtimestamp(int(start))
        if(price[:-1].isdigit()):
            self.price = delta.days * int(price[:-1])
        else:
            self.price = "price not found in db"
        self.created = datetime.now().timestamp()

    #tested
    @app.route("/offer",methods=['GET'],endpoint='offerGet')
    def get():
        hotel_id = request.args.get('hotel')
        room_id = request.args.get('room')
        start = request.args.get('start')
        end = request.args.get('end')
        if(hotel_id == None or not hotel_id.isdigit() or
            room_id == None or not room_id.isdigit()):
            abort(404)

        try:
            start = dateparse.parse(start).timestamp()
            end = dateparse.parse(end).timestamp()
        except Exception as e:
            abort(404)

        hotelRooms = rooms.get(int(hotel_id))
        if(hotelRooms == None):
            abort(404)
        for ob in hotelRooms:
            if(int(room_id) == ob.id):
                return json.dumps(Offer(room_id, hotel_id, start, end, ob.price).__dict__)
        abort(404)






#################################################################################################
#################################################################################################
#################################################################################################
############################################## MAIN #############################################
#################################################################################################
#################################################################################################
def readJsonOld():
    data = json.load(open('db.json'))
    for hotel in data:
        tmp1 = Location(hotel["cityName"],hotel["latitude"],hotel["longitude"],hotel["countryName"])
        if (hotel["price"] == '' or hotel["price"]==99999):
            price = str(randint(16, 60))+ "$"
        else:
            price = str(hotel["price"]) + "$"
        tmp2 = Hotel(hotel["hotelName"],tmp1.id,hotel["facilities"],hotel["stars"],price)
        url = hotel["url"]
        if(len(url)>4):
            Website(tmp2.id,url)


if __name__ == '__main__':
    print("Admin:")
    print(User("admin","","admin@api.at",True,"root",Uid=1).id)
    readJsonOld()
    #TODO read and save
    app.run(debug=True)
