# @desc: contains the implementation for the UI
# @author: Yahya

# all the required modules
import pygame as pg
from collections import deque
import box 

# The ui class
class ui:

    surface = None # the drawing surface
    running = True # determines if the app is running
    drag = False # determines if user is dragging 
    sourceAndDestSelection = False 
    source = -1 # the source node
    dest = -1 # the destination node
    completed = False # determines if the algo is finished with finding the path
    allBoxes = {} # dictionary for containing all the boxes/node
    baseBoxSize = 30 # base size for all the boxes/nodes
    graph = {} # dictionary for storing the graph

    # @desc: the constructor
    # @args:
    # @sWidth: the window width
    # @sHeight: the window height
    # @bgColor: the window background color
    # @tRows: total number of rows containing boxes
    # @perRow: total number of boxes per row aka columns
    def __init__(self, sWidth, sHeight, bgColor, tRows, perRow):
        pg.init() # pygame init
        pg.display.set_caption("SPV") # set the window title
        self.surface = pg.display.set_mode((sWidth, sHeight)) # create window with the specified width and height
        self.surface.fill(bgColor) # set the background color for the window
        self.initBoxes(tRows, perRow) # create all the boxes/nodes
        self.initGraph() # create the graph
        self.loop() # start the main loop

    # @desc: creates the boxes/nodes
    # @args: 
    # @tRows: total number of rows
    # @perRow: total number of boxes per row
    def initBoxes(self, tRows, perRow):
        xPos = 0 # represents x position of a box
        yPos = 0 # represents the y position of a box
        idx = 0 # represents the number of the box used as a key in the dictionary
        for i in range(0,tRows):
            for j in range(0,perRow):
                # create a new box object with the specified position, base size and color
                newBox = box.box(xPos, yPos, self.baseBoxSize, self.baseBoxSize, (0,0,0))
                # store box in the dictionary
                self.allBoxes[idx] = newBox
                # increment idx by one to represent the next box
                idx += 1
                # increment xPos by base size so that the next box will be displayed immediately after the previous one
                xPos += self.baseBoxSize

            # set xPos back to 0 for the next row
            xPos = 0
            # increment yPos by the base size to display the boxes in the next row immediately after the previous one
            yPos += self.baseBoxSize

    # @desc: draws all the boxes/nodes
    def drawAllBoxes(self):
        # loop through all the boxes
        for _, box in self.allBoxes.items():
            # if curr box is a wall then
            if box.wall:
                # draw wall with by passing True for fill
                self.drawRect(box.xPos, box.yPos, box.width, box.height, box.color, 1, True)
            # if curr box is not a wall then
            else:
                # draw wall with by passing False for fill
               self.drawRect(box.xPos, box.yPos, box.width, box.height, box.color, 1, False) 

        pg.display.flip()

    # @desc: draws all the boxes/nodes
    # @args: 
    # @xPos: the x position of the box to draw
    # @yPos: the y position of the box to draw
    # @width: the width of the box to draw
    # @height: the height of the box to draw
    # @color: the color of the box to draw
    # @borderThickness: border thickness of the box to draw
    # @fill: determines if the box should be filled with the specified color or not
    def drawRect(self, xPos, yPos, width, height, color, borderThickness, fill):
        # if fill is true or color is == to any of the specified colors then
        if fill or color == (217, 52, 52) or color == (136, 222, 126) or color == (69, 161, 222) or color == (81, 55, 230):
            # draw the box by filling it with the specified color
            pg.draw.rect(self.surface, color, pg.Rect(xPos, yPos, width, height))
        else:
            # draw the box with a border of the specified color without filling it
            pg.draw.rect(self.surface, color, pg.Rect(xPos, yPos, width, height), borderThickness)

    # @desc: check if the mouse is colliding with any of the boxes
    # @args: 
    # @mPosX: x position of the mouse
    # @mPosY: y position of the mouse
    def mouseBoxCollisionCheck(self, mPosX, mPosY):
        i=0 # determines the number of the box
        for _, box in self.allBoxes.items():
            # check for collision with the curr box
            if(
                mPosX > box.xPos and 
                mPosX < box.xPos + box.width and 
                mPosY > box.yPos and 
                mPosY < box.yPos + box.height
            ):
                # return the curr box along with its number
                return (box, i)

            i+=1

    # @desc: colors the boxes and turns them into walls when the mouse is being dragged over them
    # @args: 
    # @mPosX: x position of the mouse
    # @mPosY: y position of the mouse    
    def colorWalls(self, mPosX, mPosY): 
        # get the box with which mouse is currently colliding
        box = self.mouseBoxCollisionCheck(mPosX, mPosY)
        # if box is not None and the box is not the source or destination then
        if box != None and box[1] != self.source and box[1] != self.dest:
            # color the box black
            box[0].color = (0,0,0)
            # turn the box into a wall
            box[0].wall = True

    # @desc: used to zoom in or out
    # @args: 
    # @factor: zoom in or out factor i.e the amount
    def zoomInOrOut(self, factor):
        # represents the new x and y position of the box since its size will change due to the zoom in or out
        xPos = 0
        yPos = 0
        i=0 # used to set the xPos = 0 to account for the next row
        self.baseBoxSize += factor # increase the base size by the factor
        for _, box in self.allBoxes.items():
            # set new base size
            box.width = self.baseBoxSize
            box.height = self.baseBoxSize 
            # set new x and y positions
            box.xPos = xPos
            box.yPos = yPos
            # increment xPos by base size so that the next box will be displayed immediately after the previous one
            xPos += self.baseBoxSize
            # increment idx by one to represent the next box
            i+=1
            # if i == 65 then we have reached the end of the current row 
            if(i == 65):
                # set i and xPos to 0 since it is the start of a new row
                i=0
                xPos = 0 
                # increment yPos by the base size to display the boxes in the next row immediately after the previous one
                yPos += self.baseBoxSize 

        # fill window with the specified color
        self.surface.fill((255,255,255))

    # @desc: creates the graph
    def initGraph(self):
        # represents the number of the box/node
        i=0
        # loop through all the boxes
        for _, box in self.allBoxes.items():
            # if box/node hasn't been added then
            if self.graph.get(i) is None:
                # create a new key = to the number of the box/node in the dictionary with value = an array of the box/node neighbors 
                self.graph[i] = []

                # if xPos != 0 then box has a left neighbor
                if box.xPos != 0:
                    # add left neigbhor
                    self.graph[i].append(i-1)

                # if xPos != 1920 then box has a right neighbor
                if box.xPos != 1920:
                    # add right neighbor
                    self.graph[i].append(i+1)

                # if yPos != 0 then box has a top neighbor
                if box.yPos != 0:
                    # add top neighbor
                    self.graph[i].append(i-65)

                # if yPos != 1320 then box has a bottom neighbor
                if box.yPos != 1320:
                    # add bottom neighbor
                    self.graph[i].append(i+65)

            i+=1

    # @desc: used to select the source and destination nodes
    # @args: 
    # @mPosX: x position of the mouse
    # @mPosY: y position of the mouse 
    def selectSourceAndDest(self, mPosX, mPosY):
        # get the box and its number with which the mouse is colliding
        matchedBoxAndPositionTuple = self.mouseBoxCollisionCheck(mPosX, mPosY)
        # if there is a box with which the mouse is curretly colliding
        if matchedBoxAndPositionTuple != None:
                # extract the box and its number
                (box, i) = matchedBoxAndPositionTuple
                # if source node hasn't been selected yet and the box is not a wall then
                if self.source == -1 and self.dest == -1 and box.wall == False:
                    # set curr box as source
                    self.source = i
                    # change box color
                    box.color = (136, 222, 126)

                # if source and dest node hasn't been selected yet and the box is not a wall then
                elif self.source != -1 and self.dest == -1 and box.wall == False:
                    # set curr box as dest
                    self.dest = i
                    # change box color
                    box.color = (81, 55, 230)

    # @desc: finds the shortest path between the source and dest nodes
    # @args: 
    # @source: the source node
    # @dest: the destination node
    def findShortestPath(self, source, dest):
        queue = deque([source]) # create a queue for graph traversal
        visited = {source: True} # used to check if a node has been visited
        prev = None # stores the previous node to the curr node
        prevs = {} # stores all the previous nodes key=neighbour, value=currNode . Will be used to trace back path to the source from the dest
        prevs[source] = None # prev of source is none since nothing comes before it

        # if queue is not empty
        while(len(queue) > 0):
            
            node = queue.popleft() # pop leftmost element
            
            if node != source and node != dest: # if curr node is not source or dest then
                self.allBoxes[node].color = (78, 76, 199) # change color of the node

            if node == dest: # if we have reached the dest node then stop
                break
            
            # curr node will act as the previous node for all its children
            prev = node

            # loop through all the neighbours 
            for neighbour in self.graph[node]:
                # is curr neighbour hasn't been visited and curr neighbour is not a wall
                if visited.get(neighbour) is None and self.allBoxes[neighbour].wall == False:
                    # if curr neighbour is not == dest then
                    if neighbour != dest:
                        # change color
                        self.allBoxes[neighbour].color = (69, 161, 222)
                    # add curr neighbour to the queue
                    queue.append(neighbour)
                    # add the curr node as previous for the current neighbour
                    prevs[neighbour] = node
                    # add neighbour to the visited dictionary
                    visited[neighbour] = True

            self.surface.fill((255,255,255)) # fill window with specified colors
            self.drawAllBoxes() # redraw all the boxes

        # if dest node is present in prevs then the algo has found a path to it so
        if prevs.get(dest) is not None:
            path = self.generatePath(dest, prevs) # get the path
            self.hightlightPath(path, source, dest) # hightlight the path

        # if dest node is not present in prevs then the algo hasn't found a path to it so
        else:
            self.displayNoPathFoundMsg() # display no path found message
        
        # set completed = true since the alog finished
        self.completed = True

    # @desc: generates a path from the source to the destination
    # @args: 
    # @dest: the destinaion node
    # @prevs: the prevs dictionary
    def generatePath(self, dest, prevs):
        path = [dest] # create path array with dest alredy in it
        tr = dest # set tr = dest since we are tracing back from dest to source
        # loop until we reach the source
        while prevs[tr] != None:
            # get the previous of the current node
            tr = prevs[tr]
            # add curr node to the path
            path.append(tr)

        # return the path
        return path

    # @desc: highlights the generated path
    # @args: 
    # @path: the path array
    # @source: the source node
    # @dest: the destination node
    def hightlightPath(self, path, source, dest):
        # fill the window with specified color
        self.surface.fill((255,255,255))
        # loop through path array starting from the end
        for i in range(len(path)-1, -1, -1):
            # if path[i] is not source or dest then
            if path[i] != source and path[i] != dest:
                self.allBoxes[path[i]].color = (217, 52, 52) # color path[i]

            # draw all boxes
            self.drawAllBoxes()
            # wait for 15ms
            pg.time.wait(15)
        
    # @desc: displays no path found message
    def displayNoPathFoundMsg(self):
        # set font
        font = pg.font.SysFont("Arial", 70)
        # render a new surface
        textsurface=font.render('No path found', True, (255, 255, 255))
        # create new surface
        surface=pg.Surface(textsurface.get_size())
        # fill it with the specified color
        surface.fill((0, 0, 0))
        # blit the font surface to the new surface
        surface.blit(textsurface, pg.Rect(0, 0, 10, 10))
        # set alpha of the new surface to make it transparent
        surface.set_alpha(160)
        # blit the new surface on the original surface and position it in the middle
        self.surface.blit(surface, pg.Rect(650 - surface.get_size()[0]/2, 450 - surface.get_size()[1]/2, 10, 10))

    # @desc: reinits everything
    def reinitEverything(self):
        # set everything back to default
        self.source = -1
        self.dest = -1
        self.allBoxes = {}
        self.completed = False
        self.initBoxes(45,65)
        self.initGraph()
        self.surface.fill((255,255,255))

    # @desc: the main event loop
    def loop(self):
        # if running is true then
        while self.running:
            self.drawAllBoxes() # draw all boxes
            # loop throught the occured events
            for event in pg.event.get():
                if event.type == pg.QUIT: # if event type = Quit then
                    self.running = False # quit the app

                # if event type = key down and the downed key = left control then
                elif event.type == pg.KEYDOWN and event.key == pg.K_LCTRL:
                    # set sourceAndDestSelection = True because user is trying to select the source or destination by holding down control
                    self.sourceAndDestSelection = True

                # if event type = key up and the upped key = left control then
                elif event.type == pg.KEYUP and event.key == pg.K_LCTRL:
                    # set sourceAndDestSelection = False because user left the control button
                    self.sourceAndDestSelection = False

                # if sourceAndDestSelection = True and event type = MOUSEBUTTONDOWN and pressed mouse button is = left mouse button then
                elif self.sourceAndDestSelection and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    # get mosuse pos
                    (mPosX,mPosY) = pg.mouse.get_pos()
                    # if sourceAndDestSelection = True and user presses left mouse button then the user is trying to selec either the source or dest node so
                    self.selectSourceAndDest(mPosX, mPosY)

                # if user presses enter and the source and dest has been selected and completed = False then
                elif event.type == pg.KEYUP and event.key == pg.K_RETURN and self.source != -1 and self.dest != -1 and self.completed == False:
                    # find the shortest path between the source and dest
                    self.findShortestPath(self.source, self.dest)

                # if user pressed escape button then 
                elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                    self.reinitEverything() # reinit everything

                # if user presses left mouse button then
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    # set drag to true becuase user is trying to drag over the boxes
                    self.drag = True

                # if user leaves the left mouse button then
                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    # set drag to false because user has finished dragging
                    self.drag = False

                # if user moves the mousewheel then
                elif event.type == pg.MOUSEWHEEL:
                    # if mousewheel is rotated upwards and base size <= 56 then
                    if event.y > 0 and self.baseBoxSize <= 56:
                        self.zoomInOrOut(2) # zoom in
                    # if mousewheel is rotated downwards and base size > 20 then
                    elif event.y < 0 and self.baseBoxSize > 20:
                        self.zoomInOrOut(-2) # zoom out

                # if drag is true and completed is false then
                if self.drag and self.completed == False:
                    # get mouse pos
                    (mPosX,mPosY) = pg.mouse.get_pos()
                    # color boxes and turn them into walls
                    self.colorWalls(mPosX, mPosY)