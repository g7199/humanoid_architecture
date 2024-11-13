from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from utils import draw_colored_cube, draw_axes, set_lights

import glm

center = glm.vec3(0, 0, 0)
eye = glm.vec3(1, 3, 10)
upVector = glm.vec3(0, 1, 0)

last_x, last_y = 0, 0
is_rotating = False
is_translating = False

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # 카메라 설정    
    gluLookAt(eye.x, eye.y, eye.z,
              center.x, center.y, center.z,
              upVector.x, upVector.y, upVector.z)

    draw_axes()
    draw_colored_cube(0.5)

    glutSwapBuffers()

def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def motion(x, y):
    """마우스 드래그 이벤트 처리"""
    global eye, center, upVector, last_x, last_y

    dx = x - last_x
    dy = y - last_y
    last_x, last_y = x, y

    if is_rotating:        # 회전
        center2eye = eye - center
        rotation = glm.rotate(glm.mat4(1.0), -dx*0.01, glm.vec3(0, 1, 0))
        rotation = glm.rotate(rotation, -dy*0.01, glm.vec3(1, 0, 0))
        rotated = glm.vec3(rotation * center2eye)
        eye = center + rotated
        
    elif is_translating:
        # 평행 이동
        translation = glm.vec3(-dx, dy, 0) * 0.01
        eye += translation
        center += translation

    glutPostRedisplay()

def mouse(button, state, x, y):
    """마우스 버튼 이벤트 처리"""
    global last_x, last_y, is_rotating, is_translating

    last_x, last_y = x, y

    if button == GLUT_LEFT_BUTTON:
        is_rotating = (state == GLUT_DOWN)
    elif button == GLUT_RIGHT_BUTTON:
        is_translating = (state == GLUT_DOWN)

def mouse_wheel(button, direction, x, y):
    """마우스 휠 이벤트 처리 (Zoom In/Out)"""
    global eye, center  
    
    zoom_speed = 0.9 if direction > 0 else 1.1
    eye = eye*zoom_speed   

    glutPostRedisplay()
    
def update(value):
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Camera Control Example")

    glEnable(GL_DEPTH_TEST)
    set_lights()

    glutReshapeFunc(resize)
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutMouseWheelFunc(mouse_wheel) 
    glutTimerFunc(16, update, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
