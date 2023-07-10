import csv
import sys
from datetime import datetime
from enum import Enum


class Candidate(Enum):
    BOTH_CANDIDATE = 'Both Candidate'
    DONALD_TRUMP = 'Donald Trump'
    JOE_BIDEN = 'Joe Biden'


class State(Enum):
    NEW_YORK = 'new york'
    CALIFORNIA = 'california'


def read_csv(file):
    reader = csv.reader(file)
    next(reader)  # titles
    for row in reader:
        yield row


def get_tweet_candidate(tweet):
    tweet = tweet.lower()

    if ('trump' in tweet) and ('biden' in tweet):
        candidate = Candidate.BOTH_CANDIDATE
    elif 'trump' in tweet:
        candidate = Candidate.DONALD_TRUMP
    elif 'biden' in tweet:
        candidate = Candidate.JOE_BIDEN
    else:
        return None

    return candidate.value


def get_state(lat, long):
    if lat == '' or long == '':
        return None

    if (-79.7624 < float(long) < -71.7517) and (40.4772 < float(lat) < 45.0153):
        return State.NEW_YORK.value

    if (-124.6509 < float(long) < -114.1315) and (32.5121 < float(lat) < 42.0126):
        return State.CALIFORNIA.value

    return None


def is_tweet_acceptable(tweet, created_at, state):
    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
    if not '09:00:00' <= str(created_at.time()) <= '17:00:00':
        return False

    if (state is None) or (get_tweet_candidate(tweet) is None):
        return False

    return True


def get_candidate_list(candidate):
    return [candidate == Candidate.BOTH_CANDIDATE.value, candidate == Candidate.JOE_BIDEN.value,
            candidate == Candidate.DONALD_TRUMP.value]


def get_output(state, candidate):
    candidates = get_candidate_list(candidate)
    state = state.lower().replace(' ', ';-;')

    return state, candidates[0], candidates[1], candidates[2], 1


def main():
    rows = read_csv(sys.stdin)

    for row in rows:
        state = get_state(row[13], row[14])

        if not is_tweet_acceptable(row[2], row[0], state):
            continue

        print('%s %d %d %d %d' % get_output(state, get_tweet_candidate(row[2])))


if __name__ == "__main__":
    main()
