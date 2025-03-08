from VectorProfile import *

class GenreVectorProfile(VectorProfile):

    sumOfWeights = 0.0
    quantityFilmsWatched = 0
    weightedMeanRating = 0.0
    
    def __init__(self, _profileId, _profileLength = 0):
        super().__init__(_profileId, _profileLength)
        