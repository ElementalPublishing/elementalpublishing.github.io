import bpy
import json

# Load pose data (example assumes JSON with frame-by-frame keypoint coords)
with open('pose_data.json') as f:
    pose_data = json.load(f)

# Create armature and bones (one-time setup)
bpy.ops.object.armature_add()
armature = bpy.context.object
bpy.context.view_layer.objects.active = armature
bones = armature.data.edit_bones

# Assume a bone for each keypoint (simplified)
keypoints = list(pose_data[0].keys())
for keypoint in keypoints:
    bone = bones.new(keypoint)
    bone.head = (0, 0, 0)  # Start at origin
    bone.tail = (0, 0.1, 0)  # Arbitrary length

# Animate bones for each frame
for frame_idx, frame_data in enumerate(pose_data):
    bpy.context.scene.frame_set(frame_idx)
    for keypoint, coords in frame_data.items():
        bone = bones[keypoint]
        bone.head = (coords[0], coords[1], 0)  # Map 2D coords to XY plane
        bone.tail = (coords[0], coords[1]+0.1, 0)
        bone.keyframe_insert(data_path="head", frame=frame_idx)
        bone.keyframe_insert(data_path="tail", frame=frame_idx)