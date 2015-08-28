function bool = inRange(data, dims)
%INRANGE Summary of this function goes here
%   Detailed explanation goes here

if (data(1) > dims(1,1) && data(1) < dims(1,2) &&...
    data(2) > dims(2,1) && data(2) < dims(2,2) &&...
    data(3) > dims(3,1) && data(3) < dims(3,2))
    bool = 1;
else
    bool = 0;
end

end

