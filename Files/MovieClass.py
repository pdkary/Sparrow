class Movie:
    def __init__(self,title,magnet,image=None,rating=0):
        self.title = title
        self.magnet = magnet
        self.image = image
        self.rating = rating

    def getTitle(self):
        return self.title

    def getMag(self):
        return self.magnet

    def getImage(self):
        return image
