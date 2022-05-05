# Forest-Fire-Von-Neumann
Forest fire models that support von Neumann neighbors or all 8 neighbors.

The map starts with all **empty**.

You can set the following parameters：

- **x,y:int** map size
- **all_direction:bool** switch between von Neumann neighbors (4) and omnidirectional neighbors (8)
- **save_animation:bool** choose if need to save animation(in gif format)
- **interval:int** set the interval between two frames(in ms)
- **iteration_limit:int** number of iterations to simulate
- **save_grids_count:bool** choose if need to save the count of every state and output to a file
- **p:float** probability of a tree growing in an empty grid
- **f:float** probability that a tree will naturally catch fire
- **q:float** probability of a blank lattice growing a tree when its neighbor has a tree
- **r:float** probability of a tree catching fire when a neighbor catches fire


##### Copyright notice: I used part of this project for **animation generation**.
https://github.com/scipython/scipython-maths
