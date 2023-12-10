from math import sqrt


class Race:
    def __init__(self, time, distance):
        self.time = time
        self.distance = distance

    def __repr__(self):
        return f'Race(time={self.time}, distance={self.distance})'

    def determine_win_numbers(self):
        x1 = (- self.time + sqrt(self.time ** 2 - 4 * self.distance)) / - 2
        x2 = (- self.time - sqrt(self.time ** 2 - 4 * self.distance)) / - 2

        x1 = round(x1)
        x2 = round(x2)

        offset = 0

        if (self.time - x1) * x1 <= self.distance and (self.time - x2) * x2 <= self.distance:
            offset = -1

        if (self.time - x1) * x1 > self.distance and (self.time - x2) * x2 > self.distance:
            offset = 1

        return x2 - x1 + offset


def parse_races(lines):
    times = [int(t) for t in lines[0].split(':')[1].strip().split(' ') if t != '']
    distances = [int(d) for d in lines[1].split(':')[1].strip().split(' ') if d != '']

    return [Race(t, d) for t, d in zip(times, distances)]


with open('day-6/part-1.txt') as f:
    lines = f.read().splitlines()

result = 1

for race in parse_races(lines):
    result *= race.determine_win_numbers()

print(result)
