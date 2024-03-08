import numpy as np
import json


def main():
    # a = np.array([0.82370058, 0.81023987, 0.38494354, 0.50288582, 0.22283563, 0.15909661, 0.39347553, 0.19623588,
    #               0.0281054, 0.8, 0.09836888, 0.11894605, 0.00301129, 0.05269762, 0.03061481, 0.03613551, 0.00953576,
    #               0.09535759, 0.0, 0.13801757, 0.14404015, 0.03161857, 0.16361355, 0.06072773, 0.01053952])
    a = np.array([0.38494354, 0.50288582, 0.22283563, 0.15909661, 0.39347553, 0.19623588,
                  0.0281054, 0.8, 0.09836888, 0.11894605, 0.00301129, 0.05269762, 0.03061481, 0.03613551, 0.00953576,
                  0.09535759, 0.0, 0.13801757, 0.14404015, 0.03161857, 0.16361355, 0.06072773, 0.01053952])
    # try to create the 'ideal' film:
    # year is as high as possible
    # imdbRating is as high as possible
    # pick 3 genres that have the highest weight
    # b = np.array([1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    b = np.array([0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Dune pt 2
    # b = np.array([1.0, 0.9638554216867469, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    sim = round(cosineSimilarity(a, b) * 100.0, 2)
    # sim = np.linalg.norm(a-b)

    print(str(sim))


# gets the cosine similarity between two vectors
def cosineSimilarity(A, B):
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))


if __name__ == "__main__":
    main()

# DUNE PT 2
# dot prod:  3.292484031566265
# mag A: 1.659680112273714
# mag B: 2.220139021303607
# 89.36

# 'IDEAL' FILM:
# dot prod:  3.3303018000000004
# mag A: 1.659680112273714
# mag B: 2.23606797749979
# 89.74
