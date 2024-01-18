from matplotlib import colors
from DLA_module import Matrix, WhiteWalker, BlackWalker, make_gif
from tqdm import tqdm
from matrixGenerator import matrix_generator

# set of inputs
length_x = 500  # length x of matrix
length_y = 500  # length y of matrix
maxCount = 5000  # maximum number of particles to add
cmap = colors.ListedColormap(['black', 'black', 'white'])  # color palette for number 0,1 and 2 in matrix

# Initialize parameter
total_added = 0

completeCluster = False
matrix = Matrix(length_x, length_y)
matrix.value = matrix_generator('sample.png')
#matrix.plot(cmap)

matrix.max_y = 5
white_walker = WhiteWalker()
black_walker = BlackWalker()

pbar = tqdm(total=maxCount)

while not completeCluster:

    if total_added > 1201:
        # spawn a white walker randomly at the circle edge
        white_walker.random_at_white(matrix)
        white_walker.foundFriend = False

        # make random walk until it finds a friend
        while white_walker.foundFriend is False:
            # print(f'white walker at {walker.x},{walker.y} is walking')
            white_walker.check_around(matrix)
            if white_walker.foundFriend is False:
                white_walker.random_walk(matrix)

        white_walker.addedCount += 1
        pbar.update(1)

    # spawn a black walker at the center
    if matrix.value[250, 250] == 1:
        black_walker.y = int(length_y / 2)
        black_walker.x = int(length_x / 2)
    else:
        black_walker.random_at_black(matrix)
    
    black_walker.foundEnemy = False

    while black_walker.foundEnemy is False:
        black_walker.check_around(matrix)
        if black_walker.foundEnemy is False:
            black_walker.random_walk(matrix)

    black_walker.addedCount += 1
    pbar.update(1)

    total_added = white_walker.addedCount + black_walker.addedCount

    matrix.save_image(total_added, cmap=cmap, interval_print =100)


    # check if the cluster is complete
    if total_added >= maxCount:
        completeCluster = True
        print('cluster is complete')



pbar.close()

print(f'cluster 100% complete at {total_added} particles')