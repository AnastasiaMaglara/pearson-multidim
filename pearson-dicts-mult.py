import statistics
from math import sqrt

# define dimensions used in the overall process
DIMENSIONS = ["overall", "joy", "anger", "sadness"]

#define weights for the dimensions
dimensionWeights = {"overall": 0.6, "joy": 0.15, "anger": 0.15, "sadness": 0.1}

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

numUsers = 100

ratings = [dict() for x in range(numUsers)]

# read <userid, itemid, rating> triples from dataset
# rating has multiple dimensions; example dimensions are
# "overall", "joy", "anger", "sadness"
# all dimensions are rated between 1 and 5, with 1 being the lowest and 5 being the highest
ratings[1][10] = {}
ratings[1][10]['overall'] = 2;
ratings[1][10]['joy'] = 0.2;
ratings[1][10]['anger'] = 0.2;
ratings[1][10]['sadness'] = 0.6;
ratings[1][20] = {}
ratings[1][20]['overall'] = 1;
ratings[1][20]['joy'] = 0;
ratings[1][20]['anger'] = 0.6;
ratings[1][20]['sadness'] = 0.4;
ratings[1][30] = {};
ratings[1][30]['overall'] = 5;
ratings[1][30]['joy'] = 0.9;
ratings[1][30]['anger'] = 0.0;
ratings[1][30]['sadness'] = 0.1;
ratings[2][10] = {};
ratings[2][10]['overall'] = 2;
ratings[2][10]['joy'] = 0.2;
ratings[2][10]['anger'] = 0.3;
ratings[2][10]['sadness'] = 0.5;
ratings[2][30] = {};
ratings[2][30]['overall'] = 4;
ratings[2][30]['joy'] = 0.8;
ratings[2][30]['anger'] = 0.1;
ratings[2][30]['sadness'] = 0.1;
ratings[2][100] = {};
ratings[2][100]['overall'] = 5;
ratings[2][100]['joy'] = 0.95;
ratings[2][100]['anger'] = 0.0;
ratings[2][100]['sadness'] = 0.05;


avgUserRatings = []
for i in range(0, numUsers):
  avgUserRatings.insert(i, avgRating(ratings[i]))

print(pearsonSim(ratings[1], avgUserRatings[1], ratings[2], avgUserRatings[2]))