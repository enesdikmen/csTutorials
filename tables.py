class Topic:
    def __init__(self, name):
        self.name = name

class Educator:
    def __init__(self, name, infoURL, id=None, avgRating = None):
        self.id = id
        self.name = name
        self.infoURL = infoURL
        self.avgRating = avgRating

class Tutorial:
    def __init__(self, title, educatorID, platform, url, skill, lenght = None, info = None, ratingNum=0, tutorialRating = None):
        self.title = title
        self.educatorID = educatorID
        self.platform = platform
        self.url = url
        self.skill = skill
        self.length = lenght
        self.info = info
        self.ratingNum = ratingNum
        self.tutorialRating = tutorialRating
        
