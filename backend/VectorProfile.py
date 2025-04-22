import numpy as np

class VectorProfile:

    def __init__(self, profileId, profileLength=0):
        self.profileId = profileId
        self.profile = np.zeros(profileLength)
