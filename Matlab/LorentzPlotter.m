%% Lorentz live plotter
% raymas
% first order : euler forward method

close all
clearvars
clc

% time values
numberOfStep = 10000;
delta = 0.01;

initalValues = [1, 1, 1];

lastValues = initalValues;
path = nan * zeros(numberOfStep, 3); path(1,:) = initalValues;
stepValues = ones(1, numberOfStep);


%% Lorentz system
% dx = x + delta * r * (y - x);
% dy = y + delta * (x * (rho - z) - y);
% dz = z + delta * (x * y - beta * z);
Lorentz = @(r, rho, beta, x, y, z, delta) [x + delta * r * (y - x), y + delta * (x * (rho - z) - y), z + delta * (x * y - beta * z)];

%% Figure

% Full figure
figure3D = figure;
plot3D = plot3(nan, nan, nan, 'r', nan, nan, nan, 'b');
view(74, 16);
grid minor;
xlabel('x axis');
ylabel('y axis');
zlabel('z axis');

% Single axis plot
figureAxis = figure;
subplot(3,1,1)
plotAxisX = plot(nan, nan);
grid minor;
xlabel('Step');
ylabel('X value');

subplot(3,1,2)
plotAxisY = plot(nan, nan);
grid minor;
xlabel('Step');
ylabel('Y value');

subplot(3,1,3)
plotAxisZ = plot(nan, nan);
grid minor;
xlabel('Step');
ylabel('Z value');


counter = 2;
while counter < numberOfStep+1
    lastValues = Lorentz(20, 18, 8/3, lastValues(1), lastValues(2), lastValues(3), delta);
    path(counter,:) = lastValues;
    stepValues(counter) = counter;
    counter = counter + 1;
    % 3D update
    set(plot3D, 'XData', path(:,1)); set(plot3D, 'YData', path(:,2)); set(plot3D, 'ZData', path(:,3));
    % 1D update
    set(plotAxisX, 'XData', stepValues); set(plotAxisY, 'XData', stepValues); set(plotAxisZ, 'XData', stepValues);
    set(plotAxisX, 'YData', path(:,1)); set(plotAxisY, 'YData', path(:,2)); set(plotAxisZ, 'YData', path(:,3));
    % update the view
    % view(x, y, z);
    pause(0.01);
end
