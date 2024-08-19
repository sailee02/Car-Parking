import turtle

Draw = turtle.Turtle()
Draw._tracer(0)
Draw.speed(0)
Draw.color("#000000")
topLeft_x=-150
topLeft_y=150
colors = ["#DDDDDD","#888888","red","yellow","blue","green","orange","magenta","purple","brown","darkgreen","gold","skyblue","darkred","turquoise","cyan","navy","lightgreen"]

#car(length, row, column, isHorizontal, colour)
cars = []
cars.append([2,3,2,True,2]) #Red Car
cars.append([3,1,4,False,3]) #Yellow Car
cars.append([3,2,5,False,4]) #Blue Car
cars.append([2,1,1,True,5]) #Green Car
cars.append([2,1,6,False,6]) #Orange Car
cars.append([2,5,1,False,7]) #Magenta Car
cars.append([3,2,1,False,8]) #Purple Car
cars.append([2,3,6,False,9]) #Brown Car
cars.append([3,4,2,True,17]) #Dark Green Car
cars.append([2,5,5,True,16]) #Gold Car
cars.append([2,6,5,True,12]) #Cyan Car

def drawGrid(width):
  for i in range(0,8):
    Draw.penup()
    Draw.goto(topLeft_x,topLeft_y-i*width)
    Draw.pendown()
    Draw.goto(topLeft_x+8*width,topLeft_y-i*width)
  for i in range(0,8):
    Draw.penup()
    Draw.goto(topLeft_x+i*width,topLeft_y)
    Draw.pendown()
    Draw.goto(topLeft_x+i*width,topLeft_y-8*width)
  for i in range(0,8):
    Draw.penup()
    Draw.goto(topLeft_x+i*width+10,topLeft_y+10)
    Draw.write(chr(65+i))
  for i in range(0,8):
    Draw.penup()
    Draw.goto(topLeft_x-15,topLeft_y-i*width+10-width)
    Draw.write(str(i))

  Draw.setheading(0)
  Draw.goto(topLeft_x,topLeft_y-width)
  for row in range (0,8):
      for column in range (0,8):
        if grid[row][column]>=0:
          square(width,grid[row][column])
        elif grid[row][column]==-1:
          square(width,0)
     
        Draw.penup()
        Draw.forward(width)
        Draw.pendown()
      Draw.setheading(270)
      Draw.penup()
      Draw.forward(width)
      Draw.setheading(180)
      Draw.forward(width*8)
      Draw.setheading(0)
      Draw.pendown()

#This function draws a box
def square(width,index):
    Draw.fillcolor(colors[index])
    Draw.begin_fill()
    for i in range(0,4):
      Draw.forward(width)
      Draw.left(90)
    Draw.end_fill()
    Draw.setheading(0)


#To check if it is solved
def checkGrid(grid):
 if grid[3][6]==2:
    return True
 else:
    return False

grid=[]
grid    =  [[1,1,1,1,1,1,1,1]]
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,0,0,0,0,0,0,-1])
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,1,1,1,1,1,1,1])  
index=2
for car in cars:
  if car[3]==True:
    for i in range(0,car[0]):
      grid[car[1]][car[2]+i]=car[4]
  else:
    for i in range(0,car[0]):
      grid[car[1]+i][car[2]]=car[4]
  index+=1
drawGrid(30) #30 is the width of each square
Draw.getscreen().update()  

def stampGrid(grid):
  stamp = ""
  for row in range (1,7):
    for column in range (1,7):
      stamp = stamp + str(grid[row][column])
  return stamp
 
#If repeated moves are there, there is no need to reinvestigate this position
history = []

def sendToFront(cars, color):
  index = 0
  for car in cars:
    if car[4]==color:
      cars.insert(0, cars.pop(index))
      break  
    index+=1
   
def sendToBack(cars, color):
  index = 0
  for car in cars:
    if car[4]==color:
      cars.append(cars.pop(index))
      break    
    index+=1
 
def applyHeuristics(grid,cars):
  #Priority 3 (Low): Vertical Cars in the way
  for car in cars:
    if car[3]==False and grid[3][car[2]]==car[4]:
      sendToFront(cars,car[4])

  #Priority 2 (Medium): Horizontal Cars that can move to the left  
  for car in cars:
    if car[3]==True and car[4]!=2:
      if grid[car[1]][car[2]-1]==0:
        sendToFront(cars,car[4])
      else:  
        sendToBack(cars,car[4])

  #Priority 1 (High): Red car if it can move to the right  
  if (grid[3][2]==2 and grid[3][3]==0) or (grid[3][3]==2 and grid[3][4]==0) or (grid[3][4]==2 and grid[3][5]==0) or (grid[3][5]==2 and grid[3][6]==0):
    sendToFront(cars,2)
  else:
    sendToBack(cars,2)
   
#Backtracking function to check all possible positions for all pieces
def moveCars(grid,cars):
    stamp = stampGrid(grid)
    if stamp in history:
      return False
    else:
      history.append(stamp)
     
    applyHeuristics(grid,cars)
    for car in cars:
        color = grid[car[1]][car[2]]
        if car[3]==True: #horizontal car
          if color==2: #Red Car
            if grid[car[1]][car[2]+car[0]]==0:
              #Move right?
              grid[car[1]][car[2]+car[0]]=color
              grid[car[1]][car[2]]=0
              car[2]+=1
              if moveCars(grid,cars)==True:
                return True
             
              #Backtrack
              car[2]-=1
              grid[car[1]][car[2]]=color
              grid[car[1]][car[2]+car[0]]=0
             
            if grid[car[1]][car[2]-1]==0:
              #Move left?
              grid[car[1]][car[2]+car[0]-1]=0
              grid[car[1]][car[2]-1]=color
              car[2]-=1
              if moveCars(grid,cars)==True:
                return True
              #Backtrack
              car[2]+=1
              grid[car[1]][car[2]+car[0]-1]=color
              grid[car[1]][car[2]-1]=0
          else: #All other horizontal cars
            if grid[car[1]][car[2]-1]==0:
              #Move left?
              grid[car[1]][car[2]+car[0]-1]=0
              grid[car[1]][car[2]-1]=color
              car[2]-=1
              if moveCars(grid,cars)==True:
                return True
              #Backtrack
              car[2]+=1
              grid[car[1]][car[2]+car[0]-1]=color
              grid[car[1]][car[2]-1]=0
             
            if grid[car[1]][car[2]+car[0]]==0:
              #Move right?
              grid[car[1]][car[2]]=0
              grid[car[1]][car[2]+car[0]]=color
              car[2]+=1
              if moveCars(grid,cars)==True:
                return True
             
              #Backtrack
              car[2]-=1
              grid[car[1]][car[2]]=color
              grid[car[1]][car[2]+car[0]]=0  
           
        else: #Vertical cars
          if car[0]==3: #Trucks
            if grid[car[1]+car[0]][car[2]]==0:
              #Move down?
              grid[car[1]][car[2]]=0
              grid[car[1]+car[0]][car[2]]=color
              car[1]+=1
              if moveCars(grid,cars)==True:
                return True
              #Backtrack              
              car[1]-=1
              grid[car[1]][car[2]]=color
              grid[car[1]+car[0]][car[2]]=0
             
            if grid[car[1]-1][car[2]]==0:
              #Move up?
              grid[car[1]+car[0]-1][car[2]]=0
              grid[car[1]-1][car[2]]=color
              car[1]-=1
              if moveCars(grid,cars)==True:
                return True  
              #Backtrack              
              car[1]+=1
              grid[car[1]+car[0]-1][car[2]]=color
              grid[car[1]-1][car[2]]=0
          else:
            if grid[car[1]-1][car[2]]==0:#Cars
              #Move up?
              grid[car[1]+car[0]-1][car[2]]=0
              grid[car[1]-1][car[2]]=color
              car[1]-=1
              if moveCars(grid,cars)==True:
                return True  
              #Backtrack              
              car[1]+=1
              grid[car[1]+car[0]-1][car[2]]=color
              grid[car[1]-1][car[2]]=0
           
            if grid[car[1]+car[0]][car[2]]==0:
              #Move down?
              grid[car[1]][car[2]]=0
              grid[car[1]+car[0]][car[2]]=color
              car[1]+=1
              if moveCars(grid,cars)==True:
                return True
              #Backtrack              
              car[1]-=1
              grid[car[1]][car[2]]=color
              grid[car[1]+car[0]][car[2]]=0
           
        drawGrid(30)
        Draw.getscreen().update()  
        if checkGrid(grid):
          grid[3][5]=0
          grid[3][7]=2
          drawGrid(30)
          Draw.getscreen().update()
          print("We have a solution!")
          return True
    return False
 
if moveCars(grid,cars):
  print("Problem Solved!")
else:
    print("This problem cannot be solved!")