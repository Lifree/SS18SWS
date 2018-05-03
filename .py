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