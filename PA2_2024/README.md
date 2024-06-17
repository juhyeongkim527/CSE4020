# PA2
### Student ID : 2021093518
### Name : 김주형

## `SimpleScene.py`

Only this file in the `PA2` directory was modified. Below are the parts that were modified or added for the implementation of this project.

### `Global Variables` Declaration

- `CYCLECOUNT = 3`

This variable represents the number of times the cow will move along the control points as a roller coaster.

- `cowCount = -1`

This variable is used to track how many control points for the cow have been marked.

- `cowPosition = []`

This list stores the positions of the cow's control points.

- `animStartTime = 0`

This variable stores the start time of the cow's animation.

- `currentPos = []`

This variable is set in the `onMouseDrag` function to prevent the cow's position from changing when `V_DRAG` is active.


### `display` function

```
def display():
    ...
    ...
    # TODO: 
    # update cow2wld here to animate the cow.
    #animTime=glfw.get_time()-animStartTime;
    #you need to modify both the translation and rotation parts of the cow2wld matrix every frame.
    # you would also probably need a state variable for the UI.

    if(cowCount < 6):
        for pos in cowPosition: 
            drawCow(pos, False)
        drawCow(cow2wld, cursorOnCowBoundingBox) 

    elif(cowCount == 6):
        animTime=glfw.get_time()-animStartTime;
        
        if(animTime < 6 * CYCLECOUNT):
            t = float(animTime) - int(animTime)
            cowPos = spline(t, 
                            cowPosition[(int(animTime) + 5) % 6], 
                            cowPosition[int(animTime) % 6], 
                            cowPosition[(int(animTime) + 1) % 6],
                            cowPosition[(int(animTime) + 2) % 6])
                        
            direction = normalize(getTranslation(cowPos) - getTranslation(cow2wld))
            cowPos[:3, :3] = cowHeadDirection(direction)
            cow2wld = cowPos
            drawCow(cow2wld, False)

        else:
            cowCount = -1
            cowPosition = []

    glFlush();
```
1. When `cowCount` is less than 6, the control points have not all been drawn yet, so it iterates through `cowPosition` and draws only the control points that have been drawn so far using the `drawCow` function.

2. When `cowCount` reaches 6, the cow roller coaster animation starts. It calls the `spline` function and the `cowHeadDirection` function, implemented below, and continues drawing the cow using the `drawCow` function as long as `animTime` is within the specified `CYCLECOUNT`.

3. If `animTime` exceeds `CYCLECOUNT`, it resets `cowCount` and `cowPosition`.


### `spline` function

```
# Catmull-Rom Spline
def spline(t, p0, p1, p2, p3):
    return 0.5 * ((2 * p1) 
                + (-p0 + p2) * t 
                + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t 
                + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t)
```

This function returns the position on the spline curve at parameter `t` using the Catmull-Rom Spline formula learned in the theory class.


### `cowHeadDirection` function

```
def cowHeadDirection(direction):
    direction = direction.T

    pitch = np.arcsin(direction[1])
    yaw = np.arctan2(direction[0], direction[2]) - np.pi / 2

    Rpitch = np.array([[np.cos(pitch), -np.sin(pitch), 0],
                       [np.sin(pitch), np.cos(pitch), 0],
                       [0, 0, 1]])
    Ryaw = np.array([[np.cos(yaw), 0, np.sin(yaw)],
                     [0, 1, 0],
                     [-np.sin(yaw), 0, np.cos(yaw)]])
    
    return Ryaw @ Rpitch
```
Using **yaw orientation** and **pitch orientation**, this function calculates and returns the matrix to ensure the cow faces forward and faces upward when going up during the roller coaster animation.


### `onMouseButton` function

```
def onMouseButton(window,button, state, mods):
    global isDrag, V_DRAG, H_DRAG, cowCount, cowPosition, animStartTime
    GLFW_DOWN=1;
    GLFW_UP=0;
    x, y=glfw.get_cursor_pos(window)
    if button == glfw.MOUSE_BUTTON_LEFT:
        if state == GLFW_DOWN:
            # if isDrag==H_DRAG:
            #     isDrag=0
            # else:
            #     isDrag=V_DRAG;
            isDrag = V_DRAG
            print( "Left mouse down-click at %d %d\n" % (x,y))
            # start vertical dragging
        elif state == GLFW_UP and isDrag!=0:
            isDrag=H_DRAG;
            print( "Left mouse up\n");
            
            if cursorOnCowBoundingBox:
                cowCount += 1
                if(0 < cowCount < 7):
                    cowPosition.append(cow2wld.copy())
                    if(cowCount == 6):
                        animStartTime = glfw.get_time()                
                        isDrag = 0

            # start horizontal dragging using mouse-move events.
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if state == GLFW_DOWN:
            print( "Right mouse click at (%d, %d)\n"%(x,y) );
```

When the left mouse button is clicked, it stores the current number and positions of the cow's control points.

It checks if the cursor is on the cow's bounding box using `cursorOnCowBoundingBox`, and if so, it increments `cowCount`. When `cowCount` is between 1 and 6, it appends the current cow's control point to `cowPosition`.

When `cowCount` reaches 6, it stores `animStartTime` and sets `isDrag` to 0 before exiting.

The initial setting of `cowCount` to -1 is to handle the initial increase of `cowCount` when the left mouse button is clicked.


### `onMouseDrag` function & `initialize` function

```
def onMouseDrag(window, x, y):
    global isDrag,cursorOnCowBoundingBox, pickInfo, cow2wld, currentPos
    if isDrag: 
        print( "in drag mode %d\n"% isDrag);
        if  isDrag==V_DRAG:
            # vertical dragging
            # TODO:
            # create a dragging plane perpendicular to the ray direction, 
            # and test intersection with the screen ray.

            if cursorOnCowBoundingBox:
                ray = screenCoordToRay(window, x, y)
                pp = pickInfo
                p = Plane(np.array((1, 0, 0)), currentPos)
                c = ray.intersectsPlane(p)

                currentPos[1] = ray.getPoint(c[1])[1] # fix vertical position
                print(pp.cowPickPosition, currentPos)
                print(pp.cowPickConfiguration, cow2wld)

                T = np.eye(4)
                setTranslation(T, currentPos-pp.cowPickPosition)
                cow2wld = T @ pp.cowPickConfiguration;

            print('vdrag')

        else:
            # horizontal dragging
            ...
```            

implemented the condition for `V_DRAG` similarly to how `H_DRAG` was handled.

The difference is that I used `currentPos`, copied from `cow2wld` in the `initialize` function, to prevent the cow's control points from moving suddenly up or down when the left mouse button is clicked during `V_DRAG`.

And during `V_DRAG`, I fixed the cow's position in the vertical direction by modifying `currentPos[1]`.

```
def initialize(window):
    global cursorOnCowBoundingBox, floorTexID, cameraIndex, camModel, cow2wld, cowModel, currentPos
    ...
    ...
    cow2wld=glGetDoublev(GL_MODELVIEW_MATRIX).T # convert column-major to row-major 
    currentPos = getTranslation(cow2wld.copy())
    glPopMatrix();			# Pop the matrix on stack to GL.
```