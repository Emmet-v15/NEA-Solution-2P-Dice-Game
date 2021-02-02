import filetools

# a class to represent a player
class User():
    def __init__(self, username, points):
        """initialise with username and points"""
        self.username = username
        self.points = points

    def addPoints(self, points):
        """increment the user's points"""
        self.points += points
    
    def save(self):
        """save score to external file, if it is a new highscore and return True if it is"""

        # load all user profiles
        profiles = filetools.loadProfiles()

        highscore = False
        
        # loop through all profiles
        for profile in profiles:
            # check if the username matches
            if profile['username'] == self.username:
                # check if highscore
                if profile['score'] < self.points:
                    profile['score'] = self.points
                    highscore = True
        
        # save the newly modified profiles
        filetools.dumpProfiles(profiles)
        
        return highscore