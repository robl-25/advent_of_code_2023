with open('day-4/part-1.txt') as file:
  result = 0

  for line in file:
    numbers = line.split(': ')[1]
    win_num, my_num = numbers.split('| ')
    win_num = [int(num) for num in win_num.strip().split(' ') if num.isdigit()]
    my_num = [int(num) for num in my_num.strip().split(' ') if num.isdigit()]

    length = len(set(win_num) & set(my_num))

    if length != 0:
      result += 2**(length - 1)

  print(result)