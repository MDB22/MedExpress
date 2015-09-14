function data = getLidarData(socket)
%GETLIDARDATA Reads LiDAR data passed from the Raspberry Pi via TCP/IP

% First piece of data is number of points
n = fscanf(socket,'%u', 1)

% Generate data matrix
data = zeros(n, 3);

for i=1:n
    s = scanstr(socket);
    data(i,:) = sscanf(s{1},'[ %f %f %f]');
    i
end

data