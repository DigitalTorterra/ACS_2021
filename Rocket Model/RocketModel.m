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





% Compute airspeed, angle of attack, lateral wind speed, Reynolds number...




% Compute aerodynamic forces and moments

% Base drag

% body pressure drag

% Parasitic drag from tabs




% Compute effect of motor thrust and gravity

% Mass and force from motor



% Compute mass, moments of inertia, and linear and angular acceleration



% Numerical integration using RK 4