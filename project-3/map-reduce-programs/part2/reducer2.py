import sys
from itertools import groupby
from operator import itemgetter


def read_mapper_output(file):
    for line in file:
        yield line.rstrip().split(' ')


def main():
    data = read_mapper_output(sys.stdin)

    for state, group in groupby(data, itemgetter(0)):
        try:
            counts = [0, 0, 0, 0]
            for values in group:
                values = list(map(int, values[1:]))
                counts = [sum(count) for count in zip(counts, values)]

            counts[:-1] = [i/counts[-1] for i in counts[:-1]]
            state = state.replace(';-;', ' ')
            counts = ' '.join(list(map(str, counts)))

            print(state, counts)
        except ValueError:
            pass


if __name__ == "__main__":
    main()
