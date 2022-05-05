import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# Statement: I added more detailed instructions in GitHub
# https://github.com/MrZoyo/Forest-Fire-Von-Neumann

neighbourhood_eight = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
neighbourhood_four = ((-1, 0), (0, -1), (0, 1), (1, 0))
EMPTY, TREE, FIRE = 0, 1, 2

# set up map size
# we leave boundary cells always empty, so we extend each side by 2
x, y = 101, 82
x += 2
y += 2
maxi_digits = len(str(x * y))

# set up iteration limit
iteration_limit = 200
iteration_digits = len(str(iteration_limit))
# set up interval between frames(ms).
interval = 200
# choose the neighbourhood
all_directions = False
# choose if need to save grids count
save_grids_count = True
# choose if need to save the animation
# please always set save_animation to True
save_animation = True
# Probability of new tree growth per empty cell, on fire itself and grow with alive neighbors.
p, f, q = 0.05, 0.00001, 0.8
r = 1.0
# Initialize the map with empty.
X = np.zeros((y, x))

step = 0


def iterate(X):
    # calculate new state of each cell
    X_next = np.zeros((y, x))
    global step
    empty_count = 0
    tree_count = 0
    fire_count = 0
    step += 1
    for ix in range(1, x - 1):
        for iy in range(1, y - 1):
            # If current cell is empty:
            if X[iy, ix] == EMPTY:
                # If it has a tree as a neighbour, grow a tree with probability q
                # If not, grow a tree with probability p
                X_next[iy, ix] = EMPTY
                empty_count += 1
                has_neighbour = False
                for dx, dy in neighbourhood:
                    if X[iy + dy, ix + dx] == TREE:
                        has_neighbour = True
                        break
                if has_neighbour:
                    if np.random.random() <= q:
                        X_next[iy, ix] = TREE
                        tree_count += 1
                        empty_count -= 1
                elif np.random.random() <= p:
                    X_next[iy, ix] = TREE
                    tree_count += 1
                    empty_count -= 1

            # If current cell is a tree:
            if X[iy, ix] == TREE:
                X_next[iy, ix] = TREE
                tree_count += 1
                # If it has a fire as a neighbour, burn it
                has_neighbour = False
                for dx, dy in neighbourhood:
                    if X[iy + dy, ix + dx] == FIRE:
                        has_neighbour = True
                        break

                if has_neighbour and np.random.random() <= r:
                    X_next[iy, ix] = FIRE
                    fire_count += 1
                    tree_count -= 1
                # If it has no fire as a neighbour, burn it with probability f
                elif np.random.random() <= f:
                    X_next[iy, ix] = FIRE
                    fire_count += 1
                    tree_count -= 1

            # If current cell is on fire:
            if X[iy, ix] == FIRE:
                # it burns out
                X_next[iy, ix] = EMPTY
                empty_count += 1

    # save the count of each type of cell in file
    if save_grids_count:
        with open("forest_fire_count.txt", "a") as file:
            if step == 1:
                file.write("Step\tEmpty\tTree\tFire\n")
                file.write(str(0).zfill(iteration_digits) + "\t" + str(x * y).zfill(maxi_digits) + "\t"
                           + str(0).zfill(maxi_digits) + "\t" + str(0).zfill(maxi_digits) + "\n")
            file.write(str(step).zfill(iteration_digits) + "\t" + str(empty_count).zfill(maxi_digits) + "\t"
                       + str(tree_count).zfill(maxi_digits) + "\t" + str(fire_count).zfill(maxi_digits) + "\n")

    return X_next


if all_directions:
    neighbourhood = neighbourhood_eight
else:
    neighbourhood = neighbourhood_four

# following code is for animation and imported from GitHub user "xnx". I modified it to fit my code.
# -------------
# Colours for visualization: brown for EMPTY, dark green for TREE and orange
# for FIRE. Note that for the colormap to work, this list and the bounds list
# must be one larger than the number of different values in the array.
colors_list = ['#42280E', '#008000', 'blue', '#FF4500']
cmap = colors.ListedColormap(colors_list)
bounds = [0, 1, 2, 3]
norm = colors.BoundaryNorm(bounds, cmap.N)
# -------------

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)


def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)


# Bind our grid to the identifier X in the animate function's namespace.
animate.X = X
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=iteration_limit, repeat=False)

if save_animation:
    anim.save("forest-fire.gif")

plt.show()
