function updateGrid(cells, dim, resolution)
%UPDATEGRID Takes only new data points, and renders voxels to those
%positions


for i = 1:size(cells,2)
    pos = dim(:,1) + (cells(:,i)-0.5) .* resolution;
    hue = (pos(3) - dim(3,1))/(dim(3,2) - dim(3,1));
    drawCube(pos, resolution, hsv2rgb([hue 0.8 0.8]));
end

end

