function [sample, windspeed] = windGenerator(u)

% Author: Nick Crnkovich
% Date: November 2020

% This function provides a vector of windspeeds at 20 Hz. An input of the
% average windspeed is used, and turbulence is simulated around the average
% windspeed using pink noise.
endTime = 25; % [s] Duration of flight
sample = 0:0.05:endTime; % generate sample at 20 Hz
alpha = 5/3;  % frequency spectrum of pink noise
wGauss = wgn(length(sample), 1, 0); % generates white noise
x = zeros(1, length(sample));
x(1) = 1; x(2) = 1;
windspeed = zeros(1, length(sample));
windspeed(1) = u; windspeed(2) = u;
sigma_u = 1.5;

for i = 1:length(wGauss)-2
    a0 = 1;
    a1 = (1 - 1 - alpha/2)*a0/1;
    a2 = (2 - 1 - alpha/2)*a1/1;
    
    x(i+2) = wGauss(i+2) - a1*x(i+1) - a2*x(i);
    x(i+2) = x(i+2)/2.252;
    
    windspeed(i+2) = u + sigma_u*x(i+2);
    
end

end