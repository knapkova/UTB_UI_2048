# imports
import numpy as np
import copy as cp

# adds given value to total score
def add_score(sc, val):
    sc += val
    return sc


# move the grid to the left and update score
def move_left(grid, score):
    for i in range(4):
        non_zero = [x for x in grid[i, :] if x != 0]
        zero = [0] * (4 - len(non_zero))
        grid[i, :] = np.array(non_zero + zero)
        for j in range(3):
            if grid[i, j] == grid[i, j + 1]:
                grid[i, j] *= 2
                score = add_score(score, grid[i, j])
                grid[i, j + 1] = 0
        non_zero = [x for x in grid[i, :] if x != 0]
        zero = [0] * (4 - len(non_zero))
        grid[i, :] = np.array(non_zero + zero)
    return (grid, score)


# move the grid to the right and update score
def move_right(grid, score):
    for i in range(4):
        non_zero = [x for x in grid[i, :] if x != 0]
        zero = [0] * (4 - len(non_zero))
        grid[i, :] = np.array(zero + non_zero[::-1])
        for j in range(3, 0, -1):
            if grid[i, j] == grid[i, j - 1]:
                grid[i, j] *= 2
                score = add_score(score, grid[i, j])
                grid[i, j - 1] = 0
        non_zero = [x for x in grid[i, :] if x != 0]
        zero = [0] * (4 - len(non_zero))
        grid[i, :] = np.array(zero + non_zero[::-1])
    return (grid, score)


# move the grid up and update score
def move_up(grid, score):
    for i in range(4):
        non_zero = [x for x in grid[:, i] if x != 0]
        zero = [0] * (4 - len(non_zero))
        grid[:, i] = np.array(non_zero + zero)
        for j in range(3):
            if grid[j, i] == grid[j + 1, i]:
                grid[j, i] *= 2
                score = add_score(score, grid[j, i])
                grid[j + 1, i] = 0
        non_zero = [x for x in grid[:, i] if x != 0]
        zero = [0] * (4 - len(non_zero))
        grid[:, i] = np.array(non_zero + zero)
    return (grid, score)


# move the grid down and update score
def move_down(grid, score):
    for i in range(4):
        non_zero = [x for x in grid[:, i] if x != 0]
        zero = [0] * (4 - len(non_zero))
        grid[:, i] = np.array(zero + non_zero[::-1])
        for j in range(3, 0, -1):
            if grid[j, i] == grid[j - 1, i]:
                grid[j, i] *= 2
                score = add_score(score, grid[j, i])
                grid[j - 1, i] = 0
        non_zero = [x for x in grid[:, i] if x != 0]
        zero = [0] * (4 - len(non_zero))
        grid[:, i] = np.array(zero + non_zero[::-1])
    return (grid, score)


# generates new tile
def add_new_number(grid):
    zero_indices = np.where(grid == 0)
    if len(zero_indices[0]) == 0:
        return False
    index = np.random.choice(len(zero_indices[0]))
    i, j = zero_indices[0][index], zero_indices[1][index]
    grid[i, j] = 2 if np.random.random() < 0.9 else 4
    return True


# checks whether it is Game Over
def check_game_over(grid):
    if np.all(grid) == False:
        return False

    for row in range(4):
        for col in range(4):
            if row != 3:
                if (grid[row, col] == grid[row + 1, col]):
                    return False
            if col != 3:
                if (grid[row, col] == grid[row, col + 1]):
                    return False

    return True


# checks for potential win
def check_win(grid):
    return 2048 in grid


# move the grid in specified direction, check for win or lose
# raises RuntimeError "GO" if the game is in GAME OVER state
# raises RuntimeError "WIN" if the game is in WIN state
def play_2048(grid, move, score):
    orig_grid = cp.deepcopy(grid)

    if check_game_over(grid):
        raise RuntimeError("GO")

    if move == 'left':
        grid, score = move_left(grid, score)
    elif move == 'right':
        grid, score = move_right(grid, score)
    elif move == 'up':
        grid, score = move_up(grid, score)
    elif move == 'down':
        grid, score = move_down(grid, score)
    else:
        raise ValueError("Invalid move")

    if check_win(grid):
        raise RuntimeError("WIN")

    # check whether the move was possible
    if np.array_equal(grid, orig_grid) == False:
        add_new_number(grid)
    return (grid, score)


# starts a new game by generating two tiles and setting score to 0
def new_game():
    score = 0
    grid = np.zeros((4, 4), dtype=int)
    add_new_number(grid)
    add_new_number(grid)

    return (grid, score)


# print of the grid
def print_grid(grid, score):
    print('Score: ', score)
    print("+----+----+----+----+")
    for i in range(4):
        line = "|"
        for j in range(4):
            if grid[i, j] == 0:
                line += "    |"
            else:
                line += "{:4d}|".format(grid[i, j])
        print(line)
        print("+----+----+----+----+")

# Check if a move is possible
def is_move_possible(grid, move):
    temp_grid = cp.deepcopy(grid)
    if move == 'left':
        temp_grid, _ = move_left(temp_grid, 0)
    elif move == 'right':
        temp_grid, _ = move_right(temp_grid, 0)
    elif move == 'up':
        temp_grid, _ = move_up(temp_grid, 0)
    elif move == 'down':
        temp_grid, _ = move_down(temp_grid, 0)
    return not np.array_equal(grid, temp_grid)

# Algorithm to prioritize upper right corner moves
def prioritize_upper_right(grid, score):
    directions = ['up', 'right', 'left', 'down']
    for move in directions:
        if is_move_possible(grid, move):
            grid, score = play_2048(grid, move, score)
            if check_game_over(grid):
                raise RuntimeError("GO")
            return grid, score
    return grid, score

def prioritize_upper_left(grid, score):
    directions = ['up', 'left', 'right', 'down']
    for move in directions:
        if is_move_possible(grid, move):
            grid, score = play_2048(grid, move, score)
            if check_game_over(grid):
                raise RuntimeError("GO")
            return grid, score
    return grid, score

def prioritize_left_upper(grid, score):
    directions = ['up', 'left', 'right', 'down']
    for move in directions:
        if is_move_possible(grid, move):
            grid, score = play_2048(grid, move, score)
            if check_game_over(grid):
                raise RuntimeError("GO")
            return grid, score
    return grid, score



def prioritize_lower_left(grid, score):
    directions = ['left', 'down','up', 'right']
    for move in directions:
        if is_move_possible(grid, move):
            grid, score = play_2048(grid, move, score)
            if check_game_over(grid):
                raise RuntimeError("GO")
            return grid, score
    return grid, score

def prioritize_lower_right(grid, score):
    directions = [ 'right','down','up','left']
    for move in directions:
        if is_move_possible(grid, move):
            grid, score = play_2048(grid, move, score)
            if check_game_over(grid):
                raise RuntimeError("GO")
            return grid, score
    return grid, score



with open("results.csv","w") as f:
    f.write("Type;First_direction;Try;Score;Moves;Status;Category\n")

    for repete in range(30):
        #Random direction solver
        grid, score = new_game()
        for i in range(1000):
            direction = np.random.choice(('left','right','up','down'))
            try:
                grid, score = play_2048(grid, direction, score)
            except RuntimeError as inst:
                if(str(inst)=="GO"):
                    print("Random GAME OVER in ",(i+1)," moves")
                    f.write("Random;" + str(direction) + ";" + str(repete) + ";" + str(score) + ";" + str(i + 1) + ";Loose;Random\n")
                elif(str(inst)=="WIN"):
                    print("WIN in ",(i+1)," moves")
                    f.write("Random;" + str(direction) + ";" + str(repete) + ";" + str(score) + ";" + str(i + 1) + ";Win;Random\n")
                break

    for repete in range(30):
        # Prioritize upper right corner solver
        grid, score = new_game()
        first_direction = None
        for i in range(1000):
            if first_direction is None:
                first_direction = 'up'
            try:
                grid, score = prioritize_upper_right(grid, score)
            except RuntimeError as inst:
                if str(inst) == "GO":
                    print("GAME OVER in ", (i + 1), " moves")
                    f.write(f"Prioritize_Upper_Right;{first_direction};{repete};{score};{i + 1};Loose;Heuristic\n")
                elif str(inst) == "WIN":
                    print("WIN in ", (i + 1), " moves")
                    f.write(f"Prioritize_Upper_Right;{first_direction};{repete};{score};{i + 1};Win;Heuristic\n")
                break

    for repete in range(30):
        # Prioritize upper left corner solver
        grid, score = new_game()
        first_direction = None
        for i in range(1000):
            if first_direction is None:
                first_direction = 'up'
            try:
                grid, score = prioritize_upper_left(grid, score)
            except RuntimeError as inst:
                if str(inst) == "GO":
                    print("GAME OVER in ", (i + 1), " moves")
                    f.write(f"Prioritize_Upper_Left;{first_direction};{repete};{score};{i + 1};Loose;Heuristic\n")
                elif str(inst) == "WIN":
                    print("WIN in ", (i + 1), " moves")
                    f.write(f"Prioritize_Upper_Left;{first_direction};{repete};{score};{i + 1};Win;Heuristic\n")
                break

    for repete in range(30):
        # Prioritize left upper corner solver
        grid, score = new_game()
        first_direction = None
        for i in range(1000):
            if first_direction is None:
                first_direction = 'up'
            try:
                grid, score = prioritize_left_upper(grid, score)
            except RuntimeError as inst:
                if str(inst) == "GO":
                    print("GAME OVER in ", (i + 1), " moves")
                    f.write(f"Prioritize_Left_Upper;{first_direction};{repete};{score};{i + 1};Loose;Heuristic\n")
                elif str(inst) == "WIN":
                    print("WIN in ", (i + 1), " moves")
                    f.write(f"Prioritize_Left_Upper;{first_direction};{repete};{score};{i + 1};Win;Heuristic\n")
                break

    for repete in range(30):
        # Prioritize lower left corner solver
        grid, score = new_game()
        first_direction = None
        for i in range(1000):
            if first_direction is None:
                first_direction = 'left'
            try:
                grid, score = prioritize_lower_left(grid, score)
            except RuntimeError as inst:
                if str(inst) == "GO":
                    print("GAME OVER in ", (i + 1), " moves")
                    f.write(f"Prioritize_Lower_Left;{first_direction};{repete};{score};{i + 1};Loose;Heuristic\n")
                elif str(inst) == "WIN":
                    print("WIN in ", (i + 1), " moves")
                    f.write(f"Prioritize_Lower_Left;{first_direction};{repete};{score};{i + 1};Win;Heuristic\n")
                break

    for repete in range(30):
        # Prioritize lower right corner solver
        grid, score = new_game()
        first_direction = None
        for i in range(1000):
            if first_direction is None:
                first_direction = 'right'
            try:
                grid, score = prioritize_lower_right(grid, score)
            except RuntimeError as inst:
                if str(inst) == "GO":
                    print("GAME OVER in ", (i + 1), " moves")
                    f.write(f"Prioritize_Lower_Right;{first_direction};{repete};{score};{i + 1};Loose;Heuristic\n")
                elif str(inst) == "WIN":
                    print("WIN in ", (i + 1), " moves")
                    f.write(f"Prioritize_Lower_Right;{first_direction};{repete};{score};{i + 1};Win;Heuristic\n")
                break

        #print_grid(grid, score)