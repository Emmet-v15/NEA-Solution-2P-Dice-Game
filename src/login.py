import text, hashlib, filetools, binascii, os  # import libraries, hashlib, os, binascii & uuid are inbuilt, but not mine.
from user import User  # import my user class so we can make user objects


def getUsername():
    """
    get user input for username from console
    and checks if the username is of appropriate length

    returns a username
    """

    usernameValid = False
    while not usernameValid:
        username = input(text.blue("Username\n:"))
        if len(username) < 3:
            print(text.red("Username too short (3-12 chars required)"))
        elif len(username) > 12:
            print(text.red("Username too long (3-12 chars required)"))
        else:
            usernameValid = True

    return username


def getPassword():
    """
    get user input for password from console, checks if it is of appropriate length
    returns a string
    """

    # get an appropriate password from the user
    passwordValid = False
    while not passwordValid:
        password = input(text.blue("Password\n:"))
        if len(password) < 8:
            print(text.red("Password too short (8-24 chars required)"))
        elif len(password) > 24:
            print(text.red("Password too long (8-24 chars required)"))
        else:
            passwordValid = True

    return password


def hash(text):
    """
    i am using the hashlib library for the pbkdf2 cryptographic hash function which is commonly
    used for hashing passwords to store in a database
    """

    # generate a random hash using the os library, and then enlarge it using the sha256 function
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

    # hash the text using the generated random salt using the pbkdf2 function
    pwdhash = hashlib.pbkdf2_hmac('sha512', text.encode('utf-8'), salt, 100000)

    # convert the text into hexadecimal to make it neater
    pwdhash = binascii.hexlify(pwdhash)

    # return the hashed text with the salt concatenated to it, encoded in ascii
    return (salt + pwdhash).decode('ascii')


def verifyHash(hash, text):
    """
    check if a hash matches a string
    """

    # un concatenate the stored hash into the hash and the salt
    salt = hash[:64]  # first 64 items in the string
    hash = hash[64:]  # last 64 items in the string

    # hash the text using the same function and salt, then convert it to hex
    newHash = hashlib.pbkdf2_hmac('sha512', text.encode('utf-8'),
                                  salt.encode('ascii'), 100000)
    newHash = binascii.hexlify(newHash).decode('ascii')

    # return true if the new hash matches the old hash
    return newHash == hash


def register():
    """
    Get new user credentials from the console to store into an external file to verify the user
    in the future
    """

    # load profiles from external file using my filetools library
    profiles = filetools.loadProfiles()

    print(text.blue("====Register===="))

    # get an appropriate username from the user that is not already registered
    usernameValid = False
    while not usernameValid:
        username = getUsername()
        if len(profiles) != 0:
            usernameValid = True
            # loop through the array of python dicts (json objects)
            for profile in profiles:
                # profile['username'] is the username from the external file that corresponds with the current dict
                if profile['username'] == username:
                    usernameValid = False
            if not usernameValid:
                print(text.red("Username already exists"))
        else:
            usernameValid = True

    # get an appropriate password from the user to go with their username
    password = getPassword()
    print(text.blue("================"))

    print(text.green("Logged in"))

    # create a dict which stores user's data
    profiles.append({
        "username": username,
        "password": hash(password),
        "score": 0
    })

    # write the dict into the json array in the external file to save it for later
    filetools.dumpProfiles(profiles)

    # create a user object using my User class and return it
    return User(username, 0) # the 0 represents the points


def login(notUsername=None):
    """
    Get a user's credentials from the console and authorise them
    """

    # load profiles from external file using my filetools library
    profiles = filetools.loadProfiles()

    print(text.blue("=====Login======"))

    # get user credentials which match against a profile that is stored externally
    loggedIn = False
    while not loggedIn:
        username = getUsername()
        if username == "exit":
            return False

        # notUsername is the variable which stores the username for the first user
        # this is used to prevent both players being on one account
        if username != notUsername or notUsername == None:
            userExists = False
            # loop through the array of python dicts (json objects)
            for profile in profiles:
                # check if the username matches
                if profile['username'] == username: 
                    userExists = True
                    # verify the password using the hash from the stored file and user input
                    if verifyHash(profile['password'], getPassword()):
                        print(text.green("Logged in"))
                        return User(username, profile['score'])
                    else:
                        print(text.red("Invalid Password"))
                        break
            if not userExists:
                print(text.red("User not found"))
        else:
            print(text.red("User already logged in as ") + text.orange("USER 1"))

    print(text.blue("================"))


def getUsers():
    """This function is used to get two authenticated users from the console"""

    users = [None, None]

    for i in range(2):
        print(
            text.orange("USER #" + str(i + 1)) +
            text.blue("\n1. Login \n2. Register"))

        # get two users from the console using the functions above
        success = False
        while not success:
            authMode = input(text.blue(":"))
            if authMode.casefold() == "login" or authMode == "1":
                # keep looping until we have the 'i'th user
                while users[i] == None:
                    if i:
                        users[i] = login(users[0].username)
                    else:
                        users[i] = login()
                    success = True

            elif authMode.casefold() == "register" or authMode == "2":
                # keep looping until we have the 'i'th user
                while users[i] == None:
                    users[i] = register()
                success = True
            else:
                print(text.red('Invalid Choice (type 1 or 2)'))
                success = False
    return users

def dummyUsers():
    """return dummy users to speed up debugging"""
    return [User("user1", 0), User("user2", 0)]