import os,time
if not os.path.isdir('log'):
	os.mkdir('log')

logFile = open('log/log.txt','w')
def log(linha="",tela=True):
	if tela:
		print(linha)
	logFile.write(linha+'\n')

tempoInicioBench = time.time()

# Configurações padrões
qtde = 50
printResult = False

# CARREGANDO CONFIGURAÇÕES
conf = open("benchmark.conf","r")
for linha in conf:
	linha = linha.strip()
	if "#" not in linha and linha != '':
		if 'PRINT_RESULT=' in linha:
			linha = linha.upper().replace('PRINT_RESULT=','')
			if linha == 'TRUE':
				printResult = True
			else:
				printResult = False
		if 'QNTD=' in linha:
			linha = linha.replace('QNTD=','')
			if linha.isnumeric():
				qtde = int(linha)
		if 'PRINT_FACTS_WE=' in linha:
			linha = linha.upper().replace('PRINT_FACTS_WE=','')
			if linha == 'TRUE':
				printFactsWE = True
			else:
				printFactsWE = False
		if 'PRINT_AXIOMS_WE=' in linha:
			linha = linha.upper().replace('PRINT_AXIOMS_WE=','')
			if linha == 'TRUE':
				printAxiomsWE = True
			else:
				printAxiomsWE = False
				
conf.close()

# Carregando ontologias
log("======================")
log("Ínicio do Benchmark")
log("Carregando informações do arquivo 'benchmark.conf'")
log("Quantidade total de execuções por linha e por motor: "+str(qtde))
log("")

conf = open("benchmark.conf","r")
for linha in conf:
	if "#" not in linha and 'BENCH_EXECUTE=' in linha:
		linha = linha.replace('BENCH_EXECUTE=','')
		command = linha.rstrip().split(",")
		command = " ".join(command)
		log("")
		log("=== Próxima Execução (Ontologia / Querys)")
		log(command)
		log("")
		log("==")
		log("WSML Engine")
		log("==")
		totalCarregarOntologia = 0
		totalConsulta = 0
		commandWsmlEngine = "python3 wsml-engine-bench.py " + str(command)
		for x in range(qtde):
			log("Loop "+str(x))
			result = os.popen(commandWsmlEngine).read()
			result = result.split('\n')
			for l in result:
				if 'Carregar Ontologia: ' in l:
					l = l.replace('Carregar Ontologia: ','')
					l = l[:-3]
					tempoCarregarOntologia = float(l)
					log("Ontologia: "+str(tempoCarregarOntologia))
					totalCarregarOntologia += tempoCarregarOntologia
				elif 'Tempo de Execução: ' in l:
					l = l.replace('Tempo de Execução: ','')
					l = l[:-3]
					tempoConsulta = float(l)
					log("Consulta: "+str(tempoConsulta))
					totalConsulta += tempoConsulta
				elif printResult and 'Resultado: ' in l:
					log(l)
				elif printFactsWE and 'Fatos: ' in l:
					log(l)
				elif printAxiomsWE and 'Axiomas: ' in l:
					log(l)
			log("=")

		log("Tempo total do carregamento da ontologia: "+ str(totalCarregarOntologia))
		log("Média em "+str(qtde)+" execuções: "+str(totalCarregarOntologia/qtde))
		log("Tempo total de execução da consulta: "+ str(totalConsulta))
		log("Média em "+str(qtde)+" execuções: "+str(totalConsulta/qtde))

		log("==")
		log("Íris")
		log("==")
		totalCarregarOntologia = 0
		totalConsulta = 0
		commandIris = "java -jar iris-bench.jar " + str(command)
		for x in range(qtde):
			log("Loop "+str(x))
			result = os.popen(commandIris).read()
			result = result.split('\n')
			for l in result:
				if 'Carregar Ontologia: ' in l:
					l = l.replace('Carregar Ontologia: ','')
					l = l[:-3]
					tempoCarregarOntologia = float(l)
					log("Ontologia: "+str(tempoCarregarOntologia))
					totalCarregarOntologia += tempoCarregarOntologia
				elif 'Tempo de Execução: ' in l:
					l = l.replace('Tempo de Execução: ','')
					l = l[:-3]
					tempoConsulta = float(l)
					log("Consulta: "+str(tempoConsulta))
					totalConsulta += tempoConsulta
				elif printResult and 'Resultado: ' in l:
					log(l)

		log("Tempo total do carregamento da ontologia: "+ str(totalCarregarOntologia))
		log("Média em "+str(qtde)+" execuções: "+str(totalCarregarOntologia/qtde))
		log("Tempo total de execução da consulta: "+ str(totalConsulta))
		log("Média em "+str(qtde)+" execuções: "+str(totalConsulta/qtde))

conf.close()

tempoFimBench = time.time()

log("")
log("Fim do Benchmark")
log("Tempo Total: "+ str(round(tempoFimBench-tempoInicioBench,2)) + " segundos")
log("======================")
logFile.close()