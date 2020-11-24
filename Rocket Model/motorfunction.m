function [motorThrust, motorMass] = motorfunction(t)

% Thrust values at given times for Cesaroni L1395
tVector = [0.02, 0.04, 0.1, 0.2, 0.4, 0.8, 1.1, 2.4, 2.8, 3, 3.18, 3.35, 3.45];
thrustVector = [100, 1400, 1800, 1500, 1540, 1591, 1641, 1481, 1446, 1500, 830, 100, 0].*0.224809;
% Vector in N, converted to lbf
massFull = 4.323; % [kg]
massEmpty = 1.848; % [kg]
burnTime = 3.51; %[s]
burnRate = (massFull - massEmpty)/burnTime; % [kg/s]

if t < 3.5 % Check if burnout has occurred
    motorMass = (massFull - t*burnRate)*35.274; % and converted to oz
    % See where in motor curve rocket is
    for i = 1:length(tVector)-1
        if t < tVector(i+1)
            motorThrust = thrustVector(i) +...
                (t - tVector(i))*(thrustVector(i+1) - thrustVector(i))...
                /(tVector(i+1) - tVector(i)); % Interpolate thrust
            
        end
        
    end
    
else
    motorThrust = 0;
end




end