import random
import matplotlib.pyplot as plt
import numpy
import numpy as np


class Matrix:

	def __init__(self, length_x, length_y):
		self.value = numpy.zeros((length_x, length_y))
		self.value[5:length_x - 5, 5:length_y - 5] = 2
		self.max_y = 5
		self.length_x = length_x
		self.length_y = length_y

	def plot(self, cmap):
		plt.matshow(self.value, interpolation='nearest', cmap=cmap, origin='lower')
		plt.show()

	def save_image(self, walker, interval_print, cmap):
		interval = range(2, 10000000, interval_print)
		if walker.addedCount in interval:
			print(f'total cluster added = {walker.addedCount}')
			label = str(walker.addedCount)
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
		self.nearEdgeUp = False
		self.nearEdgeDown = False
		self.nearEdgeRight = False
		self.nearEdgeLeft = False
		self.addedCount = 0
		self.x = 0
		self.y = 0

	def random_at_white(self, matrix):
		indices = np.where(matrix.value == 2)
		indices = list(zip(indices[0], indices[1]))  # convert indices to list of tuples
		random_index = random.choice(indices)
		self.x = random_index[0]
		self.y = random_index[1]

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
		self.nearEdgeUp = False
		if matrix.value[self.y + 1, self.x] == 1:
			self.foundFriend = True
			self.make_friend(matrix)
		if matrix.value[self.y + 1, self.x] == 0:
			self.nearEdgeUp = True

		# check down
		if matrix.value[self.y - 1, self.x] == 1:
			self.foundFriend = True
			self.make_friend(matrix)
		if matrix.value[self.y - 1, self.x] == 0:
			self.nearEdgeDown = True

		# check right
		self.nearEdgeRight = False
		if matrix.value[self.y, self.x + 1] == 1:
			self.foundFriend = True
			self.make_friend(matrix)
		if matrix.value[self.y, self.x + 1] == 0:
			self.nearEdgeRight = True

		# check left
		self.nearEdgeLeft = False
		if matrix.value[self.y, self.x - 1] == 1:
			self.foundFriend = True
			self.make_friend(matrix)
		if matrix.value[self.y, self.x - 1] == 0:
			self.nearEdgeLeft = True

	def random_walk(self, matrix):
		decide = random.random()

		# walk to the left
		if decide < 0.25:
			if self.nearEdgeLeft is True:
				self.random_walk(matrix)
			else:
				self.x = self.x - 1

		# walk to the right
		elif decide < 0.5:
			if self.nearEdgeRight is True:
				self.random_walk(matrix)
			else:
				self.x = self.x + 1

		# walk up
		elif decide < 0.75:
			if self.nearEdgeUp is True:
				self.random_walk(matrix)
			else:
				self.y = self.y + 1

		# walk down
		else:
			if self.nearEdgeDown is True:
				self.random_walk(matrix)
			else:
				self.y = self.y - 1

		self.nearEdgeDown = False
		self.nearEdgeUp = False
		self.nearEdgeRight = False
		self.nearEdgeLeft = False


class BlackWalker:

	def __init__(self):
		# initialize attributes
		self.foundEnemy = False  # not near white
		self.nearEdgeUp = False
		self.nearEdgeDown = False
		self.nearEdgeRight = False
		self.nearEdgeLeft = False
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
		if matrix.value[self.y + 1, self.x] == 2:
			self.foundEnemy = True
			self.make_enemy(matrix)
		if matrix.value[self.y + 1, self.x] == 0:
			self.nearEdgeUp = True

		# check down
		if matrix.value[self.y - 1, self.x] == 2:
			self.foundEnemy = True
			self.make_enemy(matrix)
		if matrix.value[self.y - 1, self.x] == 0:
			self.nearEdgeDown = True

		# check right
		self.nearEdgeRight = False
		if matrix.value[self.y, self.x + 1] == 2:
			self.foundEnemy = True
			self.make_enemy(matrix)
		if matrix.value[self.y, self.x + 1] == 0:
			self.nearEdgeRight = True

		# check left
		self.nearEdgeLeft = False
		if matrix.value[self.y, self.x - 1] == 2:
			self.foundEnemy = True
			self.make_enemy(matrix)
		if matrix.value[self.y, self.x - 1] == 0:
			self.nearEdgeLeft = True

	def random_walk(self, matrix):
		decide = random.random()

		# walk to the left
		if decide < 0.25:
			if self.nearEdgeLeft is True:
				self.random_walk(matrix)
			else:
				self.x = self.x - 1

		# walk to the right
		elif decide < 0.5:
			if self.nearEdgeRight is True:
				self.random_walk(matrix)
			else:
				self.x = self.x + 1

		# walk up
		elif decide < 0.75:
			if self.nearEdgeUp is True:
				self.random_walk(matrix)
			else:
				self.y = self.y + 1

		# walk down
		else:
			if self.nearEdgeDown is True:
				self.random_walk(matrix)
			else:
				self.y = self.y - 1

		self.nearEdgeDown = False
		self.nearEdgeUp = False
		self.nearEdgeRight = False
		self.nearEdgeLeft = False
