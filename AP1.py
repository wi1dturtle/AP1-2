import random

import numpy as np
import matplotlib.pyplot as plt

# create random 4-vectors

vector1 = [random.uniform(0.0, 100.0) for _ in range(4)]
vector2 = [random.uniform(0.0, 100.0) for _ in range(4)]

# create 2x2 matrixes with 0s in it
matrix1 = [[0 for _ in range(2)] for _ in range(2)]
matrix2 = [[0 for _ in range(2)] for _ in range(2)]

# fill matrixes with our random  vectors
for a in range(4):
    i=int(a/2)
    j=int(a%2)
    matrix1[i][j]=vector1[a]
    matrix2[i][j]=vector2[a]

print(f"first random 4-vector {vector1}")
print(f"second random 4-vector {vector2}")
print(f"first random 2x2-matrix {matrix1}")
print(f"second random 2x2-matrix {matrix2}")

# function of vector norm 1 which is absolute sum of its values
def vector_norm_1(x):
    norm=0
    for i in range(len(x)):
        norm+=abs(x[i])
    return norm

# function of matrix norm 1 which is maximum of absolute column sum
def matrix_norm_1(x):
    norm=0
    for j in range(len(x[0])):
        cur=0
        for i in range(len(x)):
            cur+=abs(x[i][j])
        norm=(max(cur,norm))
    return norm

# function of vector norm infinity which is maximum of its absolute values
def vector_norm_inf(x):
    norm=0
    for i in range(len(x)):
        norm=max(norm,abs(x[i]))
    return norm

# function of matrix norm infinity which is maximum of absolute row sum
def matrix_norm_inf(x):
    norm=0
    for i in range(len(x)):
        cur=0
        for j in range(len(x[i])):
            cur+=abs(x[i][j])
        norm=(max(cur,norm))
    return norm

def vector_distance(x1,x2,funct):
    vect = [0.0 for _ in range(4)]
    for i in range(len(x1)):
        vect[i]=x2[i]-x1[i]
    return funct(vect)

def matrix_distance(x1,x2,funct):
    mat = [[0 for _ in range(2)] for _ in range(2)]
    for i in range(len(x1)):
        for j in range(len(x1[i])):
            mat[i][j]=x1[i][j]-x2[i][j]
    return funct(mat)


print(f"distance between vectors with 1-norm {vector_distance(vector1,vector2,vector_norm_1)}")

print(f"distance between vectors with inf-norm {vector_distance(vector1,vector2,vector_norm_inf)}")

print(f"distance between matrices with 1-norm {matrix_distance(matrix1,matrix2,matrix_norm_1)}")

print(f"distance between matrices with inf-norm {matrix_distance(matrix1,matrix2,matrix_norm_inf)}")


def draw_ball(norm_fun):
    points = np.random.uniform(-1.5, 1.5, (500000, 4))

    inside = np.array([pt for pt in points if vector_distance(pt,[0,0,0,0],norm_fun) <= 1])

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(projection='3d')
    ax.scatter(inside[:, 0], inside[:, 1], inside[:, 2], s=1, alpha=0.2)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_title("Unit Ball with given norm")
    plt.show()

draw_ball(vector_norm_1)