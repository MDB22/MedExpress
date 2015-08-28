function new_data = getLidarData(file, dims)
%GETLIDARDATA Summary of this function goes here
%   Detailed explanation goes here

    data = csvread(file)';

    num_elements = size(data,2);
    
    new_data = [];

    for i=1:num_elements
        % Only keep realistic data
        if(inRange(data(:,i), dims))
            new_data = [new_data data(:,i)];
        end
    end

end