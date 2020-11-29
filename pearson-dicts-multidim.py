import statistics
from math import sqrt
import prediction
import recommendation

# define dimensions used in the overall process
DIMENSIONS = ["Overall", "Joy", "Anger", "Sadness"]

#define weights for the dimensions
dimensionWeights = {"Overall": 0.6, "Joy": 0.15, "Anger": 0.15, "Sadness": 0.1}

AVERAGE_UNCOMPUTABLE = (-1000)
PEARSON_UNCOMPUTABLE_NO_COMMON = (-1001)
PEARSON_UNCOMPUTABLE_ZERO_VARIANCE = (-1002)

def pearsonSim(x, avg_x, y, avg_y):
    if ((avg_x ==  AVERAGE_UNCOMPUTABLE) or (avg_y == AVERAGE_UNCOMPUTABLE)):
      return PEARSON_UNCOMPUTABLE_NO_COMMON

    similarityDimensionNominators = {}
    similarityDimensionDenominatorsX = {}
    similarityDimensionDenominatorsY = {}
    similarityDimensionCounts = {}
    for d in DIMENSIONS:
      similarityDimensionNominators[d] = 0
      similarityDimensionDenominatorsX[d] = 0
      similarityDimensionDenominatorsY[d] = 0
      similarityDimensionCounts[d] = 0
    for key in x:
        if key in y:
          for d in DIMENSIONS:
            if (d in x[key]) and (d in y[key]):
               xdiff = x[key][d] - avg_x[d]
               ydiff = y[key][d] - avg_y[d]
               similarityDimensionNominators[d] += xdiff * ydiff
               similarityDimensionDenominatorsX[d] += xdiff * xdiff
               similarityDimensionDenominatorsY[d] += ydiff * ydiff
               similarityDimensionCounts[d] += 1

    pearsonNominator = 0
    pearsonDenominator = 0
    for d in DIMENSIONS:
      if ((similarityDimensionCounts[d] > 0) and (similarityDimensionDenominatorsX[d] > 0) and (similarityDimensionDenominatorsY[d] > 0)):
        pearsonNominator += dimensionWeights[d] * (similarityDimensionNominators[d] / sqrt(similarityDimensionDenominatorsX[d] * similarityDimensionDenominatorsY[d]))
        pearsonDenominator += dimensionWeights[d]

    if (pearsonDenominator == 0):
        return PEARSON_UNCOMPUTABLE_ZERO_VARIANCE
    else:
        return pearsonNominator / pearsonDenominator


def avgRating(ratingDict):
  if (len(ratingDict) == 0):
    return AVERAGE_UNCOMPUTABLE
  result = {}
  for dimension in DIMENSIONS:
    dsum = 0
    dcount = 0
    for r in ratingDict.values():
      dsum += r[dimension]
      dcount += 1
    result[dimension] = dsum / dcount
  return result

numUsers = 613

ratings = [dict() for x in range(numUsers)]
ratings = recommendation.recomment(numUsers)
# read <userid, itemid, rating> triples from dataset
# rating has multiple dimensions; example dimensions are
# "overall", "joy", "anger", "sadness"
# all dimensions are rated between 1 and 5, with 1 being the lowest and 5 being the highest

avgUserRatings = []
for i in range(0, numUsers):
  avgUserRatings.insert(i, avgRating(ratings[i]))

sim=[[0 for x in range(numUsers)]for y in range(numUsers)]
for i in range(0, numUsers):
    for j in range(0, numUsers):
       sim[i][j] = pearsonSim(ratings[i], avgUserRatings[i], ratings[j], avgUserRatings[j])

print('343\n',ratings[343],'\n','266\n', ratings[266])
print(pearsonSim(ratings[343], avgUserRatings[343], ratings[266], avgUserRatings[266]))