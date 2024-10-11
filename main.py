from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from utils import draw_colored_cube, draw_axes, set_lights

import glm
import time

# PyGLM 행렬을 OpenGL에 사용할 수 있는 16개의 값으로 변환하는 함수
def glm_to_opengl_matrix(matrix):
    # 4x4 행렬의 각 요소를 추출하여 리스트로 변환 (열 우선 순서로)
    return [matrix[i][j] for i in range(4) for j in range(4)]

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # 화면 및 깊이 버퍼 지우기
    glLoadIdentity()

    # 카메라 설정
    gluLookAt(1, 3, 10,
               0, 0, 0, 
               0, 1, 0)
    # 현재 시간에 따른 회전
    current_time = time.time()  # 현재 시간을 초 단위로 가져옴
    angle = (current_time * 30) % 360  # 30도/초로 회전
    # 월드에 대해 회전 변환 적용
    glRotatef(angle, 0, 1.0, 0)

    draw_axes()

    # 정육면체 그리기
    glPushMatrix()
    # # 행렬의 곱을 통한 변환 적용
    translate = glm.translate(glm.mat4(1.0), glm.vec3(0, 0, 3))  # 이동 행렬
    rotate = glm.rotate(glm.mat4(1.0), glm.radians(45), glm.vec3(1, 0, 0))  # Z축 기준 45도 회전    
    transform_matrix = translate * rotate    
    glMultMatrixf(glm_to_opengl_matrix(transform_matrix))  # OpenGL에 변환 행렬 적용        
    draw_colored_cube(0.5)
    glPopMatrix()
    
    # 정육면체 그리기
    glPushMatrix()    
    transform_matrix = rotate * translate   
    glMultMatrixf(glm_to_opengl_matrix(transform_matrix))  # OpenGL에 변환 행렬 적용
    draw_colored_cube(0.5)
    glPopMatrix()    

    glutSwapBuffers()  # 화면 업데이트

def resize(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, w / h, 0.1, 500.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

def update(value):
    glutPostRedisplay()  # 디스플레이 함수 다시 호출 (화면 갱신)
    glutTimerFunc(16, update, 0)  # 16ms 후에 update 함수 다시 호출 (약 60FPS)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Example Code")

    # 조명 설정
    set_lights()

    # 디스플레이 함수 등록
    glutReshapeFunc(resize)
    glutDisplayFunc(display)
    # 16ms 간격으로 update 함수 호출
    glutTimerFunc(16, update, 0)

    # 이벤트 루프 시작
    glutMainLoop()

if __name__ == "__main__":
    main()
