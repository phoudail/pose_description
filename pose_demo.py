import cv2
import glob
from pose_description import *
from pose_estimation import *

TPOSE = Body.left_arm.to_the_right(Body.left_shoulder) & Body.right_arm.to_the_left(Body.right_shoulder)
DABR = Body.right_arm.to_the_left(Body.right_shoulder) & Body.left_wrist.to_the_left(Body.head)
DABL = Body.left_arm.to_the_right(Body.left_shoulder) & Body.right_wrist.to_the_right(Body.head)
POSE1 = Body.left_forearm.above(Body.head) & Body.right_forearm.above(Body.head)
POSE2 = Body.right_forearm.above(Body.head) & Body.left_arm.below(Body.head) & Body.left_arm.to_the_right(Body.left_shoulder)
POSE3 = Body.left_knee.above(Body.left_hip) | Body.right_knee.above(Body.right_hip)
POSE4 = Body.left_forearm.above(Body.head) & Body.right_arm.below(Body.head) & Body.right_arm.to_the_left(Body.left_shoulder)


POSES = {POSE1: "Both hands raised", POSE2: "Right hand raised, left arm extended", POSE3: "Knee raised", POSE4: "Left hand raised, right arm extended", TPOSE: "T-pose", DABR: "Dabbing right", DABL: "Dabbing left"}

def vid_to_frames(vidPath='demo.mp4', framePath='VidFrames/Raw/demo_frame'):
    video = cv2.VideoCapture(vidPath)
    fps = video.get(cv2.CAP_PROP_FPS)
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(length):
        (retFrame, frame) = video.read()
        cv2.imwrite(f'{framePath}{i}.jpg', frame)
        print(f'Frame {i} written at {framePath}{i}.jpg')

    video.release()
    return (length, fps)


def frames_to_vid(fps, vidPath='demo_poses.mp4', framePath='VidFrames/Treated/demo_frame'):
    done = False
    i = 0
    frames = []
    while not done:
            image = cv2.imread(f'{framePath}{i}.jpg')
            if image is None:
                done = True
            else:
                height, width, layers = image.shape
                size = (width, height)
                frames.append(image)
                i += 1

    out = cv2.VideoWriter(vidPath, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    k = 0
    for j in frames:
        out.write(j)
        print(f'Frame {k} added to {size[0]}x{size[1]} @ {int(fps)}FPS video.')
        k += 1
    out.release()


def frame_treatment(framePath, resultPath):
    (skeleton, frame) = pose_estimation(framePath, True)
    height, width, layers = frame.shape
    bestPoseId = list(POSES.keys())[0]
    for pose in POSES.keys():
        bestPoseId = pose if pose(skeleton) > bestPoseId(skeleton) else bestPoseId
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.copyMakeBorder(frame, 0, 0, 0, 1000, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    i = 0
    for key in POSES.keys():
        i += 1
        if key == bestPoseId:
            cv2.putText(frame, f'{POSES[key]}: {key(skeleton)}', (width + 24, 50*i), font, 1, (255, 0, 255), 2)
        else:
            cv2.putText(frame, f'{POSES[key]}: {key(skeleton)}', (width + 24, 50*i), font, 1, (0, 0, 0), 2)
        
    cv2.imwrite(resultPath, frame)



def demo(vidPath='demo.mp4',demoPath='demo_pose.mp4', tempFrames='VidFrames/Raw/demo_frame', treatedFrames='VidFrames/Treated/demo_frame'):
    (length, framerate) = vid_to_frames(vidPath, tempFrames)
    for i in range(length):
        try:
            frame_treatment(f'{tempFrames}{i}.jpg', f'{treatedFrames}{i}.jpg')
            print(f'Frame {i} successfully processed.')
        except TypeError:
            print(f'Frame {i} processing failed. Adding non processed framed to video anyway.')
            cv2.imwrite(f'{treatedFrames}{i}.jpg',cv2.copyMakeBorder(cv2.imread(f'{tempFrames}{i}.jpg'), 0, 0, 0, 1000, cv2.BORDER_CONSTANT, value=[255, 255, 255]))
    frames_to_vid(framerate, demoPath, treatedFrames)
    
