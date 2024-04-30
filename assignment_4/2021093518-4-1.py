import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2,2, -2,2, -1,1)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    drawFrame()
    t = glfw.get_time()
    
    # blue base transformation
    glPushMatrix() # I, I
    # left to right means local frame transformation
    # right to left means global frame transformation
    glTranslatef(np.sin(t), 0, 0) # T1, I

    # blue base drawing
    glPushMatrix() # T1, T1, I
    glScalef(.2, .2, .2) # T1S, T1, I
    glColor3ub(0, 0, 255)
    drawBox() # T1S, T1, I
    glPopMatrix() # T1, I
    glTranslatef(.0, 0, .01) # T1T2, I
    # z-axis .01 means that the local coordinate is upper than blue base
    drawFrame() # T1T2, I
    
    # red arm transformation
    glPushMatrix() # T1T2, T1T2, I
    glRotatef(t*(180/np.pi), 0, 0, 1) # T1T2R, T1T2, I
    glTranslatef(.5, 0, .01) # T1T2RT#3, T1T2, I
    # z-axis .01 means that the red arm is upper than the blue base and local coordinate of blue base
    
    # red arm drawing
    glPushMatrix() # T1T2RT3, T1T2RT3, T1T2, I
    glScalef(.5, .1, .1) # T1T2RT3S, T1T2RT3, T1T2, I
    glColor3ub(255, 0, 0) 
    drawBox() # T1T2RT3S, T1T2RT3, T1T2, I
    glPopMatrix() # T1T2RT3, T1T2, I
    glTranslatef(.0, 0, .01) # T1T2RT4, T1T2, I
    # z-axis .01 means that the local coordinate is upper than red arm
    drawFrame() # T1T2RT4, T1T2, I

    # green arm transformation
    glPushMatrix() # T1T2RT4, T1T2RT4, T1T2, I
    glTranslatef(.5, 0, .01) # T1T2RT4T5, T1T2RT4, T1T2, I
    # z-axis .01 means that the green arm is upper than the red arm
    glRotatef(t*(180/np.pi), 0, 0, 1) # T1T2RT4T5R, T1T2RT4, T1T2, I

    # green arm drawing
    glPushMatrix() # T1T2RT4T5R, T1T2RT4T5, T1T2RT4, T1T2, I
    glScalef(.2, .2, .2) # T1T2RT4T5RS, T1T2RT4T5R, T1T2RT4, T1T2, I
    glColor3ub(0, 255, 0)
    drawBox() # T1T2RT4T5RS, T1T2RT4T5R, T1T2RT4, T1T2, I
    glPopMatrix() # T1T2RT4T5R, T1T2RT4, T1T2, I
    glTranslatef(.0, 0, .01) # T1T2RT4T5R, T1T2RT4, T1T2, I
    # z-axis .01 means that the local coordinate is upper than green arm
    drawFrame() # T1T2RT4T5R, T1T2RT4, T1T2, I

    glPopMatrix() # T1T2RT4, T1T2, I
    glPopMatrix() # T1T2, I
    glPopMatrix() # I

def drawBox():
    glBegin(GL_QUADS)
    glVertex3fv(np.array([1,1,0.]))
    glVertex3fv(np.array([-1,1,0.]))
    glVertex3fv(np.array([-1,-1,0.]))
    glVertex3fv(np.array([1,-1,0.]))
    glEnd()

def drawFrame():
    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2021093518-4-1', None,None)

    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()