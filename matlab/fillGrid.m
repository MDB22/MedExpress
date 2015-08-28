function grid = fillGrid(grid, cells)
%FILLGRID Populates the occupancy grid with new data

for i = 1:size(cells, 2)
    grid(cells(1,i), cells(2,i), cells(3,i)) = 1;
end

end