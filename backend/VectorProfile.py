import numpy as np

class VectorProfile:

    def __init__(self, profileId, profileLength=0):
        self.profileId = profileId
        self.vector = np.zeros(profileLength)
