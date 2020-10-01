clear
load('centroids_sync.mat')
%centroids = centroids(4*60:12*60,:,:);
shape = size(centroids);
nPoints = shape(2);
nFrames = shape(1);
%%
centroids(:,1,1) = centroids(:,1,1) - centroids(1,1,1);
centroids = centroids*6/9;
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

speed_x = (centroids(end,1,1)-centroids(1,1,1))/nFrames*60;
disp(speed_x)
speed_y = (centroids(end,1,2)-centroids(1,1,2))/nFrames*60;
disp(speed_y)

upper = (9.5)*60;
lower = (9)*60;
speed_x = (centroids(upper,2,1)-centroids(lower,2,1))/(upper-lower)*60;
disp(speed_x)
speed_y = (centroids(upper,2,2)-centroids(lower,2,2))/(upper-lower)*60;
disp(speed_y)

for i = 2:length(centroids(lower:upper,2,1:2))
    vx(i) = (centroids(i,2,1) - centroids(i-1,2,1))*60;
    vy(i) = (centroids(i,2,2) - centroids(i-1,2,2))*60;
    v(i) = sqrt(vx(i)^2+vy(i)^2);
    F(i) = v(i)^2*1000/2*.075*.01;
    if abs(vy(i))>0
        F(i) = F(i)*sign(vy(i));
    end
end

t = linspace(0,length(centroids(lower:upper,2,1:2)),length(F))/60;
a = F/0.15*2/10;

x = tf(1,[1 0 0]);
figure
lsim(x,a,t)



