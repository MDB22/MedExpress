function data = getLidarData()
%GETLIDARDATA Summary of this function goes here
%   Detailed explanation goes here

% Randomly select the number of data points to generate
nDataPoints = randi([1 10], 1);

data = zeros(3,nDataPoints);

for i = 1:nDataPoints
    % Generate random data
    data(:,i) = -500 + 1000 * rand(3,1);    
end

end

