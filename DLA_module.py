import random
import matplotlib.pyplot as plt
import numpy as np
import os
import imageio.v2 as imageio


def make_gif():
    print("Making gif...")
    images = []
    filenames = os.listdir("images")
    # Sort filenames numerically
    filenames.sort(key=lambda filename: int(filename.replace("cluster", "").replace(".png", "")))
    for filename in filenames:
        images.append(imageio.imread("images/" + filename))
    imageio.mimsave('movie.gif', images, duration=0.3)
    print("Done!")


class Matrix:

	def __init__(self, length_x, length_y):
		self.value = np.zeros((length_x, length_y))
		self.value[0:length_x, 0:length_y] = 2
		self.max_y = 5
		self.length_x = length_x
		self.length_y = length_y

		# Check for the existence of the "images" directory when the Matrix is created
		if not os.path.exists("images"):
			os.makedirs("images")

	def plot(self, cmap):
		plt.matshow(self.value, interpolation='nearest', cmap=cmap, origin='lower')
		plt.show()

	def save_image(self, total_added, interval_print, cmap):
		interval = range(2, 10000000, interval_print)
		if total_added in interval:
			label = str(total_added).zfill(5)
			plt.title("DLA Cluster", fontsize=20)
			plt.matshow(self.value, interpolation='nearest', cmap=cmap, origin='lower')  # plt.cm.Blues) #ocean, Paired
			plt.xlabel("direction, $x$", fontsize=15)
			plt.ylabel("direction, $y$", fontsize=15)
			plt.savefig("images/cluster{}.png".format(label), dpi=200)
			plt.close()


class WhiteWalker:

	def __init__(self):
		# initialize attributes
		self.y = 0
		self.foundFriend = False
		self.addedCount = 0
		self.x = 0
		self.y = 0

	def random_at_white(self, matrix):
		indices = np.where(matrix.value == 2)
		random_index = np.random.randint(len(indices[0]))
		self.x = indices[0][random_index]
		self.y = indices[1][random_index]

	def random_at_circle_edge(self, radius, length_x, length_y):
		# Generate a random angle
		angle = np.random.uniform(0, 2 * np.pi)

		# Calculate the coordinates on the edge of circle
		self.x = int((radius * np.cos(angle)) + length_x / 2)
		self.y = int((radius * np.sin(angle)) + length_y / 2)

	def random_at_top(self, matrix, length_x, length_y):
		# self.location = [random.randint(5, length_x-5), length_y-6]
		self.x = random.randint(5, length_x - 5)
		if matrix.max_y + 10 < length_y - 6:
			self.y = matrix.max_y + 10
		else:
			self.y = length_y - 6

	def randomisation(self, length_x, length_y):
		self.x = random.randint(5, length_x - 5)
		self.y = random.randint(5, length_y - 5)

	def make_friend(self, matrix):
		radius = 3
		y_range, x_range = np.ogrid[-radius:radius + 1, -radius:radius + 1]
		mask = x_range ** 2 + y_range ** 2 <= radius ** 2
		matrix.value[self.y - radius:self.y + radius + 1, self.x - radius:self.x + radius + 1][mask] = 1

	def check_around(self, matrix):
		# check up
		if self.y + 2 < matrix.length_y:
			if matrix.value[self.y + 1, self.x] == 1:
				self.foundFriend = True
				self.make_friend(matrix)

		# check down
		if self.y - 1 > 0:
			if matrix.value[self.y - 1, self.x] == 1:
				self.foundFriend = True
				self.make_friend(matrix)

		# check right
		if self.x + 2 < matrix.length_x:
			if matrix.value[self.y, self.x + 1] == 1:
				self.foundFriend = True
				self.make_friend(matrix)

		# check left
		if self.x - 1 > 0:
			if matrix.value[self.y, self.x - 1] == 1:
				self.foundFriend = True
				self.make_friend(matrix)

	def random_walk(self, matrix):
		decide = random.random()

		# walk to the left
		if decide < 0.25:
			if self.x - 1 < 0:
				self.random_walk(matrix)
			else:
				self.x = self.x - 1

		# walk to the right
		elif decide < 0.5:
			if self.x + 2 > matrix.length_x:
				self.random_walk(matrix)
			else:
				self.x = self.x + 1

		# walk up
		elif decide < 0.75:
			if self.y + 2 > matrix.length_y:
				self.random_walk(matrix)
			else:
				self.y = self.y + 1

		# walk down
		else:
			if self.y - 1 < 0:
				self.random_walk(matrix)
			else:
				self.y = self.y - 1


class BlackWalker:

	def __init__(self):
		# initialize attributes
		self.foundEnemy = False  # not near white
		self.x = 0
		self.y = 0
		self.addedCount = 0

	def random_at_black(self, matrix):
		indices = np.where(matrix.value == 1)
		indices = list(zip(indices[0], indices[1]))  # convert indices to list of tuples
		random_index = random.choice(indices)
		self.x = random_index[0]
		self.y = random_index[1]

	def random_at_circle_edge(self, radius, length_x, length_y):
		angle = np.random.uniform(0, 2 * np.pi)

		# Calculate the coordinates on the edge or circle
		self.x = int(radius * np.cos(angle)) + length_x / 2
		self.y = int(radius * np.sin(angle)) + length_y / 2

	def random_at_top(self, matrix, length_x, length_y):
		# self.location = [random.randint(5, length_x-5), length_y-6]
		self.x = random.randint(5, length_x - 5)
		if matrix.max_y + 10 < length_y - 6:
			self.y = matrix.max_y + 10
		else:
			self.y = length_y - 6

	def random_at_boundary(self, length_x, length_y):
		"""
		This function generates a random number at the boundary of the matrix
		"""
		self.x = random.randint(5, length_x - 5)
		self.y = random.randint(5, length_y - 5)

	def make_enemy(self, matrix):
		radius = 3
		y_range, x_range = np.ogrid[-radius:radius + 1, -radius:radius + 1]
		mask = x_range ** 2 + y_range ** 2 <= radius ** 2
		matrix.value[self.y - radius:self.y + radius + 1, self.x - radius:self.x + radius + 1][mask] = 2

	def check_around(self, matrix):
		# check up
		if self.y + 1 < matrix.length_y:
			if matrix.value[self.y + 1, self.x] == 2:
				self.foundEnemy = True
				self.make_enemy(matrix)

		# check down
		if self.y - 1 > 0:
			if matrix.value[self.y - 1, self.x] == 2:
				self.foundEnemy = True
				self.make_enemy(matrix)

		# check right
		if self.x + 1 < matrix.length_x:
			if matrix.value[self.y, self.x + 1] == 2:
				self.foundEnemy = True
				self.make_enemy(matrix)

		# check left
		if self.x - 1 > 0:
			if matrix.value[self.y, self.x - 1] == 2:
				self.foundEnemy = True
				self.make_enemy(matrix)

	def random_walk(self, matrix):
		decide = random.random()

		# walk to the left
		if decide < 0.25:
			if self.x - 1 < 0:
				self.random_walk(matrix)
			else:
				self.x = self.x - 1

		# walk to the right
		elif decide < 0.5:
			if self.x + 1 > matrix.length_x:
				self.random_walk(matrix)
			else:
				self.x = self.x + 1

		# walk up
		elif decide < 0.75:
			if self.y + 1 > matrix.length_y:
				self.random_walk(matrix)
			else:
				self.y = self.y + 1

		# walk down
		else:
			if self.y - 1 < 0:
				self.random_walk(matrix)
			else:
				self.y = self.y - 1

if __name__ == '__main__':
	make_gif()