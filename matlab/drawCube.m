function drawCube(center, dimensions, colour)
% DRAWCUBE  Draws around center with given dimensions.
%   drawCube(center, dimensions).
%   center should be in [x, y, z] format.
%   dimensions should be in [dx, dy, dz] format.

x = center(1);
y = center(2);
z = center(3);

dx = dimensions(1);
dy = dimensions(2);
dz = dimensions(3);

verts = [
    x - dx/2, y - dy/2, z - dz/2;...
    x + dx/2, y - dy/2, z - dz/2;...
    x - dx/2, y + dy/2, z - dz/2;...
    x + dx/2, y + dy/2, z - dz/2;...
    x - dx/2, y - dy/2, z + dz/2;...
    x + dx/2, y - dy/2, z + dz/2;...
    x - dx/2, y + dy/2, z + dz/2;...
    x + dx/2, y + dy/2, z + dz/2;...
    ];

faces = [
    1 2 4 3;...
    5 6 8 7;...
    1 5 7 3;...
    2 6 8 4;...
    1 5 6 2;...
    3 7 8 4;
    ];

patch('Faces',faces,'Vertices',verts,'FaceColor',colour);