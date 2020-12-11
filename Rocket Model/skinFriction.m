%% skinFriction.m
% Calculates the skin friction drag coefficient for the 2021 NASA Student
% Launch Rocket

% Author: Megan Kelleher
% Date: 12/11/2020
% University of Notre Dame Rocketry Team

%% Initialize Variables
% These constants are filler numbers to be replaced with actual data later

Cfc = 1.48 * (10^(-2)); % Skin friction coefficient, value taken from 
% piecewise fig 3.81

fb = 2.5; %fineness ratio of rocket

A_wet_body = 5; 

A_wet_fins = 5; 

t = 50; % thickness

c = 50; % mean aerodynamic chord lengths of the fins

A_ref = 2; 

%% Calculate skin friction drag coefficient

CD_friction = Cfc*((1+(1/(2*fb))) * A_wet_body + (1+ ((2*t)/c)) * A_wet_fins)/A_ref;

