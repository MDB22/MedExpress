function data = getLidarData(socket, dims)
%GETLIDARDATA Reads LiDAR data passed from the Raspberry Pi via TCP/IP

% First piece of data is number of points
%n = fscanf(socket,'%u', 1);

% Generate data matrix
%data = zeros(3, n);
data = zeros(3, 1);

for i=1:1
    s = scanstr(socket);
    d = sscanf(s{1},'[ %f %f %f]');
    
    if (inRange(d, dims))
        data(:,i) = d;
    end
end