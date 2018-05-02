import json
from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from collections import defaultdict
from validate_email import validate_email
import requests
from countries import Countries
from math import sin, cos, sqrt, atan2, radians


#TODO accept utf 8 code

app = Flask(__name__)
api = Api(app)

# Resources
rooms = defaultdict(list)
hotels = {}
users = {}
websites = defaultdict(list)
locations = {}
reservations = defaultdict(list) #maybe change type
bookings = defaultdict(list) #maybe change type
bookmarks = defaultdict(list) #maybe change type
offers = defaultdict(list) #maybe change type
reviews = defaultdict(list) #maybe change type

class Room(Resource):
    def __init__(self,number,hotel,price): #init one room
        self.number = number    #room number
        self.price = price
        rooms[hotel].append(self)


    #tested
    @app.route("/room/list",methods=['GET'],endpoint='room/listGet')
    def get():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):
            abort(404)
        response = json.dumps([ob.__dict__ for ob in rooms[int(hotel_id)]],ensure_ascii=False)
        return response



class Hotel(Resource):
    def __init__(self,name,location,rooms,stars,price):
        self.id = id(self)
        self.name = name
        self.location = location #id of location
        for a in str(rooms).split("|"):
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
        print("check1")
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)
        print("check2")
        for a in str(rooms).split("|"):
            if(not a.isdigit):
                abort(404)
        print("check3")
        if(locations.get(int(location))==None):
            abort(404)

        return json.dumps(Hotel(name,int(location),rooms,int(stars),price).__dict__)


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



    @app.route("/hotel/list",methods=['GET'],endpoint='hotel/listGet')
    def getList():
        location = request.args.get('location')
        distance = request.args.get('distance')
        if(location == None or not location.isdigit() or
            distance == None or not distance.isdigit()):
            return json.dumps([ob.__dict__ for ob in hotels],ensure_ascii=False)

        response = []
        loc = locations.get(location)
        if(loc == None):
            abort(404)
        for hotel in hotels:
            loc2 = locations.get(hotel.location)
            if(getDistance(loc.lat,loc.long,loc2.lat,loc2.long) <= distance):
                response.append(hotel)
        return json.dumps([ob.__dict__ for ob in response])



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
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            abort(404)
        hotel.stars = int(stars)
        return json.dumps(hotel.__dict__)



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
        if(curr_user == None or curr_user.passkey != user_key):
            abort(403)

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            abort(404)
        #TODO delete website
        return json.dumps(hotel.__dict__)



class User(Resource):
    # TODO add put /delete/ update /get
    def __init__(self, firstname, lastname, email, is_creator, passkey, Uid=None):
        self.firstname = firstname
        self.lastname = lastname
        #is_valid = validate_email('example@example.com') check in put
        self.email = email
        self.passkey = passkey
        self.is_creator = is_creator
        if(id is None):
            self.id = id(self)
        else:
            self.id = Uid
        users[self.id] = self



class Website(Resource):
    # TODO put/update/delete/get
    def __init__(self,hotel,url):
        self.id = id(self)
        self.url = url
        websites[hotel].append(self)


    #request = requests.get('http://www.example.com') #check in put
    #if (request.status_code != 200):
        #not valid
    #check if hotel exsists

class Location(Resource):
    # TODO add put /delete /get
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

    def getDistance(lat1, lon1, lat2, lon2):
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c


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




if __name__ == '__main__':
    print("Admin:")
    print(User("admin","","admin@api.at",True,"root",Uid=1).id)
    #TODO read and save
    app.run(debug=True)
