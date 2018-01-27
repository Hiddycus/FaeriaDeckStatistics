import pygame
import math
import json
from pprint import pprint
# http://prntscr.com/i6e50j

height=200
width=400
BLUE =  (  0,   0, 255)
WHITE = (255, 255, 255)
BACK = (155, 155, 155)
RED =   (255,   0,   0)

margin = 10
nbins = 16

def DrawAxes(screen):
	pygame.draw.rect(screen, BLUE, [margin,margin,width-margin,height-margin ],2)
	
def DrawHist(screen, hist_c,hist_e):
	pygame.draw.rect(screen, BLUE, [margin,margin,width-margin,height-margin ],0)
	xstep = math.floor((width-2*margin)/nbins)
	ystep = math.floor((height-2*margin)/20)
	center = height/2
	idx = 0
	for v in hist_c:
		x = margin + xstep*idx
		y = -v*ystep
		pygame.draw.rect(screen, WHITE, [x,center,xstep-2,y ],0)
		idx += 1
	idx = 0
	for v in hist_e:
		x = margin + xstep*idx
		y = v*ystep
		pygame.draw.rect(screen, RED, [x,center,xstep-2,y ],0)
		idx += 1
	
def Lands(card):
	lands = card['deserts']+card['forests']+card['islands']+card['mountains']
	if card['wild'] != "":
		lands += int(card['wild'])
	return lands

def UpdateHist8( hist, val, n):
	idx = val	#math.floor(val/2)
	if idx > (nbins-1):
		idx = (nbins-1)
	hist[idx]+=n
	return hist
	
def CheckAllCards(all):
	sum=0
	for item in all:
		sum+=item['attack']
		
	print(sum)
	return sum
	
def LoadAllCards(file_name="cards.json"):
	#file_name="cards3.json"	
	json_data=open(file_name).read()
	data = json.loads(json_data)
	#pprint(data)
	#print(data[0]['id'])
	return data

def LoadInput(file_name="input.txt"):
	infile = open(file_name)
	decklines = []
	try:
		for line in infile:
			decklines.append(line.upper())
			#print line,
	finally:
		infile.close()
	return decklines

all=LoadAllCards("cards.json")
#decklines=LoadInput("input.txt")
decklines=LoadInput("input_ymhr.txt")
#print(decklines)
nfound = 0
#deck_ids = []
deck = []
amount = []
for cline in decklines:
	found = False
	for s in all:
		upname = s['name'].upper()
		if cline.find(upname) != -1:
			nfound += 1
			deck.append(s)
			#deck_ids.append(s['id'])
			sp = cline.split()
			n = int(sp[-1])
			amount.append(n)			
			break
#print(nfound)
#print(deck_ids)
#print(amount)
total_faeria = 0
total_flcost = 0
index=0
number=0
maxlands=0
flhist_c=[]
flhist_e=[]
for x in range(nbins):
	flhist_c.append(0)
	flhist_e.append(0)
	
for s in deck:
	n = amount[index]
	lands = Lands(s)
	if lands > maxlands:
		maxlands = lands
	fcost = s['faeriaCost']
	total_faeria += n*fcost
	fl = fcost+lands
	total_flcost += n*fl
	if s["type"]=="creature":
		flhist_c = UpdateHist8( flhist_c, fl, n)
	if s["type"]=="event":
		flhist_e = UpdateHist8( flhist_e, fl, n)
	number += n
	index+=1

if number != 30:
	print("warning! Only ", number," cards is readed")
average=total_faeria/number
print("maxlands", maxlands)
print("average faeria cost: ", average)
print("average fl cost: ", total_flcost/number)
print(flhist_c)
print(flhist_e)
	
# Initialize the game engine
pygame.init()
# Set the height and width of the screen
size = [420, 220]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Double FL histogramm Green Yellow Mobile Hard Ramp")
#http://prntscr.com/i6ewut
 
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
#hist_c = [0,2,8,3,0,0,3,0, 1,2,3,0, 0,0,0,0] 
#hist_e = [0,3,9,0,2,0,0,0, 1,2,3,0, 0,0,0,0]

while not done:
	# This limits the while loop to a max of 10 times per second.
	# Leave this out and we will use all CPU we can.
	clock.tick(10)
	
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop
			
	# All drawing code happens after the for loop and but
	# inside the main while done==False loop.
	# Clear the screen and set the screen background
	screen.fill(BACK)
	DrawHist(screen,flhist_c,flhist_e)

	pygame.display.flip()
	
# Be IDLE friendly
pygame.quit()		
