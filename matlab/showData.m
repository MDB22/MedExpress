function showData(file)

    data = csvread(file);
    
    num_elements = size(data, 1);
    
    new_data = [];

    for i=1:num_elements
        % Only keep realistic data
        if(norm(data(i,:)) < 500)
            new_data = [new_data;data(i,:)];
        end
    end
    
    disp(size(new_data,1));
    
    figure;
    showPointCloud(new_data);
    xlabel('X');
    ylabel('Y');
    zlabel('Z');
    
    
return