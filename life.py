from pygame import*
import random

#52x30

init()

BLACK = (0,0,0) 
WHITE = (255,255,255)
BLUE = (0,0,255)

size = width,height = 1092,630
screen = display.set_mode((size))
screen.fill(WHITE)


#Functions that draw vertical and horizontal lines
def vertical(x):
	draw.line(screen,BLACK,(x,0),(x,height))
def horizontal(y):
	draw.line(screen,BLACK,(0,y),(width,y))

xcoord = 0
ycoord = 21

for i in range (width//20):
	vertical(xcoord)
	xcoord += 21
for i in range (height//21):
	horizontal(ycoord)
	ycoord += 21
	
	
listrects = []
sublist = []
x,y = 1,1

for i in range (30):
	for j in range (52):
		sublist.append(Rect(x,y,20,20))
		x += 21
	listrects.append(sublist)
	sublist = []
	x = 1
	y += 21

liststates = []
statesublist = []

for i in range (30):
	for j in range (52):
		statesublist.append(False)
	liststates.append(statesublist)
	statesublist = []
	
def neighbours(i,j):
	neighbours = []
	
	if i == 0 and j == 0:
		neighbours.append(liststates[i][j+1])
		neighbours.append(liststates[i+1][j])
		neighbours.append(liststates[i+1][j+1])
	elif i == 0 and j == 51:
		neighbours.append(liststates[i][j-1])
		neighbours.append(liststates[i+1][j])
		neighbours.append(liststates[i+1][j-1])
	elif i == 29 and j == 0:
		neighbours.append(liststates[i][j+1])
		neighbours.append(liststates[i-1][j])
		neighbours.append(liststates[i-1][j+1])
	elif i == 29 and j == 51:
		neighbours.append(liststates[i][j-1])
		neighbours.append(liststates[i-1][j])
		neighbours.append(liststates[i-1][j-1])
	elif i == 0:
		neighbours.append(liststates[i][j-1])
		neighbours.append(liststates[i][j+1])
		neighbours.append(liststates[i+1][j])
		neighbours.append(liststates[i+1][j-1])
		neighbours.append(liststates[i+1][j+1])
	elif i == 29:
		neighbours.append(liststates[i][j-1])
		neighbours.append(liststates[i][j+1])
		neighbours.append(liststates[i-1][j])
		neighbours.append(liststates[i-1][j-1])
		neighbours.append(liststates[i-1][j+1])
	elif j == 0:
		neighbours.append(liststates[i][j+1])
		neighbours.append(liststates[i+1][j])
		neighbours.append(liststates[i+1][j+1])
		neighbours.append(liststates[i-1][j])
		neighbours.append(liststates[i-1][j+1])
	elif j == 51:
		neighbours.append(liststates[i-1][j])
		neighbours.append(liststates[i-1][j-1])
		neighbours.append(liststates[i][j-1])
		neighbours.append(liststates[i+1][j])
		neighbours.append(liststates[i+1][j-1])
	else:
		neighbours.append(liststates[i-1][j-1])
		neighbours.append(liststates[i-1][j])
		neighbours.append(liststates[i-1][j+1])
		neighbours.append(liststates[i][j-1])
		neighbours.append(liststates[i][j+1])
		neighbours.append(liststates[i+1][j-1])
		neighbours.append(liststates[i+1][j])
		neighbours.append(liststates[i+1][j+1])

	return neighbours
	
display.flip()

drawing = False
selecting = True
loop = False
birth = []
death = []


running = True
while running:
	for e in event.get():
		
		if e.type == QUIT:
			running = False
		if e.type == MOUSEBUTTONDOWN:
			drawing = True
			x,y = e.pos
		if e.type == MOUSEBUTTONUP:
			drawing = False
		try:
			if selecting and drawing:
				for i in range(30):
					for j in range (52):
						if listrects[i][j].collidepoint(e.pos):
							liststates[i][j] = True
							if liststates[i][j]:
								draw.rect(screen,BLACK,listrects[i][j])
								display.flip()
							else: 
								draw.rect(screen,WHITE,listrects[i][j])
								display.flip()
			if e.type == KEYDOWN and e.key == K_r:
				liststates = []
				statesublist = []

				for i in range (30):
					for j in range (52):
						num = random.randint(0,1)
						if num == 0:
							statesublist.append(False)
							draw.rect(screen,WHITE,listrects[i][j])
							display.flip()
						else: 
							statesublist.append(True)
							draw.rect(screen,BLACK,listrects[i][j])
							display.flip()
					liststates.append(statesublist)
					statesublist = []
			if e.type == KEYDOWN and e.key == K_SPACE:
				liststates = []
				statesublist = []
				for i in range (30):
					for j in range (52):
						statesublist.append(False)
						draw.rect(screen,WHITE,listrects[i][j])
						display.flip()
					liststates.append(statesublist)
					statesublist = []
								
			if e.type == KEYDOWN and e.key == K_RETURN:
				selecting = False
				loop = True
		except AttributeError:
			pass
	if loop:
		time.wait(100)
		for i in range(30):
			for j in range (52):
				if neighbours(i,j).count(True) == 3 and liststates[i][j] == False:
					birth.append([i,j])
				if neighbours(i,j).count(True) < 2 and liststates[i][j] == True:
					death.append([i,j])
				if neighbours(i,j).count(True) > 3 and liststates[i][j] == True:
					death.append([i,j])
				
		for i in birth:
			liststates[i[0]][i[1]] = True
			draw.rect(screen,BLACK,listrects[i[0]][i[1]])
			display.flip()
			birth = []
		
		for i in death:
			liststates[i[0]][i[1]] = False
			draw.rect(screen,WHITE,listrects[i[0]][i[1]])
			display.flip()
			death = []
			
		for e in event.get():
			if e.type == QUIT:
				running = False
		
quit()
