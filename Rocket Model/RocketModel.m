%% RocketModel

% November 2020
% Created by Nick Crnkovich

% Model using formulas and documentation from OpenRocket to generate our
% own simulation of the rocket apogee and position, velocity, acceleration
% data to be used for controller and ACS design


%% Initialize rocket conditions
u = 10; % [mph] windspeed
theta = 5; % [deg] launch angle
dt = 0.01;

weightR = 100; % [lbf] 
lengthR = 134/12; % [ft] length of rocket
diamR = 6.17/12; % [ft] outer diameter of rocket


% World Coord i, j, k
% i is into the wind and direction the launch rail is canted
% k is vertical
ihat = [1; 0; 0]; j = [0; 1; 0]; k = [0; 0; 1];

% Rocket coord Ri, Rj, Rk
% +Ri points from nose cone down rocket body
% +Rj aligns with i-k plane
Ri = -sind(theta)*ihat - cosd(theta)*k;
Rj = cosd(theta)*ihat - sind(theta)*k;
Rk = -j;

% Initial conditions
RocketVel = 0*Ri + 0*Rj + 0*Rk; % initial velocity
RocketPos = [lengthR*sind(theta); 0; lengthR*cosd(theta)];

% Compute local wind velocity and atmospheric conditions
rho_air = 0.002378; % [slugs/ft^3] density of air
c_air = 1120; % [ft/s] speed of sound at 70 deg F
T = 68; % [deg F] atmospheric temperature
nu = 1.621e-4; % [ft^2/s] kinematic viscosity of air at 68 deg
[windTime, windspeed] = windGenerator(u); % windspeed is in mph
wfps = windspeed.*5280/3600; % convert to [ft/s]

rocketSpeed = abs(RocketVel);
t = 0;
iCnt = 1;
%% Run loop
while rocketSpeed > -2   
    
    % Compute airspeed, angle of attack, lateral wind speed, Reynolds number...
    w_wind = (wfps(iCnt) + (t - windTime(iCnt))*(wfps(iCnt+1) - wfps(iCnt))...
        /(windTime(iCnt+1) - windTime(iCnt)))*-ihat; % Interpolate windspeed
    if RocketPos(3) < 20 % Wind is negligible til it leaves the rail
        w_wind = 0;
    end
    
    airspeed = RocketVel - w_wind; 
    
    Re = abs(airspeed)*lengthR/nu; 
    % angle of attack is angle between velocity and airspeed
    alpha = 0;
    % Compute aerodynamic forces and moments
    
    % Base drag
    
    % body pressure drag
    
    % Parasitic drag from tabs
    
    
    
    
    % Compute effect of motor thrust and gravity
    
    % Mass and force from motor
    [motorThrust, motorMass] = motorfunction(t); % returns mass in oz and thrust in lbf
    
    
    % Compute mass, moments of inertia, and linear and angular acceleration
    
    
    
    % Numerical integration using RK 4
    
    
    
    rocketSpeed = -5;
    t = t + dt;
    iCnt = iCnt + 1;
end