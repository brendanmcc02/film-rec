from VectorProfile import *

class GenreVectorProfile(VectorProfile):

    sumOfWeights = 0.0
    quantityFilmsWatched = 0
    weightedMeanRating = 0.0
    
    def __init__(self, profileId, profileLength = 0):
        super().__init__(profileId, profileLength)
        