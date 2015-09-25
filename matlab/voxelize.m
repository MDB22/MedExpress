close all;
clc;

socket = tcpip('192.168.1.100', 50010, 'NetworkRole', 'client',...
    'Timeout', 5, 'Terminator', ']');
fopen(socket);

% World dimensions (cm)
xdim = [-50 500];
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

% Timers
t1 = clock;
t2 = clock;

count = 0;

% Repeat for given amount of time
while (etime(t2, t1) < 60)
    try
        % Update our position data
        %new_data = getRandomData();
        %new_data = getLidarDataFromFile('data.csv', world_dim);
        new_data = getLidarData(socket, world_dim);

        % Convert from coordinates to cells
        cells = posToCell(new_data, world_dim, voxelize_resolution);

        % Fill occupancy grid
        occupancy_grid = fillGrid(occupancy_grid, cells);

        % Render the occupancy grid
        updateGrid(cells, world_dim, voxelize_resolution);

        count = count + 1;

        drawnow;        
            
    catch
        disp('Out of data, waiting for more');
        pause(3);
    end
    
    t2 = clock;
end
    
% Save figure to jpeg
hgexport(gcf, ['Figures/voxelize',num2str(count),'.png'], hgexport('factorystyle'), 'Format', 'jpeg');

fclose(socket);