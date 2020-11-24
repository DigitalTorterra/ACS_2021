%% RocketModel

% November 2020
% Created by Nick Crnkovich

% Model using formulas and documentation from OpenRocket to generate our
% own simulation of the rocket apogee and position, velocity, acceleration
% data to be used for controller and ACS design


% Initialize rocket conditions
Ground = [1; 1; 1];


w = 10; % windspeed (pick units)
alpha = 5; % [deg] launch angle
v0 = 0; % initial velocity
RocketPos = 0.*Ground; % initial position

% Compute local wind velocity and atmospheric conditions
rho_air = 0.002378; % [slugs/ft^3] density of air
c_air = 1120; % [ft/s] speed of sound at 70 deg F
T = 68; % [def F] atmospheric temperature





% Compute airspeed, angle of attack, lateral wind speed, Reynolds number...




% Compute aerodynamic forces and moments

% Base drag

% body pressure drag

% Parasitic drag from tabs




% Compute effect of motor thrust and gravity

% Mass and force from motor
[motorThrust, motorMass] = motorfunction(t); % returns mass in oz and thrust in lbf


% Compute mass, moments of inertia, and linear and angular acceleration



% Numerical integration using RK 4