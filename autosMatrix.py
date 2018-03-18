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
		elif matrix[i] == 5:
			sense.set_pixel(Spalte, Zeile, 255, 0, 0) # rot

# Ampel Funktion
def Ampel(Iterationszahl, Ampelvariable):
	# Zeitschaltuhr
	if Iterationszahl % 10 == 0:
		if matrix[32] == 4 and matrix[15] == 4: # Wenn die Hauptstraße grün hat
			# Hauptstraße
			matrix[34] = 1
			matrix[33] = 3
			matrix[32] = 1
			matrix[13] = 1
			matrix[14] = 3
			matrix[15] = 1

			# Nebenstraße
			matrix[37] = 1
			matrix[45] = 3
			matrix[53] = 1

			# Speichervariable für Ampelschaltung
			return 0

		elif matrix[34] == 2 and matrix[13] == 2: # Wenn die Hauptstraße rot hat
			# Hauptstraße
			matrix[34] = 1
			matrix[33] = 3
			matrix[32] = 1
			matrix[13] = 1
			matrix[14] = 3
			matrix[15] = 1

			# Nebenstraße
			matrix[37] = 1
			matrix[45] = 3
			matrix[53] = 1

			# Speichervariable für Ampelschaltung
			return 1

	# Wenn die Ampeln gelb sind
	elif matrix[33] == 3: 
		if Gelb == 0: # Wenn die Hauptstraße gelb hat und rot werden soll
			# Hauptstraße			
			matrix[34] = 2
			matrix[33] = 1
			matrix[32] = 1
			matrix[13] = 2
			matrix[14] = 1
			matrix[15] = 1

			# Nebenstraße
			matrix[37] = 1
			matrix[45] = 1
			matrix[53] = 4

		else: # Wenn die Hauptstraße gelb hat und grün werden soll
			# Hauptstraße
			matrix[34] = 1
			matrix[33] = 1
			matrix[32] = 4
			matrix[13] = 1
			matrix[14] = 1
			matrix[15] = 4

			# Nebenstraße
			matrix[37] = 2
			matrix[45] = 1
			matrix[53] = 1

	# Wenn zuviele Autos an der Nebenstraße anstehen
	elif matrix[36] == 2 and matrix[44] == 2 and matrix[52] == 2: 
		# Hauptstraße
		matrix[34] = 1
		matrix[33] = 3
		matrix[32] = 1
		matrix[13] = 1
		matrix[14] = 3
		matrix[15] = 1

		# Nebenstraße
		matrix[37] = 1
		matrix[45] = 3
		matrix[53] = 1

		# Speichervariable für Ampelschaltung
		return 0

	# Wenn zuviele Autos an der Hauptstraße anstehen (auf einer der beiden Seiten)
	elif (matrix[25] == 2 and matrix[26] == 2) or (matrix[21] == 2 and matrix[22] == 2):
		# Hauptstraße
		matrix[34] = 1
		matrix[33] = 3
		matrix[32] = 1
		matrix[13] = 1
		matrix[14] = 3
		matrix[15] = 1

		# Nebenstraße
		matrix[37] = 1
		matrix[45] = 3
		matrix[53] = 1

		# Speichervariable für Ampelschaltung
		return 1

# Update Funktion
def updateMatrix():

	# 1. Spur - Hauptstraße von rechts
	for i in range(16,24):
		if i == 16 and matrix[i] == 2: # Auto über den Rand fahren lassen
			matrix[i] = 0
		elif i == 21: # Kritischer Punkt für die Ampel
			if matrix[15] == 4 and matrix[i] == 2:
				matrix[i] = 0
				matrix[i-1] = 2
		elif matrix[i] == 2 and matrix[i-1] != 2: # wenn auf i ein Auto und der nächste Platz frei ist, fahren
			matrix[i] = 0
			matrix[i-1] = 2

	# 2. Spur - Hauptstraße von links
	for i in range(31,23,-1):
		if i == 31 and matrix[i] == 2: # Auto über den Rand fahren lassen
			matrix[i] = 0
		elif i == 26: # Kritischer Punkt für die Ampel
			if matrix[32] == 4 and matrix[i] == 2:
				matrix[i] = 0
				matrix[i+1] = 2
		elif matrix[i] == 2 and matrix[i+1] != 2: # wenn auf i ein Auto und der nächste Platz frei ist, fahren
			matrix[i] = 0
			matrix[i+1] = 2
		elif matrix[i] == 5 and matrix[i-8] != 5:
			matrix[i] = 0
			matrix[i-8] = 2

	# 3. Spur - Nebenstraßevon unten
	for i in range(36,68,8):
		if i == 36 and matrix[i] == 2 and matrix[53] == 4: # Auto ab der Ampel fahren lassen
			zz = rnd.randint(0,1)
			if zz == 0: # links abbiegen
				matrix[i] = 0
				matrix[i-8] = 5 # 5 als extra Fall für die Matrix
			else: # rechts abbiegen
				matrix[i] = 0
				matrix[i-8] = 2
		elif i != 36 and matrix[i] == 2 and matrix[i-8] != 2: # wenn auf i ein Auto und der nächste Platz frei ist, fahren
			matrix[i] = 0
			matrix[i-8] = 2

# Main
# Zufällige generierung von Autos
Iteration = 1
Gelb = 0
while True:
	time.sleep(1)
	updateMatrix()
	matrixToSensehat()
	zz = rnd.randint(0,3)
	time.sleep(0.3)
	if zz == 1: # Hauptstraße von links
		if matrix[25] != 2: # Abstandsbedingung von einem Bildpunkt
			matrix[24] = 2
	elif zz == 2: # Hauptstraße von rechts
		if matrix[22] != 2: # Abstandsbedingung von einem Bildpunkt
			matrix[23] = 2
	elif zz == 3: # Nebenstraße von unten
		if matrix[52] != 2: # Abstandsbedingung von einem Bildpunkt
			matrix[60] = 2
	matrixToSensehat()
	Gelb = Ampel(Iteration, Gelb)
	Iteration += 1
