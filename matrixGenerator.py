from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def matrix_generator(image_path):
    img = Image.open(image_path).convert('L')
    matrix = np.array(img)
    matrix = ((matrix / 255) + 1).astype(int)
    
    # Calculate the starting position for the original image
    start_row = (500 - matrix.shape[0]) // 2
    start_col = (500 - matrix.shape[1]) // 2
    
    # Resize the matrix to 500 x 500 and place the original image in the center
    resized_matrix = np.zeros((500, 500), dtype=int)
    resized_matrix[start_row:start_row+matrix.shape[0], start_col:start_col+matrix.shape[1]] = matrix
    
    # Fill any excess pixels with value 2
    resized_matrix[:start_row, :] = 2
    resized_matrix[start_row+matrix.shape[0]:, :] = 2
    resized_matrix[:, :start_col] = 2
    resized_matrix[:, start_col+matrix.shape[1]:] = 2
    
    return resized_matrix


def plot_matrix(matrix):
        plt.imshow(matrix, cmap='gray')
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    # Example usage:
    image_path = 'sample.png'
    matrix = matrix_generator(image_path)
    plot_matrix(matrix)
