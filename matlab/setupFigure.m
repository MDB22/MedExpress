function setupFigure(world_dim, drawAxes)
%SETUPFIGURE Summary of this function goes here
%   Detailed explanation goes here

figure('Name', 'Voxelized Point Cloud', 'NumberTitle', 'off');
hold on;
grid on;
xlabel('X');
ylabel('Y');
zlabel('Z');
title('Real-time LiDAR Data');

if strcmp(drawAxes, 'on')   
    quiver3(0, 0, 0, 100, 0, 0, 'color', 'r');
    text(100, 0, 0, 'N');
    quiver3(0, 0, 0, 0, -100, 0, 'color', 'b');
    text(0, -100, 0, 'E');
    quiver3(0, 0, 0, 0, 0, -100, 'color', 'g');
    text(0, 0, -100, 'D');
end

xlim(world_dim(1, :));
ylim(world_dim(2, :));
zlim(world_dim(3, :));

end