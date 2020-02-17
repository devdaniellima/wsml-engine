import sys,os
import time
from wsmlparser.parser import *

args = sys.argv[1:]
ontCarregada = False

reasoner = Reasoner()
for contArg in range(len(args)):
	arg = args[contArg]
	if (contArg == 0):
		if (os.path.exists(arg)):
			inicio = time.time()
			reasoner.load(arg)
			fim = time.time()
			tempo = (fim-inicio)*100
			print("Carregar Ontologia: "+str(tempo))
			ontCarregada = True
	elif ontCarregada :
		if (os.path.exists(arg)):
			f = open(arg,'r')
			query = f.read()
			f.close()
			inicio = time.time()
			res = reasoner.execute(query)
			fim = time.time()
			tempo = (fim-inicio)*100
			print("Query: "+query)
			print("Tempo de Execução: "+ str(tempo))
			print("Resultado: " + str(res))