# define dimensions used in the overall process

SIMILARITY_THRESHOLD = 0
MAX_RATING = 5
MIN_RATING = 1
NO_PREDICTION = -1003

def predictRatingPearson(ratings, avgUserRatings, sim, numUsers, userToPredict, itemToPredict):
  count = 0
  numerator = 0
  denominator = 0
 
  for userCount in range(0, numUsers):
    if ((itemToPredict in ratings[userCount]) and (sim[userToPredict][userCount] > SIMILARITY_THRESHOLD)):
      numerator += (ratings[userCount][itemToPredict] - avgUserRatings[userCount ]) * sim[userToPredict][userCount]
      denominator += sim[userToPredict][userCount]

  if (denominator > 0):
    retval = (avgUserRatings[userToPredict]) + (numerator / denominator)
    if (retval > MAX_RATING):
        retval = MAX_RATING;
    elif (retval < MIN_RATING):
        retval = MIN_RATING
    return retval
  else:
    return NO_PREDICTION