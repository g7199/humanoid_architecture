import glm
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

joint_size = 0.3

from utils import draw_colored_cube, draw_colored_sphere, bone_rotation
spine_local_position = [[0, 2, 0], [0, 1.5, 0], [0, 1, 0], [0, 1.5, 0]]
ub_local_position = [[[-2, -1.5, 0], [-1.5, 0, 0], [-1.5, 0, 0], [-1, 0, 0], [-0.5, 0, 0]], [[2, -1.5, 0], [1.5, 0, 0], [1.5, 0, 0], [1, 0, 0], [0.5, 0, 0]]]
lb_local_position = [[[-0.8, 0, 0], [0, -2, 0], [0, -2, 0], [0, -2, 0], [0, -1, 0], [0, -0.5, 0.5], [0, 0, 0.5]], [[0.8, 0, 0], [0, -2, 0], [0, -2, 0], [0, -2, 0], [0, -1, 0], [0, -0.5, 0.5], [0, 0, 0.5]]]

def draw_humanoid():
    glPushMatrix()
    glTranslatef(0,0,0)
    draw_colored_sphere(joint_size)

    glPushMatrix()
    draw_bone(spine_local_position[0])
    glTranslate(*spine_local_position[0])
    draw_spine_joints()
    glPopMatrix()

    glPushMatrix()
    draw_bone(lb_local_position[0][0])
    glTranslatef(*lb_local_position[0][0])
    draw_leg_joints(is_right = False)
    glPopMatrix()

    glPushMatrix()
    draw_bone(lb_local_position[1][0])
    glTranslatef(*lb_local_position[1][0])
    draw_leg_joints(is_right = True)
    glPopMatrix()

    glPopMatrix()

def draw_spine_joints(level = 1):

    if level == 4:
        glPushMatrix()
        draw_colored_sphere(joint_size)
        draw_bone([0,1,0])

        glPushMatrix()
        draw_bone(ub_local_position[0][0])
        glTranslatef(*ub_local_position[0][0])
        draw_arm_joints(is_right = False)
        glPopMatrix()

        glPushMatrix()
        draw_bone(ub_local_position[1][0])
        glTranslatef(*ub_local_position[1][0])
        draw_arm_joints(is_right = True)
        glPopMatrix()

        glPopMatrix()
        return 0

    glPushMatrix()
    draw_colored_sphere(joint_size)
    draw_bone(spine_local_position[level])

    glPushMatrix()
    glTranslatef(*spine_local_position[level])
    draw_spine_joints(level+1)
    glPopMatrix()

    glPopMatrix()

def draw_arm_joints(is_right, level = 1):
    if level == 5:
        glPushMatrix()
        draw_colored_sphere(joint_size)
        glPopMatrix()
        return 0
    
    glPushMatrix()
    draw_colored_sphere(joint_size)
    draw_bone(ub_local_position[is_right][level])

    glPushMatrix()
    glTranslatef(*ub_local_position[is_right][level])
    draw_arm_joints(is_right, level+1)
    glPopMatrix()

    glPopMatrix()
    
    

def draw_leg_joints(is_right, level = 1):

    if level == 7:
        glPushMatrix()
        draw_colored_sphere(joint_size)
        glPopMatrix()
        return 0

    glPushMatrix()
    draw_colored_sphere(joint_size)
    draw_bone(lb_local_position[is_right][level])

    glPushMatrix()
    glTranslatef(*lb_local_position[is_right][level])
    draw_leg_joints(is_right, level+1)
    glPopMatrix()

    glPopMatrix()

def draw_bone(offset):
    mid = [offset[0] / 2.0, offset[1] / 2.0, offset[2] / 2.0]
    rot_quat = bone_rotation(glm.vec3(*offset))
    rot_mat = glm.mat4_cast(rot_quat)
    print('---------------------------------------')

    glPushMatrix()

    glTranslatef(*mid)
    glMultMatrixf(np.array(rot_mat, dtype=np.float32).flatten())
    glScalef(joint_size, abs(glm.l2Norm(offset)-2*joint_size)/2, joint_size)
    draw_colored_cube(1)

    glPopMatrix()