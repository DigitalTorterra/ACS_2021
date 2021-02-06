"""
This file contains code relating to
controlling the servo, mostly PID
or some subset of it, with gain 
scheduling or whatever fancy stuff
you guys do
"""

# Import modules
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

# Global Variables
initialized = False
angle = 0
angle_min = 0
angle_max = 70 # degrees. Mechanism is changing so don't actually know if this is right
extension = 0  # 0 no extension, 1 full extension

# Function definitions
def initialize(data):
    """
    Author:
    This function should do whatever work
    is required to initialize the algorithm
    Input: data - output from filter, will
    be an ordered pair of data
    Output: None
    """
    height, velocity, acceleration, *_ = data

    return None

def step(data, extension):
    """
    Author: Nick Crnkovich
    This function should perform a computation
    step which takes in sensor data and updates
    the current recommended angle
    Input: data - output from filter, will
    be an ordered pair of data
    Output: None
    """
    height, velocity, acceleration, *_ = data


    # Set parameters
    # c = 1125.3  # [fps] speed of sound
    c = 343  #[m/s] speed of sound
    w_tabs = 1.71*0.0254  # [in to m] tab width
    L_max_tabs = 1.85*0.0254  # [in to m] max tab length/extension
    rho = 1.225  #[kg/m**3] density of air
    M_e = 771.2/35.274  # [oz to kg] EMPTY mass of rocket
    g = 9.81  # [m/s**2] gravity
    theta = 5*np.pi/180  # [degrees to radians] launch angle
    dt = 0.2  # [s] time step size
    targetApogee = 1615.44  # [m]

    # Initial conditions for simulation at BURNOUT, initalize variables for in flight
    ax_R = 0  # [m/s**2] rocket acceleration
    ay_R = acceleration 
    Vx_R = 0 
    Vy_R = velocity  # [m/s] rocket vertical velocity 
    x_R = 0  # [m] rocket x position
    alt_R = height # [m] rocket altitude

    ## Run Runge Kutta to predict apogee

    # calculations
    Vmag_R = np.sqrt(Vx_R**2 + Vy_R**2) 
    Mach = Vmag_R/c  # Mach number

    # Tab drag
    # Empirical fit for incompressible coefficient of drag tabs
    Cd_o_tabs = 10**(0.44*extension - 0.7) 
    # adjusted for compressibility
    Cd_tabs = 1/np.sqrt(1-Mach**2)*Cd_o_tabs 

    # area of tabs as function of extension
    A_tabs = 4*w_tabs*(extension*L_max_tabs)  

    # rocket drag
    Cd_rocket = 0.3 
    A_rocket = (6.17*0.0254/2)**2*np.pi  # [diamter in to m] [m**2]


    # Runge Kutta
    # update with new sensor data
    VySim = Vy_R 
    VxSim = Vx_R 
    VmagSim = np.sqrt(VySim**2 + VxSim**2)  # magnitude of velocity vector from data
    axSim = ax_R 
    aySim = ay_R 
    altSim = alt_R 
    xSim = x_R 

    while VySim > 0:  
        
        # k1vx = fx(VmagSim, Cd_rocket, Cd_tabs, A_tabs, theta, M_e) 
        k1vy = fy(VmagSim, Cd_rocket, Cd_tabs, A_tabs, theta, M_e) 
        # k1rx = VxSim 
        k1ry = VySim 
        
        # k2vx = fx(VmagSim + 0.5*dt*k1rx, Cd_rocket, Cd_tabs, A_tabs, theta, M_e) 
        k2vy = fy(VmagSim + 0.5*dt*k1ry, Cd_rocket, Cd_tabs, A_tabs, theta, M_e) 
        # k2rx = VxSim*k1vx*dt/2 
        k2ry = VySim*k1vy*dt/2 
        
        # k3vx = fx(VmagSim + 0.5*dt*k2rx, Cd_rocket, Cd_tabs, A_tabs, theta, M_e) 
        k3vy = fy(VmagSim + 0.5*dt*k2ry, Cd_rocket, Cd_tabs, A_tabs, theta, M_e) 
        # k3rx = VxSim*k2vx*dt/2 
        k3ry = VySim*k2vy*dt/2 
        
        # k4vx = fx(VmagSim + dt*k3rx, Cd_rocket, Cd_tabs, A_tabs, theta, M_e) 
        k4vy = fy(VmagSim + dt*k3ry, Cd_rocket, Cd_tabs, A_tabs, theta, M_e) 
        # k4rx = VxSim*k3vx*dt 
        k4ry = VySim*k3vy*dt 
        
        # Find values at next timeStep
        # VxSim = VxSim + dt/6.0*(k1vx + 2.0*k2vx + 2.0*k3vx + k4vx) 
        VySim = VySim + dt/6.0*(k1vy + 2.0*k2vy + 2.0*k3vy + k4vy) 
        VmagSim = np.sqrt(VxSim**2 + VySim**2) 
        
        # xSim = xSim + dt/6.0*(k1rx + 2*k2rx + 2*k3rx + k4rx) 
        altSim = altSim + dt/6.0*(k1ry + 2*k2ry + 2*k3ry + k4ry) 
        
        # Calculate new drag coefficient for tabs/(rocket?)
        Mach = VmagSim/c 
        Cd_tabs = 1/np.sqrt(1-Mach**2)*Cd_o_tabs 

    SimApogee = altSim 
    error = SimApogee - targetApogee 

    ## PID/angle selection
    if error < 0:
        extension = 0  # if simulated apogee is below target, stop
    elif error > 100: 
        extension = 1  # if simulated apogee is > 100 m above target, full extension
    else:
        kp = 0.01 
        extension = kp*error 
    

    if extension > 1:
        extension = 1 
    elif extension < 0:
        extension = 0 
    
    return extension


def get_angle(extension):
    """
    Author: Nick Crnkovich
    This function should output the current
    angle the servo should be extended to
    Input: None
    Output: current angle
    """
    servo_angle = extension*angle_max
    return servo_angle

def get_min():
    """
    Author:
    This function should output the minimum
    angle the servo can be rotated to
    Input: None
    Output: minimum angle
    """
    angle_min = 0
    return angle_min

def get_max():
    """
    Author:
    This function should output the maximum
    angle the servo can be rotated to
    Input: None
    Output: maximum angle
    """
    angle_max = 70

    return angle_max

# functions to be used for RK

def fy(V, Cd_rocket, Cd_tabs, A_tabs, theta, M_e):
    rho = 1.225 #[kg/m **3] density of air
    g = 9.81 # [m/s **2] gravity
    A_rocket = (6.17*0.0254/2)**2*np.pi # [diamter in to m] [m**2]

    Ky = -(0.5*rho*Cd_rocket*V**2*A_rocket*np.sin(theta) - 0.5*rho*Cd_tabs*V**2*A_tabs*np.sin(theta) - M_e*g)/M_e

    return Ky
 
def fx(V, Cd_rocket, Cd_tabs, A_tabs, theta, M_e):
    rho = 1.225 #[kg/m**3] density of air
    g = 9.81 #[m/s**2] gravity
    A_rocket = (6.17*0.0254/2)**2*np.pi # [diamter in to m] [m**2]

    Kx = -(0.5*rho*Cd_rocket*V**2*A_rocket*np.cos(theta) - 0.5*rho*Cd_tabs*V**2*A_tabs*np.cos(theta))/M_e
    return Kx



    
