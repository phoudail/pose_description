import cv2
import math

from typing import List


MAX_LENGTH = 10


class Pose:

    def __init__(self, first, second):
        self.first = first
        self.second = second
       
    def __call__(self, skeleton):
        pass

    def matches(self, skeleton, tolerance=.8):
        return self(skeleton) > tolerance

    def __and__(self, other): # this redefines the '&' operator, not 'and'
        return AndPose(self, other)

    def __or__(self, other): # this redefines the '|' operator, not 'or'
        return OrPose(self, other)

    def __invert__(self): # this redefines the unary '~' operator, not 'not'
        return NotPose(self)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.first.__repr__()}, {self.second.__repr__()})'


class AndPose(Pose):

    def __call__(self, skeleton):
        return min(self.first(skeleton), self.second(skeleton))
    

class OrPose(Pose):

    def __call__(self, skeleton):
        return max(self.first(skeleton), self.second(skeleton))


class NotPose(Pose):

    def __init__(self, pose):
        self.pose = pose

    def __call__(self, skeleton):
        return 1 - self.pose(skeleton)

class LambdaPose(Pose):
    
    def __init__(self, criterion):
        self.criterion = criterion

    def __call__(self, skeleton):
        return self.criterion(skeleton)
    
class Above(Pose):

    def __call__(self, skeleton):
        return self.first(skeleton).above(self.second(skeleton))

class Below(Pose):
    
    def __call__(self, skeleton):
        return self.first(skeleton).below(self.second(skeleton))

class ToTheRight(Pose):

    def __call__(self, skeleton):
        return self.first(skeleton).to_the_right(self.second(skeleton))

class ToTheLeft(Pose):

    def __call__(self, skeleton):
        return self.first(skeleton).to_the_left(self.second(skeleton))
               
class AtSameHeight(Pose):

    def __call__(self, skeleton):
        return self.first(skeleton).at_same_height(self.second(skeleton))

class AtSameWidth(Pose):

    def __call__(self, skeleton):
        return self.first(skeleton).at_same_width(self.seccond(skeleton))

class IsNear(Pose): 

    def __call__(self, skeleton):
        return self.first(skeleton).is_near(self.second(skeleton))

class IsFar(Pose): 

    def __call__(self, skeleton):
        return self.first(skeleton).is_far(self.second(skeleton))

class PointsTo(Pose):

    def __call__(self, skeleton):
        return self.first(skeleton).points_to(self.second(skeleton))
        
class AlignedWith(Pose):

    def __call__(self, skeleton):
        return self.first(skeleton).aligned_with(self.second(skeleton))

class Crosses(Pose):

    def __call__(self, skeleton):
        return self.first(skeleton).crosses(self.second(skeleton))

class Parallel(Pose):

    def __call__(self, skeleton):
       return self.first(skeleton).parallel(self.second(skeleton))
   

class JointSelector:

    def __init__(self, joint_id):
        self.joint_id = joint_id
    
    def __call__(self, skeleton):
        (x, y) = skeleton[self.joint_id]
        return Joint(self.joint_id, x, y)

    def above(self, other):
        return Above(self, other)
        
    def below(self, other):
        return Below(self, other)

    def to_the_right(self, other):
        return ToTheRight(self, other)

    def to_the_left(self, other):
        return ToTheLeft(self, other)

    def at_same_height(self, other):
        return AtSameHeight(self, other)

    def at_same_width(self, other):
        return AtSameWidth(self, other)

    def is_near(self, other):
        return IsNear(self, other)

    def is_far(self, other):
        return IsFar(self, other)

    def __repr__(self):
        return f'JointSelector({self.joint_id.__repr__()})'
   
   
    
class Joint:
    
    right_wrist = 'rwrist'
    left_wrist = 'lwrist'
    right_elbow = 'relbow'
    left_elbow = 'lelbow'
    right_shoulder = 'rshoulder'
    left_shoulder = 'lshoulder'
    chest = 'chest'
    head = 'head'
    neck = 'neck'
    right_hip = 'rhip'
    left_hip = 'lhip'
    right_knee = 'rknee'
    left_knee = 'lknee'
    right_ankle = 'rankle'
    left_ankle = 'lankle'

    def __init__(self, id: str, x: int, y: int):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Joint({self.id.__repr__()}, {self.x.__repr__()}, {self.y.__repr__()})'

    def above(self, other):
        #TODO: Simple implementation for the moment, see results in practice
        if type(other) == Joint:
            return 1 if self.y < other.y else 0
        else:
            return self.above_all(other.to_joint_list())
        
    def above_all(self, others):
        top = min(joint.y for joint in others)
        bottom = max(joint.y for joint in others)
        try:
            return max(0, min(1, (bottom - self.y) / (bottom - top)))
        except ZeroDivisionError:
            return 1 if top > self.y else 0
    
    def below(self, other):
        if type(other) == Joint:
            return 1 if self.y > other.y else 0
        else:
            return self.below_all(other.to_joint_list())

    def below_all(self, others):
        top = min(joint.y for joint in others)
        bottom = max(joint.y for joint in others)
        try:
            return max(0, min(1, (self.y - top) / (bottom - top)))
        except ZeroDivisionError:
            return 1 if self.y > bottom else 0

    def to_the_right(self, other):
        if type(other) == Joint:
            return 1 if self.x > other.x else 0
        else:
            return self.to_the_right_all(other.to_joint_list())

    def to_the_right_all(self, others):
        right = max(joint.x for joint in others)
        left = min(joint.x for joint in others)
        try:
            return max(0, min(1, (self.x - left) / (right - left)))
        except ZeroDivisionError:
            return 1 if self.x > right else 0

    def to_the_left(self, other):
        if type(other) == Joint:
            return 1 if self.x < other.x else 0
        else:
            return self.to_the_left_all(other.to_joint_list())

    def to_the_left_all(self, others):
        right = max(joint.x for joint in others)
        left = min(joint.x for joint in others)
        try:
            return max(0, min(1, (right - self.x) / (right - left)))
        except ZeroDivisionError:
            return 1 if self.x < left else 0

    def is_near(self, other):
        pass

    def is_far(self, other):
        pass

    def at_same_height(self, other):
        pass

    def at_same_width(self, other):
        pass

    def aligned_with(self, other):
        pass


class SegmentSelector:

    def __init__(self, segm_id: tuple):
        self.segm_id = segm_id

    def __call__(self, skeleton):
        j1 = JointSelector(self.segm_id[0])
        j2 = JointSelector(self.segm_id[1])
        return Segment(j1(skeleton), j2(skeleton))

    def above(self, other):
        return Above(self, other)

    def below(self, other):
        return Below(self, other)

    def to_the_right(self, other):
        return ToTheRight(self, other)

    def to_the_left(self, other):
        return ToTheLeft(self, other)

    def at_same_height(self, other):
        return AtSameHeight(self, other)

    def at_same_width(self, other):
        return AtSameWidth(self, other)

    def is_near(self, other):
        return IsNear(self, other)

    def is_far(self, other):
        return IsFar(self, other)

    def points_to(self, other):
        return PointsTo(self, other)

    def aligned_with(self, other):
        return AlignedWith(self, other)

    def parallel(self, other):
        return Parallel(self, other)

    def __repr__(self):
        return f'SegmentSelector({self.segm_id.__repr__()})'

class Segment:

    face = ('head', 'neck')
    right_forearm = ('rwrist', 'relbow')
    left_forearm = ('lwrist', 'lelbow')
    right_biceps = ('relbow', 'rshoulder')
    left_biceps = ('lelbow', 'lshoulder')
    right_trapezius = ('rshoulder', 'neck')
    left_trapezius = ('lshoulder', 'neck')
    torso = ('neck', 'chest')
    right_rib = ('chest', 'rhip')
    left_rib = ('chest', 'lhip')
    right_thigh = ('rhip', 'rknee')
    left_thigh = ('lhip', 'lknee')
    right_calf = ('rknee', 'rankle')
    left_calf = ('lknee', 'lankle')

    
    def __init__(self, firstJoint, secondJoint):
        self.firstJoint = firstJoint
        self.secondJoint = secondJoint

    def __repr__(self):
        return f'Segment({self.firstJoint.__repr__()}, {self.secondJoint.__repr__()})'

    def to_joint_list(self):
        return [self.firstJoint, self.secondJoint]

    def above(self, other):
        if type(other) == Joint:
            return other.below_all(self.to_joint_list())
        else:
            return self.above_all(other.to_joint_list())

    def above_all(self, others):
        top1 = min(self.firstJoint.y, self.secondJoint.y)
        bottom1 = max(self.firstJoint.y, self.secondJoint.y)
        top2 = min(joint.y for joint in others)
        try:
            return max(0, min(1, (top2 - top1) / (bottom1 - top1)))
        except ZeroDivisionError:
            return 1 if top2 > top1 else 0
        
    def below(self, other):
        if type(other) == Joint:
            return other.above_all(self.to_joint_list())
        else:
            return self.below_all(other.to_joint_list())

    def below_all(self, others):
        top1 = min(self.firstJoint.y, self.secondJoint.y)
        bottom1 = max(self.firstJoint.y, self.secondJoint.y)
        bottom2 = max(joint.y for joint in others)
        try:
            return max(0, min(1, (bottom1 - bottom2) / (bottom1 - top1)))
        except ZeroDivisionError:
            return 1 if bottom1 > bottom2 else 0
       
    def to_the_right(self, other):
        if type(other) == Joint:
            return other.to_the_left_all(self.to_joint_list())
        else:
            return self.to_the_right_all(other.to_joint_list())

    def to_the_right_all(self, others):
        right1 = max(self.firstJoint.x, self.secondJoint.x)
        left1 = min(self.firstJoint.x, self.secondJoint.x)
        right2 = max(joint.x for joint in others)
        try:
            return max(0, min(1, (right1 - right2) / (right1 - left1)))
        except ZeroDivisionError:
            return 1 if left1 > right2 else 0
   
    def to_the_left(self, other):
        if type(other) == Joint:
            return other.to_the_right_all(self.to_joint_list())
        else:
            return self.to_the_left_all(other.to_joint_list())

    def to_the_left_all(self, others):
        right1 = max(self.firstJoint.x, self.seondJoint.x)
        left1 = min(self.firstJoint.x, self.secondJoint.x)
        left2 = min(joint.x for joint in others)
        try:
            return max(0, min(1, (left2 - left1) / (right1 - left1)))
        except ZeroDivisionError:
            return 1 if right2 < left2 else 0

    def is_near(self, other):
        pass
    
    def is_far(self, other):
        pass
   
    def at_same_height(self, other):
        pass

    def at_same_width(self, other):
        pass

    def points_to(self, other):
        pass

    def crosses(first, second, skeleton):
        pass

    def parallel(first, second, skeleton):
        pass

    def aligned_with(first, second, skeleton):
        pass

class LimbSelector:

    def __init__(self, limb_id: List[str]):
        self.limb_id = limb_id

    def __call__(self, skeleton):
        joint_list = [JointSelector(joint)(skeleton) for joint in self.limb_id]
        return Limb(joint_list)

    def above(self, other):
        return Above(self, other)

    def below(self, other):
        return Below(self, other)

    def to_the_right(self, other):
        return ToTheRight(self, other)

    def to_the_left(self, other):
        return ToTheLeft(self, other)

    def at_same_height(self, other):
        return AtSameHeight(self, other)

    def at_same_width(self, other):
        return AtSameWidth(self, other)

    def is_near(self, other):
        return IsNear(self, other)

    def is_far(self, other):
        return IsFar(self, other)

    def points_to(self, other):
        return PointsTo(self, other)

    def aligned_with(self, other):
        return AlignedWith(self, other)

    def parallel(self, other):
        return Parallel(self, other)

    def straight(self):
        return Parallel(self, self)

    def __repr__(self):
        return f'LimbSelector({self.limb_id.__repr__()})'
    

class Limb:
    
    right_arm = ['rwrist', 'relbow', 'rshoulder']
    left_arm = ['lwrist', 'lelbow', 'lshoulder']
    right_leg = ['rhip', 'rknee', 'rankle']
    left_leg = ['lhip', 'lknee', 'lankle']


    def __init__(self, joints):
        self.joints = joints

    @property
    def first_joint(self):
        return self.joints[0]

    @property
    def second_joint(self):
        return self.joints[1]

    @property
    def third_joint(self):
        return self.joints[2]

    def __repr__(self):
        return f'Limb({self.joints.__repr__()})'

    def to_joint_list(self):
        return self.joints

    def above(self, other):
        if type(other) == Joint:
           return other.below_all(self.to_joint_list())
        else:
            return self.above_all(other.to_joint_list())

    def above_all(self, others):
        top1 = min(joint.y for joint in self.joints)
        bottom1 = max(joint.y for joint in self.joints)
        top2 = min(joint.y for joint in others)
        try:
            return max(0, min(1, (top2 - top1) / (bottom1 - top1)))
        except ZeroDivisionError:
            return 1 if top2 > top1 else 0

    def below(self, other):
        if type(other) == Joint:
            return other.above_all(self.to_joint_list())
        else:
            return self.below_all(other.to_joint_list())

    def below_all(self, others):
        top1 = min(joint.y for joint in self.joints)
        bottom1 = max(joint.y for joint in self.joints)
        bottom2 = max(joint.y for joint in others)
        try:
            return max(0, min(1, (bottom1 - bottom2) / (bottom1 - top1)))
        except ZeroDivisionError:
            return 1 if bottom1 > bottom2 else 0

    def to_the_right(self, other):
        if type(other) == Joint:
            return other.to_the_left_all(self.to_joint_list())
        else:
            return self.to_the_right_all(other.to_joint_list())

    def to_the_right_all(self, others):
        right1 = max(joint.x for joint in self.joints)
        left1 = min(joint.x for joint in self.joints)
        right2 = max(joint.x for joint in others)
        try:
            return max(0, min(1, (right1 - right2) / (right1 - left1)))
        except ZeroDivisionError:
            return 1 if left1 > right2 else 0

    def to_the_left(self, other):
        if type(other) == Joint:
            return other.to_the_right_all(self.to_joint_list())
        else:
            return self.to_the_left_all(other.to_joint_list())

    def to_the_left_all(self, others):
        right1 = max(joint.x for joint in self.joints)
        left1 = min(joint.x for joint in self.joints)
        left2 = min(joint.x for joint in others)
        try:
            return max(0, min(1, (left2 - left1) / (right1 - left1)))
        except ZeroDivisionError:
            return 1 if right1 < left2 else 0

class Body:

    right_wrist = JointSelector(Joint.right_wrist)
    left_wrist = JointSelector(Joint.left_wrist)
    right_elbow = JointSelector(Joint.right_elbow)
    left_elbow = JointSelector(Joint.left_elbow)
    right_shoulder = JointSelector(Joint.right_elbow)
    left_shoulder = JointSelector(Joint.left_elbow)
    chest = JointSelector(Joint.chest)
    head = JointSelector(Joint.head)
    neck = JointSelector(Joint.neck)
    right_hip = JointSelector(Joint.right_hip)
    left_hip = JointSelector(Joint.left_hip)
    right_knee = JointSelector(Joint.right_knee)
    left_knee = JointSelector(Joint.left_knee)
    right_ankle = JointSelector(Joint.right_ankle)
    left_ankle = JointSelector(Joint.left_ankle)

    face = SegmentSelector(Segment.face)
    right_forearm = SegmentSelector(Segment.right_forearm)
    left_forearm = SegmentSelector(Segment.left_forearm)
    right_biceps = SegmentSelector(Segment.right_biceps)
    left_biceps = SegmentSelector(Segment.left_biceps)
    right_trapezius = SegmentSelector(Segment.right_trapezius)
    left_trapezius = SegmentSelector(Segment.left_trapezius)
    torso = SegmentSelector(Segment.torso)
    right_rib = SegmentSelector(Segment.right_rib)
    left_rib = SegmentSelector(Segment.left_rib)
    right_thigh = SegmentSelector(Segment.right_thigh)
    left_thigh = SegmentSelector(Segment.left_thigh)
    right_calf = SegmentSelector(Segment.right_calf)
    left_calf = SegmentSelector(Segment.left_calf)

    right_arm = LimbSelector(Limb.right_arm)
    left_arm = LimbSelector(Limb.left_arm)
    right_leg = LimbSelector(Limb.right_leg)
    left_leg = LimbSelector(Limb.left_leg)
