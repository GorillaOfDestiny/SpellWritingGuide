import numpy as np
import math

def centre_circle(P,Q,thetas = None):
    x1 = P[0]
    y1 = P[1]
    x2 = Q[0]
    y2 = Q[1]
    a = (x1+x2)/2
    b = (y1+y2)/2
    r = np.sqrt((a-x1)**2 + (b-y1)**2)
    if thetas == "Full":
        theta = np.linspace( 0 , 2 * np.pi , 150 )
    else:
        theta0 = math.atan2(y1-b, x1-a)
        theta1 = math.atan2(y2-b, x2-a)
        if y2 < y1:
            theta0,theta1 = theta1 + np.pi,theta0+np.pi
        theta = np.linspace(theta0,theta1,150)
    X2 = r*np.cos(theta)+a
    Y2 = r*np.sin(theta)+b
    return(X2,Y2)

def non_centre_circle(P,Q,b,thetas = None):
    x1 = P[0]
    y1 = P[1]
    x2 = Q[0]
    y2 = Q[1]
    b2 = -b
    delta = x1**2 - x2**2 + y1**2 - y2**2
    a = (delta-2*(y1 - y2)*b)/(2*(x1 - x2))
    a2 = (delta-2*(y1 - y2)*b2)/(2*(x1 - x2))
    r = np.sqrt((x1-a)**2 + (y1 - b)**2)
    r2 = np.sqrt((x1-a2)**2 + (y1 - b2)**2)
    if r2 <= r:
        a = a2
        b = b2
        r = r2

    if thetas == "Full":
        theta1 = np.linspace( 0 , 2 * np.pi , 150 )
 
    else:
        theta0 = math.atan2(y1-b, x1-a)
        theta1 = math.atan2(y2-b, x2-a)
        theta02 = theta0
        theta12 = theta1
        while theta1 < theta0:
            theta0 -= 2*np.pi  
        while theta02 < theta12:
            theta12 -= 2*np.pi
        arc1 = r*(theta1 - theta0)
        arc2 = r*(theta02 - theta12)
        if arc1 < arc2 or np.sqrt(b**2) <1:
            theta = np.linspace(theta1,theta0,150)
        else:
            theta = np.linspace(theta02,theta12,150)
    
    X = r*np.cos(theta)+a
    Y = r*np.sin(theta)+b
    return(X,Y)

def straight(P,Q):
    X = [P[0],Q[0]]
    Y = [P[1],Q[1]]
    return(X,Y)