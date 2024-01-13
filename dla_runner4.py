import numpy as np
from matplotlib import colors
from DLA_module import Matrix, WhiteWalker, BlackWalker
from tqdm import tqdm

# set of inputs
length_x = 500  # length x of matrix
length_y = 500  # length y of matrix
maxCount = 5000  # maximum number of particles to add
cmap = colors.ListedColormap(['navy', 'black', 'white'])  # color palette for number 0,1 and 2 in matrix

# Initialize parameter
randomWalkersCount = 0
completeCluster = False
matrix = Matrix(length_x, length_y)
# matrix.plot(cmap)

# Create a circular mask
center_x = length_x / 2
center_y = length_y / 2
radius = 100
y, x = np.ogrid[:length_y, :length_x]
mask = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2

# Set the circular region as the seed
matrix.value[mask] = 1

matrix.plot(cmap)

matrix.max_y = 5
white_walker = WhiteWalker()
black_walker = BlackWalker()

pbar = tqdm(total=maxCount / 2)

while not completeCluster:
    # spawn a white walker randomly at the circle edge
    white_walker.random_at_white(matrix)
    white_walker.foundFriend = False

    # make random walk until it finds a friend
    while white_walker.foundFriend is False:
        # print(f'white walker at {walker.x},{walker.y} is walking')
        white_walker.check_around(matrix)
        if white_walker.foundFriend is False:
            white_walker.random_walk(matrix)
    # matrix.plot(cmap)
    white_walker.addedCount += 1

    # spawn a black walker at the center
    black_walker.random_at_black(matrix)
    black_walker.foundEnemy = False

    while black_walker.foundEnemy is False:
        # print(f'black walker at {walker.x},{walker.y} is walking')
        black_walker.check_around(matrix)
        if black_walker.foundEnemy is False:
            black_walker.random_walk(matrix)

    # matrix.plot(cmap)
    black_walker.addedCount += 1

    # check if the cluster is complete
    if white_walker.addedCount + black_walker.addedCount >= maxCount:
        completeCluster = True
        print('cluster is complete')
        break

    pbar.update(1)
    # print(f'cluster {int((white_walker.addedCount + black_walker.addedCount)/maxcount*100)}% complete at
    # {white_walker.addedCount + black_walker.addedCount} particles')

    # matrix.print_info(white_walker,100,cmap)

pbar.close()

print(f'cluster 100% complete at {white_walker.addedCount} particles')
matrix.plot(cmap)
