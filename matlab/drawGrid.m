function drawGrid(occupancy_grid, dim, resolution, colour)
%DRAWGRID Draws a cube representation of the occupancy grid

[row, col, plane] = ind2sub(size(occupancy_grid), find(occupancy_grid == 1));
nPoints = numel(row);

for i = 1:nPoints
    cell = [row(i); col(i); plane(i)];
    pos = dim(:,1) + (cell-0.5) .* resolution;
    drawCube(pos, resolution, colour);
end

end

