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
    TEXAS = 'texas'
    CALIFORNIA = 'california'
    FLORIDA = 'florida'


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


def is_tweet_acceptable(tweet, created_at, state):
    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
    if not '09:00:00' <= str(created_at.time()) <= '17:00:00':
        return False

    if state.lower() not in [State.NEW_YORK.value, State.TEXAS.value, State.CALIFORNIA.value, State.FLORIDA.value]:
        return False

    if get_tweet_candidate(tweet) is None:
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
        if not is_tweet_acceptable(row[2], row[0], row[18]):
            continue

        print('%s %d %d %d %d' % get_output(row[18], get_tweet_candidate(row[2])))


if __name__ == "__main__":
    main()
