# @desc: class for the box/node
# @author: Yahya

# the box class
class box:

    xPos = None # x position of the box
    yPos = None # y position of the box
    width = None # width position of the box
    height = None # height position of the box
    color = None # color position of the box
    wall = False # determines if the box is a wall

    # @desc: the constructor
    # @args: 
    # @xPos: x position of the box
    # @yPos: y position of the box
    # @width: width position of the box
    # @height: height position of the box
    # @color: color position of the box
    def __init__(self, xPos, yPos, width, height, color):
        # set the variables
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.color = color