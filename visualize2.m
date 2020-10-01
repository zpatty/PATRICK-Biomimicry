clear
for j = 1:3
    string = ['centroids_altb' num2str(j) '.mat'];
    load(string)
    fps = 60;
    
    shape = size(centroids);
    nPoints = shape(2);
    nFrames = shape(1);
    %%
    centroids(:,1,1) = centroids(:,1,1) - centroids(1,1,1);
    centroids = centroids*76/100;
    centroids(:,1,2) = centroids(:,1,2) - centroids(1,1,2);
    range = 1:nFrames;
    smooth = 10; % 1/3 second blur
    for i=1:nPoints
        pAx = subplot(1,2,i);
        x = centroids(range,i,1);
        y = centroids(range,i,2);
        plot(movmean(x,smooth),movmean(y,smooth));
        set(pAx, 'Ydir', 'reverse')
        pbaspect(pAx,[1 1 1])
        daspect(pAx, [1 1 1])
    end
    
    speed_x(j) = (centroids(end,1,1)-centroids(1,1,1))/nFrames*fps;
    speed_y(j) = (centroids(end,1,2)-centroids(1,1,2))/nFrames*fps;
end
disp(mean(speed_x));
disp(mean(speed_y));
disp(std(speed_x));


