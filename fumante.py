from threading import Thread
import time
import random

class Vendedor(Thread):	

	def __init__(self):
		Thread.__init__(self)
		# na primeira instancia pode vender
		self.pode_vender = 0 
		# nenhum produto foi ainda colocado a venda
		self.produto = 0 

	def getProduto(self):
		# valor correspondente aos produtos disponiveis
		return self.produto

	def setFumando(self, fumando):		
		'''
			informa ao vendedor se algum fumante esta fumando
			caso ninguem esteja fumando o vendedor vai colocar
			a venda mais dois produtos
		'''
		self.pode_vender = fumando

	def run(self):	
		# vendedor coloca a venda dois produtos distintos por vez
		# permitinado apenas um fumante poder fumar
		'''
			1 -> tabaco + papel		--> libera fumante 3
			2 -> tabaco + fosforo	--> libera fumante 2
			3 -> papel + fosforo	--> libera fumante 1
		'''
		while True:
			if self.pode_vender == 0: 
				# ocorre a producao e venda de dois produtos 
				# quando nenhum fumante esta fumando
				self.produto = random.randint(1, 3)
				# esperar os produtos serem condumidos 
				# para colocar outros a venda
				self.pode_vender = 1 		
		
class Fumante(Thread):
	
	def __init__(self, num_fumante):		
		Thread.__init__(self)
		self.num_fumante = num_fumante
		# quando um fumante e criado ele ainda nao esta fumando
		self.fumando = 0 

	def setFumando(self, fumando):
		self.fumando = fumando
		# 0 - nao esta fumando
		# 1 - esta fumando

	def getFumando(self):
		# retorna a condicao atual do fumante
		return self.fumando

	def run(self):
		while True:
			# o fumante comeca a fuma quando coleta os produtos necessarios
			if self.fumando == 1:
				tempo = random.randint(1, 5)
				print(" Fumante [" + self.num_fumante + "]", end="")
				print(" ira fumar durante [" + str(tempo) + "s]")	
				# aguarda o tempo de fumar			
				time.sleep(tempo)
				# finaliza o ato de fumar
				self.fumando = 0 
				print(" Fumante [" + self.num_fumante + "]", end="")
				print(" terminou de fumar")

if __name__ == '__main__':
	print("\n Fumante [1] possui tabaco")
	print(" Fumante [2] possui papel")
	print(" Fumante [3] possui fosforo\n")

	# fumante 1 criado - fica aguardando venda do papel  + fosforo
	fumante1 = Fumante('1') 
	fumante1.start()

	# fumante 2 criado - fica aguardando venda do tabaco + fosforo
	fumante2 = Fumante('2') 
	fumante2.start()

	# fumante 3 criado - fica aguardando venda do tabaco + papel
	fumante3 = Fumante('3') 
	fumante3.start()

	vendedor = Vendedor() 	# vendedor e criado	
	vendedor.start()

	# serve para controlde de venda do vendedor
	# permitindo ou não a coleta de produtos
	semaforo = 0; 

	while True: # vida eterna para fumantes e vendedor

		if semaforo == 0:
			# recebe valor correspondente a quais produtos estao disponiveis
			produto = vendedor.getProduto() 
			semaforo = 1

			if produto == 1:
				# tabaco + papel - produzidos - fumante 3 ira fumar
				print("\n Vendendo: Tabaco e Papel")
				fumante3.setFumando(1) # fumante 3 inicia o fumo
				vendedor.setFumando(1)

			elif produto == 2:
				# tabaco + papel - produzidos - fumante 2 ira fumar
				print("\n Vendendo: Tabaco e Fosforo")
				fumante2.setFumando(1) # fumante 2 inicia o fumo
				vendedor.setFumando(1)

			else:
				# tabaco + papel - produzidos - fumante 1 ira fumar
				print("\n Vendendo: Papel e Fosforo")
				fumante1.setFumando(1) # fumante 1 inicia o fumo
				vendedor.setFumando(1)

		f1 = fumante1.getFumando()
		f2 = fumante2.getFumando()
		f3 = fumante3.getFumando()

		if f1 == 0 and f2 == 0 and f3 == 0:
			# avisa ao vendedor que pode vender mais produtos
			vendedor.setFumando(0)
			semaforo = 0			

	fumante1.join()
	fumante2.join()
	fumante3.join()
	vendedor.join()