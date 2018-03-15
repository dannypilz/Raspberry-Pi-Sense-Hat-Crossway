# Importe
from sense_hat import SenseHat
import time
import random as rnd

#SenseHat initialisieren + reinigen
sense = SenseHat()
sense.clear()

# Pixel in Matrixnummer konvertieren
def konverter(x,y):
	a = x + y * 8
	return a

# Startmatrix
matrix = [
0 ,0 ,0 ,0 ,0 ,0 ,0 ,0,
1 ,1 ,1 ,1 ,1 ,1 ,1 ,4,
0 ,0 ,0 ,0 ,0 ,0 ,0 ,0,
0 ,0 ,0 ,0 ,0 ,0 ,0 ,0,
4 ,1 ,1 ,0 ,0 ,2 ,1 ,1,
0 ,0 ,1 ,0 ,0 ,1 ,0 ,0,
0 ,0 ,1 ,0 ,0 ,1 ,0 ,0,
0 ,0 ,1 ,0 ,0 ,1 ,0 ,0
]

# mittels Textausgabe die Matrix checken
def matrixCheck():
	string = ""
	for i in range(64):
		if i % 8 == 0:
			string += "\n"
		string += str(matrix[i])
	print (string)

# Matrix auf SenseHat duplizieren
def matrixToSensehat():
	for i in range(64):

		# Zeile bestimmen
		if i < 8:
			Zeile = 0
		elif i >= 8 and i <= 15:
			Zeile = 1
		elif i >= 16 and i <= 23:
			Zeile = 2
		elif i >= 24 and i <= 31:
			Zeile = 3
		elif i >= 32 and i <= 39:
			Zeile = 4
		elif i >= 40 and i <= 47:
			Zeile = 5
		elif i >= 48 and i <= 55:
			Zeile = 6
		elif i >= 56 and i <= 63:
			Zeile = 7
		
		# Spalte berechnen
		Spalte = i - Zeile * 8

		# Pixel umfärben
		if matrix[i] == 0:
			sense.set_pixel(Spalte, Zeile, 0, 0, 0) # aus
		elif matrix[i] == 1:
			sense.set_pixel(Spalte, Zeile, 255, 255, 255) # weiß
		elif matrix[i] == 2:
			sense.set_pixel(Spalte, Zeile, 255, 0, 0) # rot
		elif matrix[i] == 3:
			sense.set_pixel(Spalte, Zeile, 255, 255, 0) # gelb
		elif matrix[i] == 4:
			sense.set_pixel(Spalte, Zeile, 64, 255, 0) # grün

# Update Funktion
def updateMatrix():

	# 1. Spur - Hauptstraße von rechts
	for i in range(16,24):
		if i == 16 and matrix[i] == 2: #????
			matrix[i] = 0
		elif matrix[i] == 2:
			matrix[i] = 0
			matrix[i-1] = 2

	# 2. Spur - Hauptstraße von links
	for i in range(31,23,-1):
		if i == 31 and matrix[i] == 2:
			matrix[i] = 0
		elif matrix[i] == 2:
			matrix[i] = 0
			matrix[i+1] = 2

	# 3. Spur - Nebenstraßevon unten
	for i in range(36,68,8):
		if 

# Main
# Zufällige generierung von Autos
while True:
	time.sleep(1)
	updateMatrix()
	matrixToSensehat()
	zz = rnd.randint(0,3)
	time.sleep(0.3)
	if zz == 1:
		matrix[24] = 2
	elif zz == 2:
		matrix[23] = 2
	elif zz == 3:
		matrix[60] = 2
	matrixToSensehat()
