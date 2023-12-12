def parse_game(rounds):
    minimum_cubes = {
        'red': 0,
        'blue': 0,
        'green': 0,
    }

    for r in rounds:
        cubes = r.split(', ')

        for cube in cubes:
            number, color = cube.split(' ')

            if int(number) > minimum_cubes[color]:
             minimum_cubes[color] = int(number)

    return minimum_cubes['red'] * minimum_cubes['blue'] * minimum_cubes['green']


with open('input.txt') as file:
    result = 0

    for line in file:
        line = line.strip()
        rounds = line.split(': ')[1].split('; ')

        result += parse_game(rounds)

    print(result)