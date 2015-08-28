function cell = posToCell(pos, dims, resolution)
%FILLCELL Converts from world position to grid cell position

cell = zeros(size(pos));

for i = 1:size(pos,2)
    cell(:,i) = floor((pos(:,i) - dims(:,1))./resolution + ones(3,1));
end

end

