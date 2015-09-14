close all;
clc;

socket = tcpip('192.168.0.139', 50010, 'NetworkRole', 'client',...
    'Timeout', 5, 'Terminator', ']');
fopen(socket);

% World dimensions (cm)
xdim = [0 500];
ydim = [-500 500];
zdim = [-100 500];
world_dim = [xdim; ydim; zdim];

setupFigure(world_dim, 'on');

% Discretization resolution (cm) in x, y, z, respectively
voxelize_resolution = [10; 10; 10];

% Count the number of points/cubes in the grid
n = (world_dim(:,2) - world_dim(:,1))./voxelize_resolution;

% Initialize occupancy grid
% 0 - Empty cell
% 1 - Occupied cell
occupancy_grid = zeros(n');

% Generate cube for UAV
uav_pos = [0; 0; 0];
uav_dim = [80; 250; 30];

% Draw UAV
drawCube(uav_pos, uav_dim, 'b');

%material dull;
alpha('color');
%alphamap('rampdown');
view(30,30);

count = 0;

% Repeat until count, and update grid/figure
while (count < 1)
    % Update our position data
    %new_data = getRandomData();
    %new_data = getLidarDataFromFile('data.csv', world_dim);
    new_data = getLidarData(socket);
    
    % Convert from coordinates to cells
    cells = posToCell(new_data, world_dim, voxelize_resolution);
    
    % Fill occupancy grid
    occupancy_grid = fillGrid(occupancy_grid, cells);

    % Render the occupancy grid
    updateGrid(cells, world_dim, voxelize_resolution);
    
    % Save figure to jpeg
    hgexport(gcf, ['Figures/voxelize',num2str(count),'.png'], hgexport('factorystyle'), 'Format', 'jpeg');
    
    count = count + 1;
end

fclose(socket);