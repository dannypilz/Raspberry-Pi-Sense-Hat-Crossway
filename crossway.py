########################
#  Bibliotheken laden  #
########################

from sense_hat import SenseHat
from time import sleep
import threading, random

sense = SenseHat()
sense.clear()

###########################
#  Definition der Farben  #
###########################

O = [0, 0, 0] # aus
Y = [255,255,255] # weiß

r = [255,0,0] # rot
g = [255,255,0] # gelb
gr = [64,255,0] # grün

#########################################
#  Initialisierung Fahrbahn und Ampeln  #
#########################################

def start():
  
  ar1 = Y # da können wir doch auch gleich Y etc. in die matrx schreiben oder?
  age = Y
  ag1 = gr

  ar2 = r
  age2 = Y
  ag2 = Y

  init = [
  O, O, O, O, O, O, O, O,
  Y, Y, Y, Y, Y, ar1, age, ag1,
  O, O, O, O, O, O, O, O,
  O, O, O, O, O, O, O, O,
  ag1, age, ar1, O, O, ar2, Y, Y,
  O, O, Y, O, O, age2, O, O,
  O, O, Y, O, O, ag2, O, O,
  O, O, Y, O, O, Y, O, O
  ]

  sense.set_pixels(init)

###################
#  Ampel Klassen  #
###################

# Hauptstraße auf grün
def gruen():
  sense.set_pixel(0, 4, 64, 255, 0) # grün für Hauptstraße von links
  sense.set_pixel(2, 4, 255, 255, 255) # Hauptstraße rot ausstellen
  sense.set_pixel(7, 1, 64, 255, 0)  # grün für Hauptstraße von rechts
  sense.set_pixel(5, 1, 255, 255, 255) # Hauptstraße rot ausstellen
  sense.set_pixel(5, 4, 255, 0, 0) # rot für Nebenstraße
  sense.set_pixel(5, 6, 255, 255, 255) # Nebenstraße grün ausstellen

  # gelbe Ampeln ausschalten
  sense.set_pixel(1, 4, 255,255,255)
  sense.set_pixel(6, 1, 255, 255, 255)
  sense.set_pixel(5, 5, 255, 255, 255)
  
  return "gruen"

# Hauptstraße auf gelb
def gelb():
  sense.set_pixel(1, 4, 255,255,0) # gelb für Hauptsraße von links
  sense.set_pixel(0, 4, 255, 255, 255) # Hauptstraße grün ausstellen
  sense.set_pixel(6, 1, 255,255,0) # gelb für Hauptsraße von rechts
  sense.set_pixel(7, 1, 255, 255, 255) # Hauptstraße grün ausstellen
  sense.set_pixel(5, 5, 255,255,0) # gelb für Nebenstraße
  sense.set_pixel(5, 4, 255, 255, 255) # Nebenstraße rot ausstellen

  # Hauptstraße rote Ampeln
  sense.set_pixel(2, 4, 255, 255, 255)
  sense.set_pixel(5, 1, 255, 255, 255)

  # Nebenstraße grüne Ampel ausstellen
  sense.set_pixel(5, 6, 255, 255, 255)

  return "gelb"
  
# Hauptstraße auf rot
def rot():
  sense.set_pixel(2, 4, 255, 0, 0) # rot für Hauptsraße von links
  sense.set_pixel(1, 4, 255,255,255) # Hauptstraße gelb ausstellen
  sense.set_pixel(5, 1, 255, 0, 0)  # rot für Hauptsraße von rechts
  sense.set_pixel(6, 1, 255,255,255) # Hauptstraße gelb ausstellen
  sense.set_pixel(5, 6, 64, 255, 0) # grün für Nebenstraße
  sense.set_pixel(5, 5, 255,255,255) # Nebenstraße gelb ausstellen

  return "rot"

#####################
#  Ampel Durchlauf  #
#####################

def Ampel():
  sleep(2)
  gelb()
  sleep(1)
  rot()
  sleep(10)
  gelb()
  sleep(1)
  gruen()

#  Prüfe, wie viele Autos an Nebenstraße
def AmpelNS():
  while True:
    ns1 = sum(sense.get_pixel(4,4))
    sleep(0.3)
    ns2 = sum(sense.get_pixel(4,5))
    sleep(0.3)
    ns3 = sum(sense.get_pixel(4,6))
    sleep(0.3)
    ns4 = sum(sense.get_pixel(4,7))
    
    
    if ns1 and ns2 and ns3 and ns4 > 11: # Warum 11?
      Ampel()
      sleep(10) # Zeit zum Abfahren der 4 Autos

#########################
#  Autos fahren lassen  #
#########################

# Hauptstraße, von links
def carsl():
  for i in range (8):
    sense.set_pixel(i, 3, 255, 0, 0)
    sleep(0.2)
    sense.set_pixel(i,3, 0, 0, 0)
    
# Hauptstraße, von rechts
def carsr():
  for i in range (8):
    sense.set_pixel(7-i, 2, 255, 0, 0)
    sleep(0.2)
    sense.set_pixel(7-i, 2, 0, 0, 0)
    

# Nebenstraße, von unten nach rechts
def carsur():
  for i in range(4,8):  
    sense.set_pixel(i, 3, 255, 0, 0)
    sleep(0.3)
    sense.set_pixel(i, 3, 0, 0, 0)
    
      
   
# Nebenstraße, von unten nach links
def carsul():
  sense.set_pixel(4, 3, 255, 0, 0)
  sleep(0.3)
  sense.set_pixel(4, 3, 0, 0, 0)
  
  for j in range (5):  
    sense.set_pixel(4-j, 2, 255, 0, 0)
    sleep(0.3)
    sense.set_pixel(4-j, 2, 0, 0, 0)
    
###################
#  Autos löschen  #
###################

# Autos löschen, Ampel Nebenstraße
def carsuloesch():
  k = 0
  while k < 4:
    sense.set_pixel(4,7-k, 0, 0, 0)
    k += 1
    sleep(2)
    

# Multithread Ampel Nebenstraße links, rechts zufällig abbiegen, Autos löschen

def Cars_u():
  ul_r={}
  c = 0
  T2 = 0
  while T2 == 0:
    na4 = sum(sense.get_pixel(5,6)) # Nebenstraßenampel grün
    if na4 == 316:
      
      for y in range(4):
        sleep(2)
        random.seed()
        ulr = random.randint(1, 4)
        if ulr == 1 or ulr == 3:
          u_lr = carsur
        if ulr == 2 or ulr == 4:
          u_lr = carsul

        ul_r["string{0}".format(y)]=threading.Thread(target=u_lr)
        ul_r["string{0}".format(y)].start()
        print(ul_r["string{0}".format(y)])
    
        c += 1
        if c == 1:
          ul_r6 = threading.Thread(target=carsuloesch)
          ul_r6.start()
        else:
          continue
        T2 = 1
    else:
      continue
    
  
####################
#  Autos an Ampel  #
####################

# 4 Autos von unten + warten an Ampel
def carau():
  for j in range(4):
    random.seed()
    sl = random.randint(1, 4)
    for i in range(4):
      x = i - j
      if x < 0:
        continue
      else:
        sleep(0.2)
        sense.set_pixel(4 ,7-x, 255, 0, 0)
        

      x = (i - j)- 1
      if x <  0:
        continue
      else:
        sense.set_pixel(4, 7-x, 0, 0, 0)
        sleep(0.3)
    sleep(sl)

# 3 Autos von links + warten an Ampel
def caral():
  for j in range(3):
    sl = random.randint(1, 3)
    random.seed()
    for i in range(3):
      x = i - j
      if x < 0:
        continue
      else:
        sleep(0.3)
        sense.set_pixel(x, 3, 255, 0, 0)
        

      x = (i - j)- 1
      if x <  0:
        continue
      else:
        sense.set_pixel(x, 3, 0, 0, 0)
      
    sleep(sl)

# 3 Autos von rechts + warten an Ampel
def carar():
  for j in range(3):
    random.seed()
    sl = random.randint(1, 3)
    for i in range(3):
      x = i - j
      if x < 0:
        continue
      else:
        sleep(0.3)
        sense.set_pixel(7-x, 2, 255, 0, 0)
        
        
      x = (i - j)- 1
      if x <  0:

        continue
      else:
        sense.set_pixel(7-x , 2, 0, 0, 0)
      
    sleep(sl)
    
#########################
#  zufällige Szenarien  #
#########################

# obere Fahrbahn, zuf. Autos & Sleep, Multithreading
def oF():
  u={}
  x = 0
  while True:
    na1 = sum(sense.get_pixel(5,5)) # Nebenstraßenampel gelb
    na2 = sum(sense.get_pixel(5,6)) # Nebenstraßenampel grün
    
    if na1 == 500 or na2 == 316: # während des Umschaltens
      
      break
    else:
      random.seed()

      # zufälliges ziehen von Autos
      car_nr = random.randint(1, 4) 
      if car_nr == 1 or car_nr == 3:
        car = carsl
      elif car_nr == 2 or car_nr == 4:
        car = carsr
    
      random.seed()
      sl = random.randint(1, 2)

      u["string{0}".format(x)]=threading.Thread(target=car)
      u["string{0}".format(x)].start()
      sleep(sl)
      x += 1
      


#Autos halten zufällig an Ampel
def oH():
  T = 0
  while T == 0:
    na3 = sum(sense.get_pixel(5,6)) # Nebenstraßenampel grün
    if na3 == 316:
      h2 = threading.Thread(target=caral)
      h2.start()
      sleep(1)
      h3 = threading.Thread(target=carar)
      h3.start()
      T = 1
    else:
      continue
    
######################
###  Hauptprogramm  ##
######################

start()


# erstens()

f1 = threading.Thread(target=oF) # oben fahren
f1.start()
h1 = threading.Thread(target=carau) # unten füllen
h1.start()
a1 = threading.Thread(target=AmpelNS) # Ampel prüfen
a1.start()

# zweitens

b1 = threading.Thread(target=oH) # oben prüfen und füllen
b1.start()
f2 = threading.Thread(target=Cars_u) 
f2.start()


'''while True:
  erstens()
    oben fahren + unten fahren
    Nebenstraße füllen
    [08:28, 14.3.2018] Günna:     Nebenstraße prüfen
    zweitens() auslösen
  zweitens()
    rot schlaten
    Nebenstraße leeren
    oben + unten füllen
    drittens auslösen
  drittens()
    grün schalten
    von vorn beginnen'''
  


# Multithreading
# Staus an Ampel mit Abstand i > x für Schleife mit j'''
