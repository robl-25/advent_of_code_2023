CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def parse_game(rounds):
    for r in rounds:
        cubes = r.split(', ')

        for cube in cubes:
            number, color = cube.split(' ')

            if int(number) > CUBES[color]:
              return False

    return True


with open('input.txt') as file:
    result = 0

    for line in file:
        line = line.strip()

        game_id = int(line.split(':')[0].split('Game ')[1])
        rounds = line.split(': ')[1].split('; ')

        if parse_game(rounds):
            result += game_id

    print(result)