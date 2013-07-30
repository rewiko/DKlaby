#!/usr/bin/python3
#-*- coding:utf8-*- 

"""
Jeu Donkey Kong Labyrinthe
Jeu dans lequel on doit deplacer DK jusqu'aux bananes a travers un labyrinthe.

Script Python
Fichiers : dklabyrinthe.py, classes.py, constantes.py, n1, n2 + images
"""

import pygame
from pygame.locals import *

from classes import *
from test_lab import *
from constantes import *
from random import *

pygame.init()

#Ouverture de la fenetre Pygame
fenetre = pygame.display.set_mode((l_fenetre,h_fenetre),RESIZABLE)
#Icone
icone = pygame.image.load(image_icone)
pygame.display.set_icon(icone)

#Titre
pygame.display.set_caption(titre_fenetre)

#Initialisation des sons
son_vie = pygame.mixer.Sound(son_vie)
son_pique = pygame.mixer.Sound(son_pique)
son_tire = pygame.mixer.Sound(son_tire)
son_perdu = pygame.mixer.Sound(son_perdu)
son_gagner = pygame.mixer.Sound(son_gagner)


#BOUCLE PRINCIPALE
continuer = 1
while continuer:	
	#Chargement et affichage de l'ecran d'accueil
	accueil = pygame.image.load(image_accueil).convert()
	fenetre.blit(accueil, (0,0))



	#Rafraichissement
	pygame.display.flip()

	#On remet ces variables a 1 a chaque tour de boucle
	continuer_jeu = 1
	continuer_accueil = 1
	nbrB0 = 0
	nbrB1 = 0
	nbrB2 = 0		
	genere=0
	#BOUCLE D'ACCUEIL
	while continuer_accueil:
	
		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(30)
	
		for event in pygame.event.get():
		
			#Si l'utilisateur quitte, on met les variables 
			#de boucle a 0 pour n'en parcourir aucune et fermer
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				continuer_accueil = 0
				continuer_jeu = 0
				continuer = 0
				#Variable de choix du niveau
				choix = 0
				
			elif event.type == KEYDOWN:				
				#Lancement du niveau 1
				if event.key == K_F1:
					continuer_accueil = 0	#On quitte l'accueil
					choix = 'n1'		#On definit le niveau a charge
			
				#Lancement du niveau 2
				elif event.key == K_F2:
					continuer_accueil = 0
					choix = 'n2'

				#Lancement du niveau 3
				elif event.key == K_F3:
					continuer_accueil = 0
					choix = 'n3'

				#Lancement du niveau 4
				elif event.key == K_F4:
					continuer_accueil = 0
					choix = 'n4'

				#Lancement du niveau 5
				elif event.key == K_F5:
					continuer_accueil = 0
					choix = 'n5'

				#Lancement du niveau 6
				elif event.key == K_F6:
					continuer_accueil = 0
					choix = 'n6'

				#Lancement du niveau 7
				elif event.key == K_F7:
					continuer_accueil = 0
					choix = 'n7'

				#Lancement du niveau 8
				elif event.key == K_F8:
					continuer_accueil = 0
					choix = 'n8'

				#Lancement du niveau 9
				elif event.key == K_F9:
					continuer_accueil = 0
					choix = 'n9'

				#Lancement du niveau 10
				elif event.key == K_F10:
					continuer_accueil = 0
					choix = 'n10'

				#Lancement générateur
				elif event.key == K_F12:
					continuer_accueil = 0
					choix = 'n11'
					genere=1
					n=int(15*random()+10)
					m=int(29*random()+10)
				
				elif event.key == K_a:
					continuer_accueil = 0
					choix = 'n11'
					genere=1
					n=15
					m=25
			
				elif event.key == K_z:
					continuer_accueil = 0
					choix = 'n11'
					genere=1
					n=20
					m=35
			
				elif event.key == K_e:
					continuer_accueil = 0
					choix = 'n11'
					genere=1
					n=25
					m=39

				elif event.key == K_q:
					continuer_accueil = 0
					continuer_jeu = 0
					continuer = 0
					choix = 0
					
				
				
		
	if genere==1:
		nb_test(n,m)
		initLaby()
		generelaby()
		genere_fichier("n11")

	#on verifie que le joueur a bien fait un choix de niveau
	#pour ne pas charger s'il quitte
	if choix != 0:
		#Chargement du fond
		fond = pygame.image.load(image_fond).convert()
		

		#Generation d'un niveau a partir d'un fichier
		niveau = Niveau(choix)
		niveau.generer()
		niveau.afficher(fenetre)


		#Creation de Personnage Principale
		dk = Perso("images/dk_droite.png", "images/dk_gauche.png", 
		"images/dk_haut.png", "images/dk_bas.png", 0, niveau, 6)
		#place dk sur la case départ numéroté 3
		for i in range(0,len(niveau.structure)):
			if niveau.structure[i][0]=="3":
				dk.change(i,0)
		
		fenetre = pygame.display.set_mode((len(niveau.structure[0])*taille_sprite,len(niveau.structure)*taille_sprite),RESIZABLE)			
	

	#BOUCLE DE JEU

	pygame.key.set_repeat(100, 50) #Pour effet appui long
		
	while continuer_jeu:
		
		temps = pygame.time.get_ticks()/500 # temps...
		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(30)
	
		for event in pygame.event.get():
		
			#Si l'utilisateur quitte, on met la variable qui continue le jeu
			#ET la variable generale a 0 pour fermer la fenetre
			if event.type == QUIT:
				continuer_jeu = 0
				continuer = 0
				fenetre = pygame.display.set_mode((l_fenetre,h_fenetre),RESIZABLE)
			elif event.type == KEYDOWN:
				#Si l'utilisateur presse Echap ici, on revient seulement au menu
				if event.key == K_ESCAPE:
					continuer_jeu = 0
					fenetre = pygame.display.set_mode((l_fenetre,h_fenetre),RESIZABLE)
				#Touches de deplacement de Donkey Kong
				elif event.key == K_RIGHT:
					dk.deplacer('droite')
					if dk.bouge==1:
						test_bouge=1
				elif event.key == K_LEFT:
					dk.deplacer('gauche')
					if dk.bouge==1:
						test_bouge=1
				elif event.key == K_UP:
					dk.deplacer('haut')
					if dk.bouge==1:
						test_bouge=1
				elif event.key == K_DOWN:
					dk.deplacer('bas')
					if dk.bouge==1:
						test_bouge=1
				#Lancement sauvegarde niveau 
				elif event.key == K_F1 and choix=='n11': 
					genere_fichier('n1')
				elif event.key == K_F2 and choix=='n11':
					genere_fichier('n2')
				elif event.key == K_F3 and choix=='n11':
					genere_fichier('n3') 
				elif event.key == K_F4 and choix=='n11':
					genere_fichier('n4')
				elif event.key == K_F5 and choix=='n11':
					genere_fichier('n5')
				elif event.key == K_F6 and choix=='n11':
					genere_fichier('n6')
				elif event.key == K_F7 and choix=='n11':
					genere_fichier('n7')
				elif event.key == K_F8 and choix=='n11':
					genere_fichier('n8')
				elif event.key == K_F9 and choix=='n11':
					genere_fichier('n9')
				elif event.key == K_F10 and choix=='n11':
					genere_fichier('n10')
			
		#Affichages aux nouvelles positions
		fenetre.blit(fond, (0,0))
		niveau.afficher(fenetre)
		fenetre.blit(dk.direction, (dk.x, dk.y)) #dk.direction = l'image dans la bonne direction
	
		q=0 # variable pour l'objet Missile (Z0, Z1, Z2,...)
		
		# Parcours du labyrinthe pour trouver les missile et les banane a placer.
		for i in range(0,len(niveau.structure)):
			for j in range(0,len(niveau.structure[0])):

				if niveau.structure[i][j]=='6':
					#Mi="M"+str(q) ne sert à rien !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				
					Mi = Objet("images/missile_gauche.png", "images/missile_gauche.png", "images/missile_gauche.png", "images/missile_gauche.png", niveau)
					Mi.change(i, j)
									
					Mi.deplacer('gauche')
					
					
														
						
					if ((dk.case_y == Mi.case_y) and (dk.case_x == Mi.case_x))and niveau.structure[dk.case_y][dk.case_x]=='7' and test_bouge==1:
						dk.etat_vie("tire")		#Chargement des sons
						son_tire.play()
						test_bouge=0							
	
										
					fenetre.blit(Mi.direction, (Mi.x, Mi.y))	
					q+=1



		### Objets [BANANE] ###

				if niveau.structure[i][j]=='a':
					
					if nbrB0 != 1:		
						B0 = Objet("images/banane.png", "images/banane.png", 
						"images/banane.png","images/banane.png", niveau)
						B0.change(i, j)
						fenetre.blit(B0.direction, (B0.x, B0.y))
						
						if ((dk.case_y == B0.case_y) and (dk.case_x == B0.case_x) and dk.etat!=6):
							pygame.time.wait(100)
							dk.etat_vie("restaure")
							son_vie.play()
							del(B0)
							nbrB0 = 1

				
				if niveau.structure[i][j]=='b':

					if nbrB1 != 1:
						B1 = Objet("images/banane.png", "images/banane.png", 
						"images/banane.png","images/banane.png", niveau)
						B1.change(i, j)
						fenetre.blit(B1.direction, (B1.x, B1.y))
					
						if ((dk.case_y == B1.case_y) and (dk.case_x == B1.case_x) and dk.etat!=6 ):
							pygame.time.wait(100)
							dk.etat_vie("restaure")
							son_vie.play()
							del(B1)
							nbrB1 = 1

				
						


				if niveau.structure[i][j]=='c':
			
					if nbrB2 != 1:
						B2 = Objet("images/banane.png", "images/banane.png", 
						"images/banane.png","images/banane.png", niveau)
						B2.change(i, j)
						fenetre.blit(B2.direction, (B2.x, B2.y))
							
						if ((dk.case_y == B2.case_y) and (dk.case_x == B2.case_x)and dk.etat!=6):
							pygame.time.wait(100)
							dk.etat_vie("restaure")
							son_vie.play()
							del(B2)
							nbrB2 = 1				

		
		if dk.etat==1:
			vie = pygame.image.load(image_vie1).convert()
		elif dk.etat==2:
			vie = pygame.image.load(image_vie2).convert()
		elif dk.etat==3:
			vie = pygame.image.load(image_vie3).convert()
		elif dk.etat==4:
			vie = pygame.image.load(image_vie4).convert()
		elif dk.etat==5:
			vie = pygame.image.load(image_vie5).convert()
		elif dk.etat==6:
			vie = pygame.image.load(image_vie6).convert()
		fenetre.blit(vie, ((len(niveau.structure[0])*taille_sprite)-(taille_sprite),0))
		pygame.display.flip()				


		#Personnage tomber sur piège
		if dk.etat < 7 and dk.etat > 0:
			if niveau.structure[dk.case_y][dk.case_x] == '5':
				pygame.time.wait(500)
				dk.etat_vie("pique")
				son_pique.play()
		
		elif dk.etat == 0:
			continuer_jeu = 0
		

		#Victoire -> Retour a l'accueil
		if niveau.structure[dk.case_y][dk.case_x] == '4':
			fin_niveau = pygame.image.load(image_fin_niveau).convert()
			fenetre = pygame.display.set_mode((l_fenetre,h_fenetre),RESIZABLE)
			fenetre.blit(fin_niveau,(0,0))
			son_gagner.play()
			pygame.display.flip()
			pygame.time.wait(3000)
			continuer_jeu = 0
			fenetre = pygame.display.set_mode((l_fenetre,h_fenetre),RESIZABLE)



		#Game Over -> Retour a l'accueil
		elif dk.etat <= 0:
			fin_perdu = pygame.image.load(image_fin_perdu).convert()
			fenetre = pygame.display.set_mode((l_fenetre,h_fenetre),RESIZABLE)
			fenetre.blit(fin_perdu,(0,0))
			son_perdu.play()
			pygame.display.flip()
			pygame.time.wait(3000)
			continuer_jeu = 0
			fenetre = pygame.display.set_mode((l_fenetre,h_fenetre),RESIZABLE)

