import json

# the default directory for the profiles
userProfilesDir = "./data/profiles.json"

def loadProfiles():
    """grab all the profiles dicts from the external file"""
    with open(userProfilesDir, "r") as infile:
        profiles = json.loads("\n".join(infile.readlines()))
        infile.close()
        return profiles


def dumpProfiles(profiles):
    """write profiles to the external file"""
    with open(userProfilesDir, "w") as outfile:
        outfile.writelines(json.dumps(profiles, indent=4))
        outfile.close()

def sortProfiles():
    profiles = loadProfiles()

    # sort the profiles in decending order, so the first 5 profiles are the highest scores
    # use the key 'score' in the dict to sort them.
    profiles = sorted(profiles, key=lambda k: k['score'], reverse=True)

    dumpProfiles(profiles)

def getHighscores():
    """get a sorted dict array of the top 5 highscores"""

    # sort and load the profiles from the external file
    sortProfiles()
    profiles = loadProfiles()

    highscores = []
    for i in range(0, 5):
        # make sure we aren't exceeding the index of the array
        if i < len(profiles):
            # omit the password from the dict
            highscore = {
                'username': profiles[i]['username'],
                'score': profiles[i]['score']
            }
            highscores.append(highscore)
        else:
            break

    return highscores