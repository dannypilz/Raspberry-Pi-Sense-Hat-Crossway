#############
#  Importe  #
#############
from sense_hat import SenseHat
import time
import random as rnd

####################################
#  SenseHat Initialize + Clearing  #
####################################
sense = SenseHat()
sense.clear()

##################
#  Start-Matrix  #
##################
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

###########################################
#  Check Function For Matrix (with text)  #
###########################################
def matrixCheck():
	string = ""
	for i in range(64):
		if i % 8 == 0:
			string += "\n"
		string += str(matrix[i])
	print (string)

##################################
#  Duplicate Matrix To SenseHat  #
##################################
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
		elif matrix[i] == 6:
			sense.set_pixel(Spalte, Zeile, 255, 0, 0) # rot
		elif matrix[i] == 7:
			sense.set_pixel(Spalte, Zeile, 0, 0, 255) # blau

####################
#  Ampel Function  #
####################
def Ampel(Iterationszahl, Ampelvariable, CoolDown):
	# Zeitschaltuhr
	if Iterationszahl % 10 == 0 and CoolDown == 0:
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

			# Speichervariable für Ampelschaltung und Cooldown
			return [0,0]

		elif matrix[34] != 0 and matrix[13] != 0: # Wenn die Hauptstraße rot hat
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

			# Speichervariable für Ampelschaltung und Cooldown
			return [1,0]

	# Wenn die Ampeln gelb sind
	elif matrix[33] == 3: 
		if Ampelvariable == 0: # Wenn die Hauptstraße gelb hat und rot werden soll
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

			# Speichervariable für Ampelschaltung und Cooldown
			return [1,6]

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

			# Speichervariable für Ampelschaltung und Cooldown
			return [0,6]

	# Wenn zuviele Autos an der Nebenstraße anstehen, auf gelb schalten
	elif matrix[36] != 0 and matrix[44] != 0 and matrix[52] != 0 and CoolDown == 0: 
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

		# Speichervariable für Ampelschaltung und Cooldown
		return [0,0]

	# Wenn zuviele Autos an der Hauptstraße anstehen (auf einer der beiden Seiten)
	elif ((matrix[25] != 0 and matrix[26] != 0) or (matrix[21] != 0 and matrix[22] != 0)) and CoolDown == 0:
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

		# Speichervariable für Ampelschaltung und Cooldown
		return [1,0]
	else:
		# Speichervariable für Ampelschaltung und Cooldown (alte Werte zurückgeben)
		return [Ampelvariable, CoolDown]

#####################
#  Update Function  #
#####################
def updateMatrix():
	# Spurreihenfolge wichtig! Bei Spurwechsel kommt es sonst zum "doppel-update"
	# 4. Spur - Nebenstraße von oben
	for i in range(59,27,-8):
		if i == 59 and matrix[i] != 0: # Auto über den Rand fahren lassen
			matrix[i] = 0
		elif matrix[i] != 0 and matrix[i+8] == 0:
			matrix[i] = 0
			matrix[i+8] = 2

	# 2. Spur - Hauptstraße von links
	for i in range(31,23,-1):
		if i == 31 and matrix[i] != 0: # Auto über den Rand fahren lassen
			matrix[i] = 0
		elif i == 26: # Kritischer Punkt für die Ampel
			if matrix[32] == 4 and matrix[i] != 0 and matrix[i+1] == 0 and matrix[i+2] == 0: # nur fahren falls Punkt frei + Abstand einhalten
				matrix[i] = 0
				matrix[i+1] = 2
		elif i == 27 and matrix[i] == 2: # Kritischer Punkt für Abbieger in Nebenstraße
			zz = rnd.randint(1,100)
			if zz <= 10 and matrix[i+8] == 0: # in 10% der Fälle
				matrix[i] = 0
				matrix[i+8] = 2
			elif zz <= 10: # Wenn noch nicht frei, Auto als wartend speichern
				matrix[i] = 6
			elif matrix[i+1] == 0: # normal weiter fahren
				matrix[i] = 0
				matrix[i+1] = 2
		elif i == 27 and matrix[i] == 6 and matrix[i+8] == 0: # Abbieger in Nebenstraße
			matrix[i] = 0
			matrix[i+8] = 2
		elif matrix[i] != 0 and matrix[i+1] == 0: # wenn auf i ein Auto und der nächste Platz frei ist, fahren
			matrix[i] = 0
			matrix[i+1] = 2
		elif matrix[i] == 5 and matrix[i-8] != 5:
			matrix[i] = 0
			matrix[i-8] = 2

	# 1. Spur - Hauptstraße von rechts
	for i in range(16,24):
		if i == 16 and matrix[i] != 0: # Auto über den Rand fahren lassen
			matrix[i] = 0
		elif i == 21: # Kritischer Punkt für die Ampel
			if matrix[15] == 4 and matrix[i] != 0 and matrix[i-1] == 0 and matrix[i-2] == 0: # nur fahren falls Punkt frei + Abstand einhalten
				matrix[i] = 0
				matrix[i-1] = 2
		elif i == 19 and matrix[i] == 2: # Kritischer Punkt für Abbieger in Nebenstraße
			zz = rnd.randint(1,100)
			if zz <= 10: # in 10% der Fälle
				if matrix[27] == 0 and matrix[26] == 0 and matrix[35] == 0:
					matrix[i] = 0
					matrix[i+8] = 6
				else:
					matrix[i] = 6
			elif matrix[i-1] == 0: # normal weiter fahren
				matrix[i] = 0
				matrix[i-1] = 2
		elif i == 19 and matrix[i] == 6: # falls ein Auto zum abbiegen bereits wartet
			if matrix[27] == 0 and matrix[26] == 0 and matrix[35] == 0:
				matrix[i] = 0
				matrix[i+8] = 6
			elif matrix[27] == 0 and matrix[35] == 0 and matrix[34] == 2: # Hauptstraße rot hat und es frei ist darf er auch abbiegen
				matrix[i] = 0
				matrix[i+8] = 6
		elif i == 23 and matrix[i] == 7 and matrix[i-1] != 7: # Falls der erste Teil des LKWs bereits auf dem Feld ist
			matrix[i-1] = 7
		elif matrix[i] != 0 and matrix[i-1] == 0: # wenn auf i ein Auto und der nächste Platz frei ist, fahren
			matrix[i] = 0
			matrix[i-1] = 2

	# 3. Spur - Nebenstraßevon von unten
	for i in range(36,68,8):
		if i == 36 and matrix[i] != 0 and matrix[53] == 4 and matrix[i-8] == 0 and matrix[i-16] == 0 and matrix[i-8+1] == 0: # Auto ab der Ampel fahren lassen, wenn frei und Abstand eingehalten
			zz = rnd.randint(0,1)
			if zz == 0: # links abbiegen
				matrix[i] = 0
				matrix[i-8] = 5 # 5 als extra Fall für die Matrix
			else: # rechts abbiegen
				matrix[i] = 0
				matrix[i-8] = 2
		elif i != 36 and matrix[i] != 0 and matrix[i-8] == 0: # wenn auf i ein Auto und der nächste Platz frei ist, fahren
			matrix[i] = 0
			matrix[i-8] = 2

###########################################
#  Check Function For The Number Of Cars  #
###########################################
def laneCheck(lane):
	number = 0
	if lane == 1:
		for i in range(16,24):
			if matrix[i] != 0:
				number += 1
	elif lane != 0:
		for i in range(24,32):
			if matrix[i] != 0:
				number += 1
	return number

######################
#    Main Function   #
######################

# Variablen initialisierung
Iteration = 1
Gelb = 0
cd =  0

while True:
	# Ampel-CoolDown langsam senken
	if cd > 0:
		cd -= 1

	time.sleep(1)
	updateMatrix()
	
	# Matrix auf SenseHat spielen
	matrixToSensehat()

	# Zufällige generierung von Autos
	zz = rnd.randint(0,6)
	time.sleep(0.3)
	if zz == 1 and matrix[25] == 0: # Hauptstraße von links + Abstandsbedingung von einem Bildpunkt
		matrix[24] = 2
	elif zz == 2 and matrix[22] == 0: # Hauptstraße von rechts + Abstandsbedingung von einem Bildpunkt
		matrix[23] = 2
	elif zz == 3 and matrix[52] == 0: # Nebenstraße von unten + Abstandsbedingung von einem Bildpunkt
		matrix[60] = 2
	elif laneCheck(1) <= 1 and matrix[22] == 0: # wenn zu wenige Fahrzeuge von rechts unterwegs sind
		matrix[23] = 2
	elif laneCheck(2) <= 1 and matrix[25] == 0: # wenn zu wenige Fahrzeuge von links unterwegs sind
		matrix[24] = 2
	elif zz == 6 and matrix[25] != 2: # LKW von links auf die Hauptstraße
		matrix[24] = 7
	elif zz == 7 and matrix[22] != 2: # LKW von rechtss auf die Hauptstraße
		matrix[23] =  7
	elif zz == 8 and matrix[52] != 2: # LKW von unten auf die Nebenstraße
		matrix[60] = 7
	matrixToSensehat()

	# Updaten ob die Ampel von Gelb auf Grün oder auf Rot schalten muss
	Hilfsvektor = Ampel(Iteration, Gelb, cd)
	Gelb = Hilfsvektor[0]
	cd = Hilfsvektor[1]

	# Iterationzähler für Ampelschaltung nach Zeit
	Iteration += 1


# To Do:
# 	- LKW auftauchen lassen (2 Punkte sofort oder merken bis zur nächsten Iteration?)
#	- extra Zahl und Farbe für LKW (7, blau)
#	- LKW Bewegung ohne Abstand zu sich selbst
#	- "halb so schnell" nur in "Iteration % 2 == 0" LKW bewegen
#	- Wahrscheinlichkeiten prüfen
#	- Auffahren bis zur Ampel
