#-*-coding:utf8-*-
from random import *



def nb_test(n,m):
	global N
	N=n
	global M
	M=m
	global lab
	lab=N*[0]

def initLaby():
	#coordonnées entrée du labyrinthe
	Ei=int((N-2)*random()+1)
	Ej=0
	#coordonnées sortie du labyrinthe
	Si=int((N-2)*random()+1)
	Sj=M-1
	
	#creation 
	for i in range(len(lab)):	
		lab[i] = M*[0]
	for i in range(N):
		for j in range(M):
			if((i==0 or i==(N-1) or j==0 or j==(M-1)) and (i!= Ei or j!= Ej) and (i!= Si or j!= Sj)):
				lab[i][j]=1
			elif i==Ei and j==Ej:
				lab[i][j]=3
			elif  i==Si and j==Sj:
				lab[i][j]=4
			else:
				lab[i][j]=0
		
def est_constructible(i,j):
	if(
	(lab[i][j] !=1) and
	# la case n'est pas au bord
	(i > 0 and i < N - 1 and j > 0 and j < M - 1) and
	( # la case à droite est un mur ?
	( lab[i][j+1] == 1  and lab[i-1][j] != 1 and
	lab[i-1][j-1] != 1 and lab[i][j-1] != 1 and
	lab[i+1][j-1] != 1 and lab[i+1][j] != 1 ) or
	# la case au dessus est un mur ?
	( lab[i-1][j] == 1 and lab[i][j-1] != 1 and
	lab[i+1][j-1] != 1 and lab[i+1][j] != 1 and
	lab[i+1][j+1] != 1 and lab[i][j+1] != 1	)or 
	# la case à gauche est un mur ?
	( lab[i][j-1] == 1 and lab[i+1][j] != 1 and
	lab[i+1][j+1] != 1 and lab[i][j+1] != 1 and
	lab[i-1][j+1] != 1 and lab[i-1][j] != 1 ) or
	# la case au dessous est un mur ?
	( lab[i+1][j] == 1 and lab[i][j+1] != 1 and
	lab[i-1][j+1] != 1 and lab[i-1][j] != 1 and 
	lab[i-1][j-1] != 1 and lab[i][j-1] != 1 ) )):
		return True
	else:
		return False

def marque_constructible():
	nbconstr=0
	for i in range(1,N-1):
		for j in range(1,M-1):
			if(est_constructible(i,j) is True ):
				lab[i][j]=9
				nbconstr+=1
				
	return nbconstr


def generelaby():

	banane_a=0
	banane_b=0
	banane_c=0

	nbconstr=marque_constructible()
	while nbconstr > 0:
		#choisit une case de maniere aléatoire parmi les cases constructibles
		x=int(nbconstr*random()+1)
		for i in range(1,N):
			for j in range(1,M):
				if lab[i][j]==9:
					x-=1
				if x==0:
					break
			if x==0:
				break
		#construit un mur dans cette case
		lab[i][j]=1
		nbconstr-=1
		#met à jour les huits cases autour
		
		for l in range(i-1,i+2):
			for k in range(j-1,j+2):
				if(lab[l][k]==9 and (est_constructible(l,k)is not True)):
					lab[l][k]=0
					nbconstr-=1
				elif(lab[l][k]==0 and (est_constructible(l,k)is True)):
					lab[l][k]=9
					nbconstr+=1

			
### Génération pour les Bananes (au maximum 1 bananes par tiers de map) ###

	# premier tier de la map
	for i in range(1,N/3):
		for j in range(1,M-1):		
			if lab[i][j]==0 and lab[i][j+1]==0 and lab[i][j-1]==0 and lab[i+1][j]==0 and lab[i-1][j]==0:
				if banane_a == 0: 
					lab[i][j]= "a"	
					banane_a = 1

				
	# deuxieme tier de la map			
	for i in range(N/3,(N/3)*2):
		for j in range(1,M-1):		
			if lab[i][j]==0 and lab[i][j+1]==0 and lab[i][j-1]==0 and lab[i+1][j]==0 and lab[i-1][j]==0:
				if banane_b == 0: 
					lab[i][j]= "b"
					banane_b = 1


	# dernier tier de la map
	for i in range((N/3)*2, N-1):
		for j in range(1,M-1):	
			if lab[i][j]==0 and lab[i][j+1]==0 and lab[i][j-1]==0 and lab[i+1][j]==0 and lab[i-1][j]==0: 
				if banane_c == 0: 
					lab[i][j]= "c"
					banane_c = 1
									

def genere_fichier(fichier):


	for i in range(1,N-1):
		if lab[i][0]==3:
			lab[i][1]=3
		if lab[i][M-1]==4:
			lab[i][M-2]=4
		
		
	for i in range(1,N-1):
		for j in range(1,M-1):

			### Génération pour les pièges [MISSILE]
			if lab[i][j]==0 and lab[i][j+1]==0 and lab[i][j+2]==0 and lab[i][j+3]==0 and lab[i][j+4] == 1:
				lab[i][j+4]=6
				lab[i][j+3]=7
				lab[i][j+2]=7
				lab[i][j+1]=7
			
			### Génération pour les pièges [PIQUE]
			if lab[i][j+1]==0 and lab[i][j-1]==0 and lab[i-1][j]==0 and lab[i-1][j-1]==0 and lab[i-1][j+1]==0:
				lab[i][j]=5
				
					
	with open(fichier,"w") as fichier:
		text=''
		for j in range(1,M-1):
			text=text+str(1)
		fichier.write(text)
		fichier.write('\n')
		for i in range(1,N-1):
			text='' 
			for j in range(1,M-1): 
				text=text+str(lab[i][j])
			fichier.write(text)
			fichier.write('\n')

