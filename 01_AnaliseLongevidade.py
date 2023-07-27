import cfgClasses

cfg = cfgClasses.CFGAL()
while True:
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
        quantCod -= 1
    sucessores = [int(sucessor) for sucessor in input().split(' ')]

    cfg.inserirBlocoBasico(id, regras, sucessores)
cfg.calcularUseDef()
cfg.analisarLongevidade()
# cfg.showCFG()