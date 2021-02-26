%% RocketModel2

% Nick Crnkovich
% Simplified model. Projects apogee based on initial velocity,
% acceleration, and position inputs from sensors. Simulated effect of tab extension.
% Will be used to determine both the PID gains and live in flight to get the error
clear
%% initialize
angle_max = 70; % [deg] servo angle maximum actual value TBD
angle_min = 0; % [deg] servo angle minimum
angle = 0; % [deg] servo angle variable
extension = 0; % 0 no extension, 1 full extension

% Set parameters
% c = 1125.3; % [fps] speed of sound
c = 343; %[m/s] speed of sound
w_tabs = 1.71*0.0254; % [in to m] tab width
L_max_tabs = 1.4*0.0254; % [in to m] max tab length/extension
rho = 1.225; %[kg/m^3] density of air
M_e = 303/35.274; % [oz to kg] EMPTY mass of rocket
g = 9.81; % [m/s^2] gravity
theta = 0*pi/180; % [degrees to radians] launch angle
dt = 0.02; % [s] time step size
targetApogee = 1615.44; % [m]

% Initial conditions for simulation at BURNOUT, initalize variables for in flight
ax_R = 0; % [m/s^2] rocket acceleration
ay_R = -50*12*0.0254; % [ft/s^2 to m/s^2]
Vx_R = 0;
Vy_R = 600*cos(theta)*12*0.0254; % [ft/s to m/s] rocket vertical velocity 
x_R = 0; % [m] rocket x position
% alt_R = 1195*12*0.0254; % [ft to m] rocket altitude
alt_R = 995*12*0.0254; % [ft to m] rocket altitude

plotTarget = 0;
i = 1;
j = 1;
t = 0;

while Vy_R > 0  
%% Run Runge Kutta to predict apogee

% calculations
Vmag_R = sqrt(Vx_R^2 + Vy_R^2);
Mach = Vmag_R/c; % Mach number

% Tab drag

% Empirical fit for incompressible coefficient of drag tabs
Cd_o_tabs = 10^(0.44*extension - 0.7);
% adjusted for compressibility
Cd_tabs = 1/sqrt(1-Mach^2)*Cd_o_tabs;

% area of tabs as function of extension
A_tabs = 4*w_tabs*(extension*L_max_tabs); 

% rocket drag
Cd_rocket = 0.145;
% Cd_rocket = 0.3;
A_rocket = (6.17*0.0254/2)^2*pi; % [diamter in to m] [m^2]


% Runge Kutta
% update with new sensor data
VySim = Vy_R;
VxSim = Vx_R;
VmagSim = sqrt(VySim^2 + VxSim^2); % magnitude of velocity vector from data
axSim = ax_R;
aySim = ay_R;
altSim = alt_R;
xSim = x_R;

while VySim > 0    
    
%     k1vx = fx(VmagSim, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
    k1vy = dt*a(VmagSim, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
%     k1rx = VxSim;
    k1ry = dt*VySim;
    
%     k2vx = fx(VmagSim + 0.5*dt*k1rx, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
    k2vy = dt*a(VmagSim + 0.5*k1vy, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
%     k2rx = VxSim*k1vx*dt/2;
    k2ry = dt*(VySim + k1vy/2);
    
%     k3vx = fx(VmagSim + 0.5*dt*k2rx, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
    k3vy = dt*a(VmagSim + 0.5*k2vy, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
%     k3rx = VxSim*k2vx*dt/2;
    k3ry = dt*(VySim + k2vy/2);
    
%     k4vx = fx(VmagSim + dt*k3rx, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
    k4vy = dt*a(VmagSim + k3vy, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
%     k4rx = VxSim*k3vx*dt;
    k4ry = dt*(VySim + k3vy);
    
    % Find values at next timeStep
%     VxSim = VxSim + dt/6*(k1vx + 2*k2vx + 2*k3vx + k4vx);
    VySim = VySim + 1/6*(k1vy + 2*k2vy + 2*k3vy + k4vy);
    VmagSim = sqrt(VxSim^2 + VySim^2);
    
%     xSim = xSim + dt/6*(k1rx + 2*k2rx + 2*k3rx + k4rx);
    altSim = altSim + 1/6*(k1ry + 2*k2ry + 2*k3ry + k4ry);
    
    % Calculate new drag coefficient for tabs/(rocket?)
    Mach = VmagSim/c;
    Cd_tabs = 1/sqrt(1-Mach^2)*Cd_o_tabs;
    
end

SimApogee = altSim;
error = SimApogee - targetApogee;

%% PID/angle selection

Kp = 0.0007;
dExt = Kp*error;
extension = extension + dExt;


if extension > 1
    extension = 1;
elseif extension < 0
    extension = 0;
end

dExtVector(i) = dExt;


%% generate next data steps with adjusted drag

A_tabs_PID = 4*w_tabs*(extension*L_max_tabs); 

% k1vx = fx(Vmag_R, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
k1vy = dt*a(Vmag_R, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
% k1rx = Vx_R;
k1ry = dt*Vy_R;

% k2vx = fx(Vmag_R + 0.5*dt*k1rx, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
k2vy = dt*a(Vmag_R + 0.5*k1vy, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
% k2rx = Vx_R*k1vx*dt/2;
k2ry = dt*(Vy_R+k1vy/2);

% k3vx = fx(Vmag_R + 0.5*dt*k2rx, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
k3vy = dt*a(Vmag_R + 0.5*k2vy, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
% k3rx = Vx_R*k2vx*dt/2;
k3ry = dt*(Vy_R+k2vy/2);

% k4vx = fx(Vmag_R + dt*k3rx, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
k4vy = dt*a(Vmag_R + k3vy, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
% k4rx = Vx_R*k3vx*dt;
k4ry = dt*(Vy_R+k3vy);
    
% Find values at next timeStep
% Vx_R = Vx_R + dt/6*(k1vx + 2*k2vx + 2*k3vx + k4vx);
Vy_R = Vy_R + 1/6*(k1vy + 2*k2vy + 2*k3vy + k4vy);
Vmag_R = sqrt(Vx_R^2 + Vy_R^2);

% x_R = xSim + dt/6*(k1rx + 2*k2rx + 2*k3rx + k4rx);
alt_R = alt_R + 1/6*(k1ry + 2*k2ry + 2*k3ry + k4ry);

% Calculate new drag coefficient for tabs/(rocket?)
Mach = VmagSim/c;
Cd_tabs = 1/sqrt(1-Mach^2)*Cd_o_tabs;

% Store vectors for plotting
i = i + 1;
j = j + 1;
accelerationVector(i) = a(Vmag_R, Cd_rocket, Cd_tabs, A_tabs, theta, M_e);
extensionVector(i) = extension;
SimApogeeVector(i) = SimApogee;
errorVector(i) = error;
VyVector(i) = Vy_R;
altitudeVector(i) = alt_R;
t = t + dt;
tVect(i) = t;
end

apogeeFinal = alt_R;

figure(1); hold on;
plot(tVect(2:end), extensionVector(2:end))
grid on;
xlabel('time step (dt = 0.15s)')
ylabel('Extension Ratio')
legend('Simulation 1', 'Simulation 2', 'Simulation 3', 'Simulation 4', 'location', 'east')

figure(2);  hold on;
plot(tVect(2:end), errorVector(2:end))
grid on;
xlabel('time step (dt = 0.15s)')
ylabel('Predicted Error')
legend('Simulation 1', 'Simulation 2', 'Simulation 3', 'Simulation 4', 'location', 'east')

figure(3); hold on; 

if plotTarget
    plot(tVect(2:end), zeros(1, length(t)-1)+targetApogee, 'k')
end
plot(tVect(2:end), altitudeVector(2:end));
            
grid on;
xlabel('time step (dt = 0.15s)')
ylabel('Altitude (m)')
legend('target Apogee', 'Simulation 1', 'Simulation 2', 'Simulation 3', 'Simulation 4', 'location', 'east')


%% functions for RK4

function Kx = fx(V, Cd_rocket, Cd_tabs, A_tabs, theta, M_e)
    rho = 1.225; %[kg/m^3] density of air
    g = 9.81; % [m/s^2] gravity
    A_rocket = (6.17*0.0254/2)^2*pi; % [diamter in to m] [m^2]

    Kx = (-0.5*rho*Cd_rocket*V^2*A_rocket*sin(theta)...
            - 0.5*rho*Cd_tabs*V^2*A_tabs*sin(theta))/M_e; 
end
   
function Ky = a(V, Cd_rocket, Cd_tabs, A_tabs, theta, M_e)
    rho = 1.225; %[kg/m^3] density of air
    g = 9.81; % [m/s^2] gravity
    A_rocket = (6.17*0.0254/2)^2*pi; % [diamter in to m] [m^2]

    Ky = (-0.5*rho*Cd_rocket*V^2*A_rocket*cos(theta)...
            - 0.5*rho*Cd_tabs*V^2*A_tabs*cos(theta) - M_e*g)/M_e;
end



