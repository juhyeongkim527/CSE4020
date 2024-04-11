import glfw
import numpy as np
from OpenGL.GL import *

global primitive_type
primitive_type = GL_LINE_LOOP

def render() :
    global primitive_type
    
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    th = np.linspace(0, 2*np.pi, 13)
    vertices = np.array([(np.cos(_th), np.sin(_th)) for _th in th])[:-1]
    
    # vertices = np.array([[1,0]])
    # for _th in th:
    #     vertices = np.concatenate((vertices, np.array([(np.cos(_th),np.sin(_th))])))
    # vertices = vertices[1:-1]
    
    glBegin(primitive_type)
    glColor3ub(255, 255, 255)
    for vertex in vertices:
        glVertex2fv(vertex)
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global primitive_type

    if key==glfw.KEY_1:
        if action == glfw.PRESS:
            primitive_type = GL_POINTS
    elif key==glfw.KEY_2:
        if action == glfw.PRESS:
            primitive_type = GL_LINES
    elif key==glfw.KEY_3:
        if action == glfw.PRESS:
            primitive_type = GL_LINE_STRIP
    elif key==glfw.KEY_4:
        if action == glfw.PRESS:
            primitive_type = GL_LINE_LOOP
    elif key==glfw.KEY_5:
        if action == glfw.PRESS:
            primitive_type = GL_TRIANGLES           
    elif key==glfw.KEY_6:
        if action == glfw.PRESS:
            primitive_type = GL_TRIANGLE_STRIP
    elif key==glfw.KEY_7:
        if action == glfw.PRESS:
            primitive_type = GL_TRIANGLE_FAN
    elif key==glfw.KEY_8:
        if action == glfw.PRESS:
            primitive_type = GL_QUADS
    elif key==glfw.KEY_9:
        if action == glfw.PRESS:
            primitive_type = GL_QUAD_STRIP
    elif key==glfw.KEY_0:
        if action == glfw.PRESS:
            primitive_type = GL_POLYGON

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2021093518-2-1", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using PyOpenGL
        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()