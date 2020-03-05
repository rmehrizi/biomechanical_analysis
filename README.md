# biomechanical_analysis
A Python Package For Biomechanical Analysis <br />

This is a collection of modules that are helpful for biomechanical analysis. The python package contains three modules. <br />
1. *time_distance.py* <br />
  implements gait event detection, cascade and swing ratio calculation <br />
2. *inverse-kinematics.py* <br />
  Implements joint angle computations <br />
3. *inverse_dynamics.py* <br />
  Implements joint force and moment computations <br />

## Dependencies
Python 3.7 <br />
NumPy <br />
Pandas 
Matplotlib

## Data
In order to be able to test the package, sample gait data is provided in ```/data```. It contains the 3D coordinates of markers and ground reaction force obtained from two force plates. <br />
The markers should be in the following order: <br />
1.	*Neck*
2.	*Left ASIS*
3.	*Left lateral epicondyle of knee* 
4.	*Left lateral malleolus*
5.	*Head of left 2th metatarsal*
6.	*Head of left 5th metatarsal*
7.	*Right ASIS*
8.	*Right lateral epicondyle of knee*
9.	*Right lateral malleolus*
10.	*Head of right 2th metatarsal*
11.	*Head of right 5th metatarsal*

The force plate data should be in the following order: <br />
1.	*Center of pressure of left force plate*
2.	*Forces on the left force plate*
3.	*Moments on the left force plate*
4.	*Center of pressure of right force plate*
5.	*Forces on the right force plate*
6.	*Moments on the right force plate*

This computation assumes the following coordinate system: <br />
**x is from right to left leg** <br />
**y is from bottom to top** <br />
**z is from back to front** <br />

## Testing
When in the repository directory, run test.py <br />
```
python test.py
```
