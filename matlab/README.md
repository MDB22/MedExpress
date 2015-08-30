# MATLAB Code
Code for quick testing of algorithms before porting to Python.

## Point Cloud visualisation
Converts a CSV data file of points to a point cloud visual representation.
* Place a CSV file containing the **N x 3** matrix of data from the LiDAR in the MATLAB folder
* Run the *showData(file)* function where *file* is the name of (or path to) the CSV file

## Voxelize
Convers a CSV data file of points to a voxel grid visual representation.
* Place a CSV file containing the **N x 3** matrix of data from the LiDAR in the MATLAB folder
* Run the *voxelize* script to generate visualization
* The script can use randomly generated data with *getRandomData()*, or can use data obtained from the LiDAR with *getLidarData(file)* where *file* is the name of (or path to) the CSV file
