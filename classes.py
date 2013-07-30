"""Classes du jeu de Labyrinthe Donkey Kong"""
#-*- coding:utf8-*-
import pygame
from pygame.locals import * 
from constantes import *


class Niveau:
	"""Classe permettant de creer un niveau"""
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0
	
	
	def generer(self):
		"""Methode permettant de generer le niveau en fonction du fichier.
		On cree une liste generale, contenant une liste par ligne a afficher"""	
		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite a la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne a la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			self.structure = structure_niveau
	
	
	def afficher(self, fenetre):
		"""Methode permettant d'afficher le niveau en fonction 
		de la liste de structure renvoyee par generer()"""
		#Chargement des images (seule celle certaine contient de la transparence _alpha)
		mur = pygame.image.load(image_mur).convert()
		depart = pygame.image.load(image_depart).convert()
		arrivee = pygame.image.load(image_arrivee).convert_alpha()
		pique = pygame.image.load(image_pique).convert_alpha()
		tireur = pygame.image.load(image_tireur).convert_alpha()
		
		#On parcourt la liste du niveau
		num_ligne = 0
		temps = pygame.time.get_ticks()/100

		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position reelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite

				if sprite == '1':		   #m = Mur
					fenetre.blit(mur, (x,y))
				elif sprite == '3':		   #d = Depart
					fenetre.blit(depart, (x,y))
				elif sprite == '4':		   #a = Arrivee
					fenetre.blit(arrivee, (x,y))
				elif sprite == '5':		   #p = Pique [piege]
					fenetre.blit(pique, (x,y))
				elif sprite == '6':		   #6 = tireur 
					fenetre.blit(tireur, (x,y))
				num_case += 1
			num_ligne += 1

	




class Animation:

	"""Classe permettant de creer une annimation"""
	def __init__(self, droite, gauche, haut, bas, bouge):
		#Sprites du personnage
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = 0
		self.case_y = 0
		self.x = 0
		self.y = 0
		#Direction par defaut
		self.direction = self.droite
		self.bouge=bouge


	

	
	def deplacer(self, direction):
		"""Methode de deplacement"""
		#Deplacement vers la droite
		if direction == 'droite':
			#Pour ne pas depasser l'ecran
			if self.case_x < (len(self.niveau.structure[0]) - 1):
				#On verifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != '1' and self.niveau.structure[self.case_y][self.case_x+1] != '6'  :
					#Deplacement d'une case
					self.case_x += 1
					self.bouge=1
					#Calcul de la position "reelle" en pixel
					self.x = self.case_x * taille_sprite
				else:
					self.bouge=0
			else:
				self.bouge=0
			#Image dans la bonne direction
			self.direction = self.droite
		
		#Deplacement vers la gauche
		if direction == 'gauche':
			if self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != '1' and self.niveau.structure[self.case_y][self.case_x-1] != '6': 
					self.case_x -= 1
					self.bouge=1
					self.x = self.case_x * taille_sprite
				else:
					self.bouge=0
			else:
				self.bouge=0
			self.direction = self.gauche
		
		#Deplacement vers le haut
		if direction == 'haut':
			if self.case_y > 0:
				if self.niveau.structure[self.case_y-1][self.case_x] != '1' and self.niveau.structure[self.case_y-1][self.case_x] != '6':
					self.case_y -= 1
					self.bouge=1
					self.y = self.case_y * taille_sprite
				else:
					self.bouge=0
			else:
				self.bouge=0
			self.direction = self.haut
		
		#Deplacement vers le bas
		if direction == 'bas':
			if self.case_y < (len(self.niveau.structure) - 1):
				if self.niveau.structure[self.case_y+1][self.case_x] != '1' and self.niveau.structure[self.case_y+1][self.case_x] != '6':
					self.case_y += 1
					self.bouge=1
					self.y = self.case_y * taille_sprite
				else:
					self.bouge=0
			else:
				self.bouge=0
			self.direction = self.bas



class Perso(Animation):
	"""Classe permettant de creer son personnage principale"""

	def __init__(self, droite, gauche, haut, bas, bouge, niveau, etat):
		#Sprites du personnage
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = 0
		self.case_y = 0
		self.x = 0
		self.y = 0
		#Direction par defaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve 
		self.niveau = niveau
		#Vie par defaut
		self.etat = etat
		self.bouge= bouge

	def etat_vie(self, action):
		"""Methode permettant de savoir la vie personnage"""
		test_bouge=0	
		if self.etat < 6 or self.etat > 0:	
	
			#Perd une vie
			if action == 'pique':
				self.etat = self.etat - 1
				
			elif action == 'tire':
				self.etat = self.etat - 2
				

		if self.etat < 6:
			#Gagne une vie	
			if action == 'restaure':
				self.etat += 1
					
	def change(self, var_1, var_2):

		#faire haut gauche droite...
		
		self.case_x = var_2
		self.case_y = var_1

		self.x = self.case_x * taille_sprite
		self.y = self.case_y * taille_sprite	




class Objet(Animation):
	"""Classe permettant de creer les missiles"""

	
	def __init__(self, droite, gauche, haut, bas, niveau):

		#Sprites missille
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()

		#Position du missile en cases et en pixels
		self.case_x = 0
		self.case_y = 0
		self.x = 0
		self.y = 0
		
		#image par defaut
		self.direction = self.haut
		#Niveau dans lequel le personnage se trouve 
		self.niveau = niveau

		#variable pour bouger missile 3fois
		self.move = 0
		self.temps = pygame.time.get_ticks()/500 # temps...



	def __del__(self):
		pass
		

	def deplacer(self, direction):
		"""Methode de deplacement"""

		self.move = 1
		#Deplacement vers la droite
		if direction == 'droite':
			#Pour ne pas depasser l'ecran
			if self.case_x < (len(self.niveau.structure[0]) - 1):
				#On verifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != '1' and self.niveau.structure[self.case_y][self.case_x+1] != '6'  :
					#Deplacement d'une case
					if self.temps%4 == 1:
						self.case_x += 1
						self.bouge=1
						self.x = self.case_x * taille_sprite

					if self.temps%4 == 2:
						self.case_x += 2
						self.bouge=1
						self.x = self.case_x * taille_sprite

					if self.temps%4 == 3:
						self.case_x += 3
						self.bouge=1
						self.x = self.case_x * taille_sprite
					
					#Calcul de la position "reelle" en pixel
					self.x = self.case_x * taille_sprite
				else:
					self.bouge=0
			else:
				self.bouge=0
			#Image dans la bonne direction
			self.direction = self.droite
		
		#Deplacement vers la gauche
		if direction == 'gauche':
			if self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != '1' and self.niveau.structure[self.case_y][self.case_x-1] != '6': 
					
					if self.temps%4 == 1:
						self.case_x -= 1
						self.bouge=1
						self.x = self.case_x * taille_sprite

					if self.temps%4 == 2:
						self.case_x -= 2
						self.bouge=1
						self.x = self.case_x * taille_sprite

					if self.temps%4 == 3:
						self.case_x -= 3
						self.bouge=1
						self.x = self.case_x * taille_sprite

					self.move += 1		
				else:
					self.bouge=0
			else:
				self.bouge=0
			self.direction = self.gauche

			
			self.temps = pygame.time.get_ticks()/700 # temps...
	
			 
				
				
		
		


	def change(self, var_1, var_2):

		#faire haut gauche droite...
		
		self.case_x = var_2
		self.case_y = var_1

		self.x = self.case_x * taille_sprite
		self.y = self.case_y * taille_sprite
		



