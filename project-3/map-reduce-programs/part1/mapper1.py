# !/usr/bin/env python

import csv
import sys
from enum import Enum


class Candidate(Enum):
    BOTH_CANDIDATE = 'Both Candidate'
    DONALD_TRUMP = 'Donald Trump'
    JOE_BIDEN = 'Joe Biden'


class Source(Enum):
    TWITTER_WEB_APP = 'Twitter Web App'
    TWITTER_FOR_IPHONE = 'Twitter for iPhone'
    TWITTER_FOR_ANDROID = 'Twitter for Android'


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


def get_source_list(source):
    return [source == Source.TWITTER_WEB_APP.value, source == Source.TWITTER_FOR_IPHONE.value,
            source == Source.TWITTER_FOR_ANDROID.value]


def get_output(candidate, likes, retweet_count, source):
    sources = get_source_list(source)
    candidate = candidate.replace(' ', ';-;')

    return candidate, int(float(likes)), int(float(retweet_count)), sources[0], sources[1], sources[2]


def main():
    rows = read_csv(sys.stdin)

    for row in rows:
        candidate = get_tweet_candidate(row[2])
        if candidate is None:
            continue

        print('%s %d %d %d %d %d' % get_output(candidate, row[3], row[4], row[5]))


if __name__ == "__main__":
    main()
