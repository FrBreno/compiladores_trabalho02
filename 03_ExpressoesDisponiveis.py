import cfgClasses

cfg = cfgClasses.CFGAED()
idRegra = 1
while True:
    idRegras = []
    regras = []
    sucessores = []
    
    entrada = input()
    if not entrada:
        break
    
    entrada = entrada.split(' ')
    id = int(entrada[0])
    quantCod = int(entrada[1])

    while quantCod > 0:
        regras.append(input())
        idRegras.append(idRegra)
        idRegra += 1
        quantCod -= 1
    sucessores = [int(sucessor) for sucessor in input().split(' ')]

    cfg.inserirBlocoBasico(id, idRegras, regras, sucessores)
cfg.construirCFG()
cfg.analisarCFG()
# cfg.showCFG()