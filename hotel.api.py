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
import itertools
R = 6373.0 #earth radius

host = 'http://127.0.0.1:5000/'


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
#offers

#################################################################################################
#################################################################################################
#################################################################################################
############################################## ROOM #############################################
#################################################################################################
#################################################################################################

@app.route("/",methods=['GET'],endpoint='')
def get():
    response = {}
    response["@context"] = "http://schema.org"
    response["@type"] = "WebAPI"
    response["documentation"] = defaultdict(list)
    response["documentation"]["@type"] = "CreativeWork"

    #Resource
    room = defaultdict(list)
    room["@type"] = "CreativeWork"
    room["name"] = "room"

    #Resource Actions
    getRooms = defaultdict(list)
    getRooms["@type"] = "SearchAction"
    getRooms["target"] = host + "rooms?hotel={hotelid}"
    getRooms["url-input"].append("name=hotel")

    #Add action to resouce
    room["potentialAction"].append(getRooms)

        #Resource
    hotel = defaultdict(list)
    hotel["@type"] = "CreativeWork"
    hotel["name"] = "hotel"

    #Resource Actions
    postHotel = defaultdict(list)
    postHotel["@type"] = "CreateAction"
    postHotel["target"] = host + "hotel?user={userId}&key={keyString}&location={locationId}&rooms={roomsString}&stars={starsNumber}&price={priceString}&name={nameString}"
    postHotel["url-input"].append("required name=user")
    postHotel["url-input"].append("required name=key")
    postHotel["url-input"].append("required name=location")
    postHotel["url-input"].append("required name=rooms")
    postHotel["url-input"].append("required name=stars")
    postHotel["url-input"].append("required name=price")
    postHotel["url-input"].append("required name=name")

    getHotel = defaultdict(list)
    getHotel["@type"] = "SearchAction"
    getHotel["target"] = host + "hotel?hotel={hotelid}"
    getHotel["url-input"].append("required name=hotel")

    getHotels = defaultdict(list)
    getHotels["@type"] = "SearchAction"
    getHotels["target"] = host + "hotels?location={locationId}&distance={distanceNumber}"
    getHotels["url-input"].append("name=location")
    getHotels["url-input"].append("name=distance")

    updateHotel = defaultdict(list)
    updateHotel["@type"] = "UpdateAction"
    updateHotel["target"] = host + "hotels?hotel={hotelId}&user={userId}&key={keyString}&stars={starsNumber}"
    updateHotel["url-input"].append("required name=hotel")
    updateHotel["url-input"].append("required name=user")
    updateHotel["url-input"].append("required name=key")
    updateHotel["url-input"].append("required name=stars")

    deleteHotel = defaultdict(list)
    deleteHotel["@type"] = "DeleteAction"
    deleteHotel["target"] = host + "hotels?hotel={hotelId}&user={userId}&key={keyString}"
    deleteHotel["url-input"].append("required name=hotel")
    deleteHotel["url-input"].append("required name=user")
    deleteHotel["url-input"].append("required name=key")

    hotel["potentialAction"].append(postHotel)
    hotel["potentialAction"].append(getHotel)
    hotel["potentialAction"].append(getHotels)
    hotel["potentialAction"].append(updateHotel)
    hotel["potentialAction"].append(deleteHotel)

    user = defaultdict(list)
    user["@type"] = "CreativeWork"
    user["name"] = "user"

    postUser = defaultdict(list)
    postUser["@type"] = "CreateAction"
    postUser["target"] = host + "user?firstname={firstName}&lastname={lastName}&email={emailString}&creator={creatorBool}&passkey={keyString}&user={creatorId}&user_key={creatorKeyString}"
    postUser["url-input"].append("required name=firstname")
    postUser["url-input"].append("required name=lastname")
    postUser["url-input"].append("required name=email")
    postUser["url-input"].append("required name=creator")
    postUser["url-input"].append("required name=passkey")
    postUser["url-input"].append("required name=user")
    postUser["url-input"].append("required name=key")

    deleteUser = defaultdict(list)
    deleteUser["@type"] = "DeleteAction"
    deleteUser["target"] = host + "user?user1={creatorId}&user2={userId}&key={creatorKey}"
    deleteUser["url-input"].append("required name=user1")
    deleteUser["url-input"].append("required name=user2")
    deleteUser["url-input"].append("required name=key")

    updateUser = defaultdict(list)
    updateUser["@type"] = "UpdateAction"
    updateUser["target"] = host + "user?firstname={firstName}&lastname={lastName}&email={emailString}&creator={creatorBool}&passkey={keyString}&user1={creatorId}&user2={userId}&user_key={creatorKeyString}"
    updateUser["url-input"].append("required name=firstname")
    updateUser["url-input"].append("required name=lastname")
    updateUser["url-input"].append("required name=email")
    updateUser["url-input"].append("required name=creator")
    updateUser["url-input"].append("required name=passkey")
    updateUser["url-input"].append("required name=user1")
    updateUser["url-input"].append("required name=user2")
    updateUser["url-input"].append("required name=key")

    user["potentialAction"].append(postUser)
    user["potentialAction"].append(deleteUser)
    user["potentialAction"].append(updateUser)


    website = defaultdict(list)
    website["@type"] = "CreativeWork"
    website["name"] = "Website"

    updateWebsite = defaultdict(list)
    updateWebsite["@type"] = "UpdateAction"
    updateWebsite["target"] = host + "website?hotel={hotelId}&website={websiteId}&url={URL}&user={creatorId}&key={creatorKey}"
    updateWebsite["url-input"].append("required name=hotel")
    updateWebsite["url-input"].append("required name=website")
    updateWebsite["url-input"].append("required name=url")
    updateWebsite["url-input"].append("required name=user")
    updateWebsite["url-input"].append("required name=key")

    deleteWebsite = defaultdict(list)
    deleteWebsite["@type"] = "DeleteAction"
    deleteWebsite["target"] = host + "website?hotel={hotelId}&website={websiteId}&user={creatorId}&key={creatorKey}"
    updateWebsite["url-input"].append("required name=hotel")
    updateWebsite["url-input"].append("required name=website")
    updateWebsite["url-input"].append("required name=user")
    updateWebsite["url-input"].append("required name=key")

    createWebsite = defaultdict(list)
    createWebsite["@type"] = "CreateAction"
    createWebsite["target"] = host + "website?hotel={hotelId}&url={URL}&user={creatorId}&key={creatorKey}"
    createWebsite["url-input"].append("required name=hotel")
    createWebsite["url-input"].append("required name=url")
    createWebsite["url-input"].append("required name=user")
    createWebsite["url-input"].append("required name=key")

    searchWebsite = defaultdict(list)
    searchWebsite["@type"] = "SearchAction"
    searchWebsite["target"] = host + "websites?hotel={hotelId}"
    searchWebsite["url-input"].append("name=hotel")

    website["potentialAction"].append(updateWebsite)
    website["potentialAction"].append(deleteWebsite)
    website["potentialAction"].append(createWebsite)
    website["potentialAction"].append(searchWebsite)

    location = defaultdict(list)
    location["@type"] = "CreativeWork"
    location["name"] = "Location"

    createLocation = defaultdict(list)
    createLocation["@type"] = "CreateAction"
    createLocation["target"] = host + "location?location={locationName}&lat={latitude}&lon={longitude}&country={countryString}"
    createLocation["url-input"].append("required name=location")
    createLocation["url-input"].append("required name=lat")
    createLocation["url-input"].append("required name=lon")
    createLocation["url-input"].append("required name=country")

    searchLocations = defaultdict(list)
    searchLocations["@type"] = "SearchAction"
    searchLocations["target"] = host + "locations"

    searchLocation = defaultdict(list)
    searchLocation["@type"] = "SearchAction"
    searchLocation["target"] = host + "location?hotel={hotelId}"
    searchLocation["url-input"].append("required name=hotel")

    deleteLocation = defaultdict(list)
    deleteLocation["@type"] = "DeleteAction"
    deleteLocation["target"] = host + "location?location={locationId}"
    deleteLocation["url-input"].append("required name=location")

    location["potentialAction"].append(createLocation)
    location["potentialAction"].append(searchLocations)
    location["potentialAction"].append(searchLocation)
    location["potentialAction"].append(deleteLocation)

    review = defaultdict(list)
    review["@type"] = "CreativeWork"
    review["name"] = "Review"

    createReview = defaultdict(list)
    createReview["@type"] = "CreateAction"
    createReview["target"] = host + "review?hotel={hotelId}&msg={msgString}&user={creatorId}&key={keyString}"
    createReview["url-input"].append("required name=hotel")
    createReview["url-input"].append("required name=msg")
    createReview["url-input"].append("required name=user")
    createReview["url-input"].append("required name=key")

    searchReview = defaultdict(list)
    searchReview["@type"] = "SearchAction"
    searchReview["target"] = host + "reviews?hotel={hotelId}"
    searchReview["url-input"].append("name=hotel")

    review["potentialAction"].append(createReview)
    review["potentialAction"].append(searchReview)

    bookmark = defaultdict(list)
    bookmark["@type"] = "CreativeWork"
    bookmark["name"] = "Bookmark"

    createBookmark = defaultdict(list)
    createBookmark["@type"] = "CreateAction"
    createBookmark["target"] = host + "bookmark?hotel={hotelId}&user={creatorId}&key={keyString}"
    createBookmark["url-input"].append("required name=hotel")
    createBookmark["url-input"].append("required name=user")
    createBookmark["url-input"].append("required name=key")

    searchBookmark = defaultdict(list)
    searchBookmark["@type"] = "SearchAction"
    searchBookmark["target"] = host + "bookmarks?user={creatorId}&key={keyString}"
    searchBookmark["url-input"].append("required name=user")
    searchBookmark["url-input"].append("required name=key")

    deleteBookmark = defaultdict(list)
    deleteBookmark["@type"] = "DeleteAction"
    deleteBookmark["target"] = host + "bookmark?bookmark={bookmarkId}&user={creatorId}&key={keyString}"
    deleteBookmark["url-input"].append("required name=bookmark")
    deleteBookmark["url-input"].append("required name=user")
    deleteBookmark["url-input"].append("required name=key")

    bookmark["potentialAction"].append(createBookmark)
    bookmark["potentialAction"].append(searchBookmark)
    bookmark["potentialAction"].append(deleteBookmark)


    reservation = defaultdict(list)
    reservation["@type"] = "CreativeWork"
    reservation["name"] = "Reservation"

    createReservation = defaultdict(list)
    createReservation["@type"] = "CreateAction"
    createReservation["target"] = host + "reservation?hotel={hotelId}&user={creatorId}&key={keyString}&room={roomId}&start={startDate}&end={endDate}"
    createReservation["url-input"].append("required name=hotel")
    createReservation["url-input"].append("required name=user")
    createReservation["url-input"].append("required name=key")
    createReservation["url-input"].append("required name=room")
    createReservation["url-input"].append("required name=start")
    createReservation["url-input"].append("required name=end")

    searchReservations = defaultdict(list)
    searchReservations["@type"] = "SearchAction"
    searchReservations["target"] = host + "reservations?room={roomId}"
    searchReservations["url-input"].append("required name=room")

    deleteReservation = defaultdict(list)
    deleteReservation["@type"] = "DeleteAction"
    deleteReservation["target"] = host + "reservation?room={roomId}&reservation={reservationId}&user={creatorId}&key={keyString}"
    deleteReservation["url-input"].append("required name=room")
    deleteReservation["url-input"].append("required name=reservation")
    deleteReservation["url-input"].append("required name=user")
    deleteReservation["url-input"].append("required name=key")

    reservation["potentialAction"].append(createReservation)
    reservation["potentialAction"].append(searchReservations)
    reservation["potentialAction"].append(deleteReservation)

    booking = defaultdict(list)
    booking["@type"] = "CreativeWork"
    booking["name"] = "Booking"

    createBooking = defaultdict(list)
    createBooking["@type"] = "CreateAction"
    createBooking["target"] = host + "booking?hotel={hotelId}&user={creatorId}&key={keyString}&room={roomId}&start={startDate}&end={endDate}"
    createBooking["url-input"].append("required name=hotel")
    createBooking["url-input"].append("required name=user")
    createBooking["url-input"].append("required name=key")
    createBooking["url-input"].append("required name=room")
    createBooking["url-input"].append("required name=start")
    createBooking["url-input"].append("required name=end")

    searchBookings = defaultdict(list)
    searchBookings["@type"] = "SearchAction"
    searchBookings["target"] = host + "bookings?room={userId}"
    searchBookings["url-input"].append("name=user")

    deleteBooking = defaultdict(list)
    deleteBooking["@type"] = "DeleteAction"
    deleteBooking["target"] = host + "reservation?booker={bookerId}&booking={bookingId}&user={creatorId}&key={keyString}"
    deleteBooking["url-input"].append("required name=booker")
    deleteBooking["url-input"].append("required name=booking")
    deleteBooking["url-input"].append("required name=user")
    deleteBooking["url-input"].append("required name=key")

    booking["potentialAction"].append(createBooking)
    booking["potentialAction"].append(searchBookings)
    booking["potentialAction"].append(deleteBooking)


    offer = defaultdict(list)
    offer["@type"] = "CreativeWork"
    offer["name"] = "Offer"

    searchOffer = defaultdict(list)
    searchOffer["@type"] = "SearchAction"
    searchOffer["target"] = host + "offer?hotel={hotelId}&room={roomId}&start={startDate}&end={endDate}"
    searchOffer["url-input"].append("required name=hotel")
    searchOffer["url-input"].append("required name=room")
    searchOffer["url-input"].append("required name=start")
    searchOffer["url-input"].append("required name=end")

    offer["potentialAction"].append(searchOffer)




    #Add resource to API
    response["documentation"]["hasPart"].append(room)
    response["documentation"]["hasPart"].append(hotel)
    response["documentation"]["hasPart"].append(user)
    response["documentation"]["hasPart"].append(website)
    response["documentation"]["hasPart"].append(location)
    response["documentation"]["hasPart"].append(review)
    response["documentation"]["hasPart"].append(bookmark)
    response["documentation"]["hasPart"].append(reservation)
    response["documentation"]["hasPart"].append(booking)
    response["documentation"]["hasPart"].append(offer)



    return json.dumps(response) ,200, {'content-type':'application/json'}


#############################
#############################
########## REAL API #########
#############################
#############################


#Room is created by the creation of an hotel
class Room(Resource):
    newid = itertools.count().__next__
    def __init__(self,number,hotel,price): #init one room
        self.number = number    #room number
        self.price = price      #price for one night incl concurrency symbol ($,€...)
        self.id = Room.newid()      #unique id of room
        rooms[hotel].append(self)  #append to dictory list
        self.links = defaultdict(list)
        self.links['hotel'] = host + 'hotel?hotel=' + str(hotel)


    #returns list of all rooms or filtered version with rooms of a hotel
    @app.route("/rooms",methods=['GET'],endpoint='room/listGet')
    def get():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):         #checks if parameter hotel was given and of correct type
            return json.dumps([[ob.dict() for ob in rooms[x]] for x in rooms],ensure_ascii=False) ,200, {'content-type':'application/json'} #if not -> return all rooms
        if(hotels.get(int(hotel_id)) == None):                  #if hotel was given but it has no rooms
            abort(404)
        response = json.dumps([ob.dict() for ob in rooms[int(hotel_id)]],ensure_ascii=False) #return rooms of one hotel
        return response ,200, {'content-type':'application/json'}

    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "HotelRoom"
        dict["name"] = self.number

        additionalProperty = {}
        additionalProperty["@type"] = "PropertyValue"
        additionalProperty["name"] = "price"
        additionalProperty["value"] = self.price
        dict["additionalProperty"] = additionalProperty

        getHotel = {}

        getHotel["@type"] = "SearchAction"
        getHotel["name"] = "hotel"
        getHotel["query"] = self.links['hotel']
        dict["potentialAction"].append(getHotel)

        return dict



#################################################################################################
#################################################################################################
#################################################################################################
############################################## HOTEL ############################################
#################################################################################################
###################################################################https://github.com/Lifree/SS18SWS.git##############################


#Hotels can just be created by an creator
class Hotel(Resource):
    newid = itertools.count().__next__
    def __init__(self,name,location,rooms,stars,price):
        self.id = Hotel.newid()      #unique id of hotel
        self.name = name        #name of the hotel
        self.location = location #id of location
        for a in str(rooms).split("|"):
            if(a.isdigit()):
                Room(int(a),self.id,price)  # create rooms
        self.stars = stars  #stars of the hotel (can be updated)
        self.links = defaultdict(list)
        self.links['rooms'] = host + 'rooms?hotel=' + str(self.id)
        self.links['reviews'] = host + 'reviews?hotel=' + str(self.id)
        self.links['reservations'] = host + 'reservations?hotel=' + str(self.id)
        self.links['websites'] = host + 'websites?hotel=' + str(self.id)
        self.links['hotel'] = host + 'hotel?hotel=' + str(self.id)
        self.links['location'] = host + 'location?hotel=' + str(self.id)
        hotels[self.id] = self #save hotel into dictionary


    #create a new hotel
    @app.route("/hotel",methods=['POST'],endpoint='hotelPost')
    def create():
        user = request.args.get('user')
        user_key = request.args.get('key')
        location = request.args.get('location')
        rooms = request.args.get('rooms')
        stars = request.args.get('stars')
        price = request.args.get('price')
        name = request.args.get('name')

        #check authentication
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        #check arguments
        if (location == None or not location.isdigit() or
            rooms == None or
            stars == None or not stars.isdigit() or
            price == None or
            name == None):
            return "not all nessary fields were given (location, rooms, stars, price, name)" , 400
        curr_user = users.get(int(user))

        #check if "login" is right + have the rights
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            return 'pass doesnt match or no rights', 403

        #check type of room
        if(len(rooms)<3):
            return "a hotel needs at least one room", 400
        for a in str(rooms).split("|"):
            if(not a.isdigit):
                return "at least one room is not a digit", 400

        #check if location exists
        if(locations.get(int(location))==None):
            return "location not found", 400

        return json.dumps(Hotel(name,int(location),rooms,float(stars),price).__dict__), 200 , {'content-type':'application/json'}



    #get one hotel by id
    @app.route("/hotel",methods=['GET'],endpoint='hotelGet')
    def get():
        hotel_id = request.args.get('hotel')

        #check args
        if(hotel_id == None or not hotel_id.isdigit()):
            return "hotel id is not given or from wrong type", 400

        hotel = hotels.get(int(hotel_id))
        #check if hotel exsists
        if(hotel == None):
            return "no hotel found", 404
        return json.dumps(hotel.__dict__), 200 ,{'content-type':'application/json'}


    #get all hotels or just hotels in a radius
    @app.route("/hotels",methods=['GET'],endpoint='hotel/listGet')
    def getList():
        location = request.args.get('location')
        distance = request.args.get('distance')
        #check argumnets
        if(location == None or not location.isdigit() or
            distance == None or not distance.isdigit()):
            return json.dumps([ob.__dict__ for key, ob in hotels.items()],ensure_ascii=False) , 200 ,{'content-type':'application/json'} # return all hotels if no location and distance are given

        response = []

        #get location and abort if not found
        loc = locations.get(int(location))
        if(loc == None):
            return "no location found", 400

        #get all hotels in distance
        for key, hotel in hotels.items():
            loc2 = locations.get(hotel.location)
            if(Location.getDistance(loc.lat,loc.long,loc2.lat,loc2.long) <= int(distance)):
                response.append(hotel)
        if(len(response) == 0):
            abort(404)

        return json.dumps([ob.__dict__ for ob in response]), 200,{'content-type':'application/json'}


    #update stars of hotel
    @app.route("/hotel",methods=['PUT'],endpoint='hotelUpdate')
    def update():
        hotel_id = request.args.get('hotel')
        stars = request.args.get('stars')
        user = request.args.get('user')
        user_key = request.args.get('key')

        #check authentication
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        #check arguments
        if(hotel_id == None or not hotel_id.isdigit() or
            stars == None or not stars.isdigit()):
            return "hotel_id and stars are missing or invalide", 400

        #get current user and check if he is creator
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            'pass doesnt match or no rights', 403

        #get hotel and update stars if the hotel exsists
        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            return "no hotel found", 400
        hotel.stars = float(stars)
        return json.dumps(hotel.__dict__), 201,{'content-type':'application/json'}


    #delete a hotel
    @app.route("/hotel",methods=['DELETE'],endpoint='hotelDel')
    def delete():
        hotel_id = request.args.get('hotel')
        user = request.args.get('user')
        user_key = request.args.get('key')

        #check authentication
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        #check arguments
        if (hotel_id == None or not hotel_id.isdigit()):
            abort(404)

        #check curr user + if he is creator
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            'pass doesnt match or no rights', 403

        #delete hotel, rooms, reservations and review
        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            return "no hotel found", 400
        del hotels[int(hotel_id)]
        if(rooms.get(int(hotel_id))):
            for ob in rooms.get(int(hotel_id)):
                if(reservations.get(ob.id) != None):
                    del reservations[ob.id]
            del rooms[int(hotel_id)]
        if(reviews.get(int(hotel_id)) != None):
            del reviews[int(hotel_id)]
        return json.dumps(hotel.__dict__), 204,{'content-type':'application/json'}

    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "Hotel"
        dict["name"] = self.name
        dict["location"] = self.location
        dict["starRating"] = self.stars

        getRooms = {}
        getRooms["@type"] = "SearchAction"
        getRooms["name"] = "rooms"
        getRooms["query"] = self.links['rooms']
        dict["potentialAction"].append(getRooms)

        getReviews = {}
        getReviews["@type"] = "SearchAction"
        getReviews["name"] = "reviews"
        getReviews["query"] = self.links['reviews']
        dict["potentialAction"].append(getReviews)

        getReservations = {}
        getReservations["@type"] = "SearchAction"
        getReservations["name"] = "reservations"
        getReservations["query"] = self.links['reservations']
        dict["potentialAction"].append(getReservations)

        getWebsites= {}
        getWebsites["@type"] = "SearchAction"
        getWebsites["name"] = "websites"
        getWebsites["query"] = self.links['websites']
        dict["potentialAction"].append(getWebsites)

        getHotel= {}
        getHotel["@type"] = "SearchAction"
        getHotel["name"] = "hotel"
        getHotel["query"] = self.links['hotel']
        dict["potentialAction"].append(getHotel)

        getLocation= {}
        getLocation["@type"] = "SearchAction"
        getLocation["name"] = "location"
        getLocation["query"] = self.links['location']
        dict["potentialAction"].append(getLocation)
        return dict


#################################################################################################
#################################################################################################
#################################################################################################
############################################## USER #############################################
#################################################################################################
#################################################################################################

# User of our API
class User(Resource):
    newid = itertools.count().__next__
    def __init__(self, firstname, lastname, email, is_creator, passkey):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.passkey = passkey  #cleartext auth-key
        self.is_creator = is_creator #if true the user can do more things
        self.id = User.newid()
        self.links = defaultdict(list)
        self.links['bookmarks'] = host + 'bookmarks?user=' + str(self.id) + '&key=' + self.passkey
        self.links['bookings'] = host + 'bookings?user=' + str(self.id) + '&key=' + self.passkey
        users[self.id] = self

    #create an new user
    @app.route("/user",methods=['POST'],endpoint='userPost')
    def create():
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')
        email = request.args.get('email')
        is_creator = request.args.get('creator')
        passkey = request.args.get('passkey')
        user = request.args.get('user')
        user_key = request.args.get('key')

        #check authentication
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401
        #check args
        if (firstname == None or
            lastname == None or
            email == None or
            passkey == None):
            return "firstname, lastname, email and/or passkey are missing", 400

        #set the is_creator boolean
        if(is_creator == "True" or is_creator == "1"):
            is_creator = True
        else:
            is_creator = False

        if(not validate_email(email)):
            return "not a valid mail", 400

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            'pass doesnt match or no rights', 403

        return json.dumps(User(firstname,lastname,email,is_creator,passkey).__dict__), 201 ,{'content-type':'application/json'}

    #delete user by id
    @app.route("/user",methods=['DELETE'],endpoint='userDelete')
    def delete():
        user1 = request.args.get('user1')
        user2 = request.args.get('user2')
        user_key = request.args.get('key')

        #check authentication
        if(user1 == None or not user1.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        #check args
        if(user2 == None or not user2.isdigit()):
            return "no user to delete given", 400

        #check rights
        curr_user = users.get(int(user1))
        if(curr_user == None or curr_user.passkey != user_key or (user1 != user2 and curr_user.is_creator != True)):
            'pass doesnt match or no rights', 403

        #delete user
        user = users.get(int(user2))
        if(user == None):
            return "no user2 found", 400
        del users[int(user2)]
        return json.dumps(user.__dict__), 201,{'content-type':'application/json'}

    #update user for all args
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
        #check authentication
        if(user1 == None or not user1.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        #check args
        if(user2 == None or not user2.isdigit()):
            return "no user to update given", 400

        if(is_creator == "True" or is_creator == "1"):
            is_creator = True
        elif(is_creator == "False" or is_creator == "0"):
            is_creator = False

        curr_user = users.get(int(user1))
        user = users.get(int(user2))
        if(curr_user == None or curr_user.passkey != user_key or user == None):
            'pass doesnt match or no rights', 403

        #update section
        if(email != None):
            if(not validate_email(email)):
                return "no valid mail given", 400
            user.email = email

        if(curr_user.is_creator):
            if(is_creator != None):
                user.is_creator = is_creator

        if(firstname != None):
            user.firstname = firstname

        if(lastname != None):
            user.lastname = lastname

        if(passkey != None):
            user.passkey = passkey

        return json.dumps(user.__dict__), 200,{'content-type':'application/json'}

    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "Person"
        dict["familyName"] = self.lastname
        dict["givenName"] = self.firstname
        dict["email"] = self.email

        additionalProperty = {}
        additionalProperty["@type"] = "PropertyValue"
        additionalProperty["name"] = "passkey"
        additionalProperty["value"] = self.passkey
        dict["additionalProperty"] = additionalProperty

        additionalProperty2 = {}
        additionalProperty2["@type"] = "PropertyValue"
        additionalProperty2["name"] = "is_creator"
        additionalProperty2["value"] = self.is_creator
        dict["additionalProperty2"] = additionalProperty2

        getBookmarks= {}
        getBookmarks["@type"] = "SearchAction"
        getBookmarks["name"] = "bookmarks"
        getBookmarks["query"] = self.links['bookmarks']
        dict["potentialAction"].append(getBookmarks)

        getBookings= {}
        getBookings["@type"] = "SearchAction"
        getBookings["name"] = "bookings"
        getBookings["query"] = self.links['bookings']
        dict["potentialAction"].append(getBookings)

        return dict

#################################################################################################
#################################################################################################
#################################################################################################
########################################### WEBSITE #############################################
#################################################################################################
#################################################################################################

# website of a hotel
class Website(Resource):
    newid = itertools.count().__next__
    def __init__(self,hotel,url):
        self.id = Website.newid()
        self.url = url #url of the hotel website
        self.hotel = hotel #id of hotel
        self.links = defaultdict(list)
        self.links['hotel'] = host + 'hotel?hotel=' + str(self.hotel)
        self.links['hotelWebsites'] = host + 'websites?hotel=' + str(self.hotel)
        websites[hotel].append(self) #append to list of websites of one hotel

    #change website of hotel
    @app.route("/website",methods=['PUT'],endpoint='websiteUpdate')
    def update():
        hotel_id = request.args.get('hotel')
        website_id = request.args.get('website')
        url = request.args.get('url')
        user = request.args.get('user')
        user_key = request.args.get('key')

        #check authentication
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        #check args
        if( hotel_id == None or not hotel_id.isdigit() or
            website_id == None or not website_id.isdigit() or
            url == None):
            return "invalid hotel_id, website_id or url", 400

        #check user rights
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            'pass doesnt match or no rights', 403

        #check website
        try:
            req = requests.get(url)
        except Exception as e:
            return "website of invalid format", 400
         #check in put
        if (req.status_code != 200):
            return "website doesnt exsists", 400
        hotelSites = websites.get(int(hotel_id))
        if(hotelSites == None):
            return "hotel has no websites", 400
        for website in hotelSites:
            if(website.id == int(website_id)):
                website.url = url;
                return json.dumps(website.__dict__), 200,{'content-type':'application/json'}
        abort(404)


    #delete website
    @app.route("/website",methods=['DELETE'],endpoint='websiteDelete')
    def update():
        hotel_id = request.args.get('hotel')
        website_id = request.args.get('website')
        user = request.args.get('user')
        user_key = request.args.get('key')

        #check authentication
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        #check args
        if( hotel_id == None or not hotel_id.isdigit() or
            website_id == None or not website_id.isdigit() or
            url == None):
            return "invalid hotel_id, website_id or url", 400,{'content-type':'application/json'}

        #check user rights
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            'pass doesnt match or no rights', 403

        hotelSites = websites.get(int(hotel_id))
        if(hotelSites == None):
            return "hotel has no websites", 400
        i = 0
        for website in hotelSites:
            if(website.id == int(website_id)):
                if(len(hotelSites)==1):
                    del websites[int(hotel_id)]
                else:
                    del websites[int(hotel_id)][i]
                return json.dumps(website.__dict__), 204,{'content-type':'application/json'}
            i += 1
        abort(404)


    #create new website
    @app.route("/website",methods=['POST'],endpoint='websitePost')
    def create():
        hotel_id = request.args.get('hotel')
        url = request.args.get('url')
        user = request.args.get('user')
        user_key = request.args.get('key')
        #check authentication
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        #check args
        if( hotel_id == None or not hotel_id.isdigit() or
            website_id == None or not website_id.isdigit() or
            url == None):
            return "invalid hotel_id, website_id or url", 400

        #check user rights
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            'pass doesnt match or no rights', 403

        #check website
        try:
            req = requests.get(url)
        except Exception as e:
            return "website of invalid format", 400

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            return "hotel id ivalide", 400
        return json.dumps(Website(hotel.id,url).__dict__), 201,{'content-type':'application/json'}

    #get list of websites (of a hotel)
    @app.route("/websites",methods=['GET'],endpoint='website/listGet')
    def create():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):
            return json.dumps([[ob.__dict__ for ob in websites[x]] for x in websites]), 200,{'content-type':'application/json'}

        hotelSites = websites.get(int(hotel_id))
        if(hotelSites == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in hotelSites]), 200,{'content-type':'application/json'}

    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "WebSite"
        dict["url"] = self.url
        dict["@type"] = "Hotel"
        dict["identifier"] = self.hotel
        dict["email"] = self.email

        getHotel= {}
        getHotel["@type"] = "SearchAction"
        getHotel["name"] = "hotel"
        getHotel["query"] = self.links['hotel']
        dict["potentialAction"].append(getHotel)

        getHotelWebsites= {}
        getHotelWebsites["@type"] = "SearchAction"
        getHotelWebsites["name"] = "hotelWebsites"
        getHotelWebsites["query"] = self.links['hotelWebsites']
        dict["potentialAction"].append(getHotelWebsites)

        return dict

#################################################################################################
#################################################################################################
#################################################################################################
########################################### LOCATION ############################################
#################################################################################################
#################################################################################################

# Location
class Location(Resource):
    newid = itertools.count().__next__
    def __init__(self, location, lat, long, country):
        self.location = location    # name of the location
        self.lat = lat              # latitude
        self.long = long            # longitude
        self.country = country      # country as fullname
        self.id = Location.newid()         # id of location
        self.links = defaultdict(list)
        self.links['hotels'] = host + 'hotels?location=' + str(self.id) + '&distance=0'
        locations[self.id] = self

    # get Shortcut of country... AUT for Austria
    def getShortcut(country):
        for a,b in Countries:
            if(a==country or b==country):
                return a
        return None

    # get Fullname of country... Austria for AUT
    def getFullname(country):
        for a,b in Countries:
            if(a==country or b==country):
                return b
        return None

    #calc distance in km between two locations
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

    #create a new location -> can be done by every user
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
            return "location, lat,lon or country is invalid", 400

        countryName = Location.getFullname(country)
        if(countryName == None):
            return "Country is invalide", 400

        return json.dumps(Location(location,int(lat),int(lon),countryName).__dict__), 201,{'content-type':'application/json'}


    #tested
    @app.route("/location",methods=['GET'],endpoint='locationGet')
    def get():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):
            return "hotel is invalide", 400
        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            return "hotel not found", 400
        location = locations.get(hotel.location)
        if(location == None):
            abort(404)
        return json.dumps(location.__dict__), 200,{'content-type':'application/json'}

    #return all locations
    @app.route("/locations",methods=['GET'],endpoint='location/listǴet')
    def getList():
        return json.dumps( [location.__dict__ for key, location in locations.items()]), 200,{'content-type':'application/json'}

    #delete location
    @app.route("/location",methods=['DELETE'],endpoint='locationDelete')
    def delete():
        location_id = request.args.get('location')
        if(location_id == None or not location_id.isdigit()):
            return "location is invalid", 400
        location = locations.get(int(location_id))
        if(location==None):
            abort(404)
        del locations[int(location_id)]
        return json.dumps(location.__dict__), 204,{'content-type':'application/json'}

    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "Place"
        dict["location"] = self.location
        dict["@type"] = "GeoCoordinates"
        dict["longitude"] = self.long
        dict["latitude"] = self.lat
        dict["addressCountry"] = self.country

        getHotels= {}
        getHotels["@type"] = "SearchAction"
        getHotels["name"] = "hotels"
        getHotels["query"] = self.links['hotels']
        dict["potentialAction"].append(getHotels)

        return dict

#################################################################################################
#################################################################################################
#################################################################################################
###########################################  REVIEW  ############################################
#################################################################################################
#################################################################################################

# Reviews of Hotels - Can not be updated or deleted
class Review(Resource):
    newid = itertools.count().__next__
    def __init__(self, hotel, user, msg):
        self.hotel = hotel  #reviewed hotel
        self.user = user    #reviewer
        self.msg = msg      #review
        self.id = Review.newid()  #id
        self.links = defaultdict(list)
        self.links['hotelReviews'] = host + 'reviews?hotel=' + str(self.hotel)
        self.links['reviewHotel'] = host + 'hotel?hotel=' + str(self.hotel)
        reviews[hotel].append(self)

    #create review
    @app.route("/review",methods=['POST'],endpoint='reviewPost')
    def put():
        hotel_id = request.args.get('hotel')
        msg = request.args.get('msg')
        user = request.args.get('user')
        user_key = request.args.get('key')

        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        if (hotel_id == None or not hotel_id.isdigit() or
            msg == None):
            return "invalide message or hotel id", 400

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            return "hotel not found", 400

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            'pass doesnt match or no rights', 403

        return json.dumps(Review(int(hotel_id),int(user),msg).__dict__),201,{'content-type':'application/json'}


    #get reviews (by hotel_id)
    @app.route("/reviews",methods=['GET'],endpoint='review/listGet')
    def get():
        hotel_id = request.args.get('hotel')
        if(hotel_id == None or not hotel_id.isdigit()):
            return json.dumps([[ob.__dict__ for ob in reviews[x]] for x in reviews]), 200,{'content-type':'application/json'}
        hotelReviews = reviews.get(int(hotel_id))
        if(hotelReviews == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in hotelReviews]),200,{'content-type':'application/json'}

    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "Review"
        dict["itemReviewed"] = self.hotel
        dict["author"] = self.user
        dict["reviewBody"] = self.msg

        getHotelReviews= {}
        getHotelReviews["@type"] = "SearchAction"
        getHotelReviews["name"] = "hotelReviews"
        getHotelReviews["query"] = self.links['hotelReviews']
        dict["potentialAction"].append(getHotelReviews)

        getReviewHotel= {}
        getReviewHotel["@type"] = "SearchAction"
        getReviewHotel["name"] = "reviewHotel"
        getReviewHotel["query"] = self.links['reviewHotel']
        dict["potentialAction"].append(getReviewHotel)
        return dict


#################################################################################################
#################################################################################################
#################################################################################################
########################################  BOOKMARKS  ############################################
#################################################################################################
#################################################################################################

# Userbookmark for hotels
class Bookmark(Resource):
    newid = itertools.count().__next__
    def __init__(self, hotel, user, key):
        self.hotel = hotel      #id of hotel
        self.user = user        #user id
        self.id = Bookmark.newid()      #bookmark id
        self.links = defaultdict(list)
        self.links['userBookmarks'] = host + 'bookmarks?user=' + str(self.user) + '&key=' + key
        bookmarks[user].append(self)

    #create bookmark
    @app.route("/bookmark",methods=['POST'],endpoint='bookmarkPost')
    def put():
        hotel_id = request.args.get('hotel')
        user = request.args.get('user')
        user_key = request.args.get('key')

        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401
        if(hotel_id == None or not hotel_id.isdigit()):
            return "invalide hotel id", 400

        hotel = hotels.get(int(hotel_id))
        if(hotel == None):
            return "hotel is not found", 400

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            'pass doesnt match or no rights', 403
        return json.dumps(Bookmark(int(hotel_id),int(user), key).__dict__), 201,{'content-type':'application/json'}


    # return the bookmarks of an user
    @app.route("/bookmarks",methods=['GET'],endpoint='bookmark/listGet')
    def get():
        user = request.args.get('user')
        user_key = request.args.get('key')
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401
        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            'pass doesnt match or no rights', 403
        userBookmarks = bookmarks.get(int(user))
        if(userBookmarks == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in userBookmarks]), 200,{'content-type':'application/json'}


    #delete bookmark
    @app.route("/bookmark",methods=['DELETE'],endpoint='bookmarkDelete')
    def get():
        user = request.args.get('user')
        user_key = request.args.get('key')
        bookmark_id = request.args.get('bookmark')
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        if(bookmark_id == None or not bookmark_id.isdigit()):
            return "bookmarkid is invalide", 400

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            'pass doesnt match or no rights', 403
        userBookmarks = bookmarks.get(int(user))
        if(userBookmarks == None):
            return "user has no bookmarks", 400
        i = 0
        for ob in userBookmarks:
            if(ob.id == int(bookmark_id)):
                if(len(userBookmarks) == 1):
                    del bookmarks[int(user)]
                else:
                    del bookmarks[int(user)][i]
                return json.dumps(ob.__dict__), 204,{'content-type':'application/json'}
            i += 1
        abort(404)

    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "Thing"
        dict["@type"] = "Person"
        dict["identifier"] = self.user
        dict["@type"] = "Hotel"
        dict["identifier"] = self.hotel

        getUserBookmarks= {}
        getUserBookmarks["@type"] = "SearchAction"
        getUserBookmarks["name"] = "userBookmarks"
        getUserBookmarks["query"] = self.links['userBookmarks']
        dict["potentialAction"].append(getUserBookmarks)
        return dict

#################################################################################################
#################################################################################################
#################################################################################################
#####################################  RESERVATIONS  ############################################
#################################################################################################
#################################################################################################
class Reservation(Resource):
    newid = itertools.count().__next__
    def __init__(self, room, user, start, end):
        self.room = room    #room id
        self.user = user    #reservator
        self.start_date = start  #start timestamp
        self.end_date = end #end timestamp
        self.links = defaultdict(list)
        self.links['roomReservations'] = host + 'reservations?room=' + str(self.room)
        self.id = Reservation.newid() #reservation id
        reservations[room].append(self)

    #create reservation
    @app.route("/reservation",methods=['POST'],endpoint='reservationPOST')
    def put():
        hotel_id = request.args.get('hotel')
        room_id = request.args.get('room')
        user = request.args.get('user')
        user_key = request.args.get('key')
        start = request.args.get('start')
        end = request.args.get('end')

        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401
        if( start == None or
            end == None or
            hotel_id == None or not hotel_id.isdigit() or
            room_id == None or not room_id.isdigit()):
            return "start, end, hotel or room are invalide", 400

        try:
            start = dateparse.parse(start).timestamp()
            end = dateparse.parse(end).timestamp()
        except Exception as e:
            return "start or end is not a date", 400

        hotelRooms = rooms.get(int(hotel_id))
        if(hotelRooms == None):
            return "rooms of hotel not found", 400

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            'pass doesnt match or no rights', 403

        for ob in hotelRooms:
            if(ob.id == int(room_id)):
                roomReservations = reservations.get(int(room_id))
                if(roomReservations == None):
                    return json.dumps(Reservation(int(room_id),int(user),start,end).__dict__), 201,{'content-type':'application/json'}
                else:
                    for res in roomReservations:
                        if ((res.start_date <= start and res.end_date >= start) or
                            (res.start_date <= end and res.end_date >= end)):
                            return "there is another reservation in this time", 400
                    return json.dumps(Reservation(int(room_id),int(user),start,end).__dict__), 201,{'content-type':'application/json'}
        abort(404)

    #get reservations (of a room)
    @app.route("/reservations",methods=['GET'],endpoint='reservation/listGet')
    def get():
        room_id = request.args.get('room')
        if(room_id == None or not room_id.isdigit()):
            json.dumps([[ob.__dict__ for ob in reservations[x]] for x in reservations]), 200,{'content-type':'application/json'}
        roomReservations = reservations.get(int(room_id))
        if(roomReservations == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in roomReservations]), 200,{'content-type':'application/json'}


    #delete reservation
    @app.route("/reservation",methods=['DELETE'],endpoint='reservationDelete')
    def get():
        user = request.args.get('user')
        user_key = request.args.get('key')
        room_id = request.args.get('room')
        res_id = request.args.get('reservation')
        if(user == None or not user.isdigit() or
            user_key == None):
            return 'you have to auth', 401

        if(room_id == None or not room_id.isdigit() or
            res_id == None or not res_id.isdigit()):
            return "room or reservation id is invalide", 400

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            'pass doesnt match or no rights', 403
        roomReservations = reservations.get(int(room_id))
        if(roomReservations == None):
            return "no reservations for the room found", 400
        i = 0
        for ob in roomReservations:
            if(ob.id == int(res_id)):
                if(ob.user != int(user) and curr_user.is_creator != True):
                    'pass doesnt match or no rights', 403
                if(len(roomReservations) == 1):
                    del reservations[int(room_id)]
                else:
                    del reservations[int(room_id)][i]
                return json.dumps(ob.__dict__), 204,{'content-type':'application/json'}
            i += 1
        abort(404)

#booking is the ACTUAL schema.org reservation -> I now used it for both, i might have to change our reservation
    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "LodgingReservation"
        dict["underName"] = self.user
        dict["@type"] = "Hotel"
        dict["identifier"] = self.hotel
        dict["checkinTime"] = self.start_date
        dict["checkoutTime"] = self.end_date

        getRoomReservations= {}
        getRoomReservations["@type"] = "SearchAction"
        getRoomReservations["name"] = "roomReservations"
        getRoomReservations["query"] = self.links['roomReservations']
        dict["potentialAction"].append(getRoomReservations)
        return dict

#################################################################################################
#################################################################################################
#################################################################################################
#####################################     BOOKING    ############################################
#################################################################################################
#################################################################################################

#booking a room
#newid = itertools.count().__next__
class Booking(Resource):
    def __init__(self, room, user, start, end):
        self.room = room    #room id
        self.user = user    #booker
        self.start_date = start     #start timestamp
        self.end_date = end         #end timestamp
        self.id = Booking.newid()          #id of booking
        bookings[user].append(self) #append it to the bookings of a user

    #create a booking
    @app.route("/booking",methods=['POST'],endpoint='bookingPOST')
    def put():
        hotel_id = request.args.get('hotel')
        room_id = request.args.get('room')
        user = request.args.get('user')
        user_key = request.args.get('key')
        start = request.args.get('start')
        end = request.args.get('end')

        if(user == None or not user.isdigit() or
            user_key == None):
                return 'you have to auth', 401

        if( start == None or
            end == None or
            hotel_id == None or not hotel_id.isdigit() or
            room_id == None or not room_id.isdigit()):
            return "start, end, room or hotel is invalide", 400

        try:
            start = dateparse.parse(start).timestamp()
            end = dateparse.parse(end).timestamp()
        except Exception as e:
            return "start or end is not a date", 400

        hotelRooms = rooms.get(int(hotel_id))
        if(hotelRooms == None):
            return "cannot find hotel rooms", 400

        curr_user = users.get(int(user))
        if(curr_user == None or curr_user.passkey != user_key):
            'pass doesnt match or no rights', 403

        for ob in hotelRooms:
            if(ob.id == int(room_id)):
                roomReservations = reservations.get(int(room_id))
                if(roomReservations == None):
                    Reservation(int(room_id),int(user),start,end)
                    return json.dumps(Booking(int(room_id),int(user),start,end).__dict__), 201,{'content-type':'application/json'}
                else:
                    for res in roomReservations:
                        if ((res.start_date <= start and res.end_date >= start) or
                            (res.start_date <= end and res.end_date >= end)):
                            print(res.__dict__)
                            abort(404)
                    Reservation(int(room_id),int(user),start,end)
                    return json.dumps(Booking(int(room_id),int(user),start,end).__dict__), 201,{'content-type':'application/json'}
        abort(404)

    #get bookings (of user)
    @app.route("/bookings",methods=['GET'],endpoint='booking/listGet')
    def get():
        user = request.args.get('user')
        if(user == None or not user.isdigit()):
            json.dumps([[ob.__dict__ for ob in bookings[x]] for x in bookings]), 200,{'content-type':'application/json'}
        userBookings = bookings.get(int(user))
        if(userBookings == None):
            abort(404)
        return json.dumps([ob.__dict__ for ob in userBookings]), 200,{'content-type':'application/json'}


    #delete the booking -> just creator
    @app.route("/booking",methods=['DELETE'],endpoint='bookingDelete')
    def get():
        user1 = request.args.get('booker')
        user2 = request.args.get('user')
        user_key = request.args.get('key')
        booking_id = request.args.get('booking')
        if(user1 == None or not user1.isdigit() or
            booking_id == None or not booking_id.isdigit()):
            return "booker or booking id is invalide", 400
        if(user2 == None or not user2.isdigit() or
            user_key == None):
            return 'you have to auth', 401
        curr_user = users.get(int(user2))
        if(curr_user == None or curr_user.passkey != user_key or curr_user.is_creator != True):
            'pass doesnt match or no rights', 403
        userBookings = bookings.get(int(user1))
        if(userBookings == None):
            return "user has no bookings", 400
        i = 0
        for ob in userBookings:
            if(ob.id == int(booking_id)):
                if(len(userBookings) == 1):
                    del bookings[int(user1)]
                else:
                    del bookings[int(user1)][i]
                return json.dumps(ob.__dict__), 204,{'content-type':'application/json'}
            i += 1
        abort(404)

    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "LodgingReservation"
        dict["underName"] = self.user
        dict["checkinTime"] = self.start_date
        dict["checkoutTime"] = self.end_date
        dict["@type"] = "HotelRoom"
        dict["identifier"] = self.room
        return dict


#################################################################################################
#################################################################################################
#################################################################################################
#####################################      OFFER     ############################################
#################################################################################################
#################################################################################################
class Offer(Resource):
    newid = itertools.count().__next__
    def __init__(self, room, hotel, start, end, price):
        self.room = room
        self.start_date = start
        self.end_date = end
        self.hotel = hotel
        self.id = Offer.newid()
        delta = datetime.fromtimestamp(int(end)) - datetime.fromtimestamp(int(start))
        if(price[:-1].isdigit()):
            self.price = delta.days * int(price[:-1])
        else:
            self.price = "price not found in db"
        self.created = datetime.now().timestamp()

    #get an offer
    @app.route("/offer",methods=['GET'],endpoint='offerGet')
    def get():
        hotel_id = request.args.get('hotel')
        room_id = request.args.get('room')
        start = request.args.get('start')
        end = request.args.get('end')
        if(hotel_id == None or not hotel_id.isdigit() or
            room_id == None or not room_id.isdigit()):
            return "invalid hotel or room id", 400

        try:
            start = dateparse.parse(start).timestamp()
            end = dateparse.parse(end).timestamp()
        except Exception as e:
            return "start or end is no date", 400

        hotelRooms = rooms.get(int(hotel_id))
        if(hotelRooms == None):
            return "no hotelrooms found", 400
        for ob in hotelRooms:
            if(int(room_id) == ob.id):
                return json.dumps(Offer(room_id, hotel_id, start, end, ob.price).__dict__),200,{'content-type':'application/json'}
        abort(404)

    def dict(self):
        dict = defaultdict(list)
        dict["@context"] = "http://schema.org"
        dict["@type"] = "Offer"
        dict["availabilityStarts"] = self.start_date
        dict["availabilityEnds"] = self.end_date
        dict["@type"] = "Hotel"
        dict["identifier"] = self.hotel
        dict["@type"] = "HotelRoom"
        dict["identifier"] = self.hotel

        return dict





#################################################################################################
#################################################################################################
#################################################################################################
############################################## MAIN #############################################
#################################################################################################
#################################################################################################

# read our data from db.json
def readJsonOld():
    data = json.load(open('db.json'))
    for hotel in data:
        tmp1 = Location(hotel["cityName"],hotel["latitude"],hotel["longitude"],hotel["countryName"])
        if (hotel["price"] == '' or hotel["price"]==99999):
            price = str(randint(16, 60))+ "$"
        else:
            price = str(hotel["price"]) + "$"
        if (len(hotel["facilities"]) > 4 ):
            tmp2 = Hotel(hotel["hotelName"],tmp1.id,hotel["facilities"],hotel["stars"],price)
            url = hotel["url"]
            if(len(url)>4):
                Website(tmp2.id,url)


if __name__ == '__main__':
    print("Admin:")
    print(User("admin","","admin@api.at",True,"root").id)
    readJsonOld()
    #TODO read and save
    app.run(debug=True)
