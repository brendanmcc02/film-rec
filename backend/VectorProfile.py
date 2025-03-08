import numpy as np

class VectorProfile:

    def __init__(self, _profileId, _profileLength=0):
        self.profileId = _profileId
        self.profile = np.zeros(_profileLength)
