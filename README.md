# Pose description

This project constitutes the base for a python library that allows for pose recognition and pose description in a way that makes it easily comprehensible for humans. This particular version of the code is tailored to work with a MPI human pose estimation neural network, but can be easily adapted to other recognition systems.


An example of a pose definition would be something like this :
```python
salute_pose = Body.right_arm.above(Body.head)
```

Poses are described by subclasses of a ```Pose``` class which act similarly to binary operators. Poses can also be combined with python's bitwise operators ```&```, ```|``` and ```~``` :
```python
pose1 = Body.right_arm.above(Body.head)
pose2 = Body.left_arm.above(Body.head)
surrendder = pose1 & pose2
```

Poses are currently constructed through the ```JointSelector```, ```SegmentSelector``` and ```LimbSelector``` classes, which, to make usage of the library easier, are grouped with the proper skeleton IDs under the ```Body``` class under body parts variables.
Once a pose is described, it is possible given a skeleton (which in the current implementation is a dictionnary with joint IDs as keys and coordinates as values) to call the pose, in order to determine how well the given skeleton fits the pose. This is returned in the form of a ```float``` varying between 0 and 1, using fuzzy logics principles.

This is an example of a processed image through usage of the library and a MPI neural network, with on the right side a few pose examples and the float result of calling them on the skeleton :
![Example of a processed image and poses corresponding to it](https://i.imgur.com/IOd8wLU.jpg)

This library isn't complete, and requires additional methods and adjustement of existing ones to be completely functionnal in all situations.
