import glfw
import numpy as np
from OpenGL.GL import *

global gComposedM
gComposeM = np.array([[1.,0.,0.],
                      [0.,1.,0.],
                      [0.,0.,1.]])

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposeM

    if key==glfw.KEY_1:
        if action == glfw.PRESS:
            gComposeM = np.array([[1.,0.,0.],
                                  [0.,1.,0.],
                                  [0.,0.,1.]])
            print("press 1")
    elif key==glfw.KEY_Q:
        if action == glfw.PRESS:
            newM = np.array([[1., 0., -0.1],
                             [0., 1., 0.],
                             [0., 0., 1.]])
            gComposeM = newM @ gComposeM # w.r.t global coordinate
            # gComposeM = gComposeM @ newM # w.r.t local coordinate
            print("press Q")
    elif key==glfw.KEY_E:
        if action == glfw.PRESS:
            newM = np.array([[1., 0., 0.1],
                             [0., 1., 0.],
                             [0., 0., 1.]])
            gComposeM = newM @ gComposeM # w.r.t global coordinate
            # gComposeM = gComposeM @ newM # w.r.t local coordinate
            print("press E")
    elif key==glfw.KEY_A:
        if action == glfw.PRESS:
            th = np.radians(10)
            newM = np.array([[np.cos(th), -np.sin(th), 0.],
                             [np.sin(th), np.cos(th), 0.],
                             [0., 0., 1.]]) 
            gComposeM = gComposeM @ newM # w.r.t local coordinate
            # gComposeM = newM @ gComposeM # w.r.t global coordinate
            print("press A")
    elif key==glfw.KEY_D:
        if action == glfw.PRESS:
            th = np.radians(10)
            newM = np.array([[np.cos(th), np.sin(th), 0.],
                             [-np.sin(th), np.cos(th), 0.],
                             [0., 0., 1.]]) 
            gComposeM = gComposeM @ newM # w.r.t local coordinate
            # gComposeM = newM @ gComposeM # w.r.t global coordinate
            print("press D")

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2021093518-3-1", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    # set the number of screen refresh to wait before calling glfw.swap_buffer().
    # if your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec 
    glfw.swap_interval(1)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using PyOpenGL
        render(gComposeM)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()