class BlocoBasico:
    def __init__(self, id, regras, sucessores):
        self.id = id
        self.regras = regras
        self.sucessores = sucessores
        self.predecessores = []
        self.inb = set()
        self.outb = set()

    def __str__(self):
        return f'Bloco_ID: {self.id}\n Regras: {self.regras}\n IN[{self.id}]: {self.inb}\n OUT[{self.id}]: {self.outb}\n Sucessores: {self.sucessores}\n'

class BlocoBasicoAL(BlocoBasico):
    def __init__(self, id, regras, sucessores):
        super().__init__(id, regras, sucessores)
        self.defb = set()
        self.useb = set()
    
    def __str__(self):
        return f'Bloco_ID: {self.id}\n Regras: {self.regras}\n IN[{self.id}]: {self.inb}\n OUT[{self.id}]: {self.outb}\n DefB: {self.defb}\n UseB: {self.useb}\n Sucessores: {self.sucessores}\n'


class BlocoBasicoADA(BlocoBasico):
    def __init__(self, id, idRegras, regras, sucessores):
        super().__init__(id, regras, sucessores)
        self.idRegras = idRegras
        self.genb = set()
        self.killb = set()
    
    def __str__(self):
        return f'Bloco_ID: {self.id}\n Regras: {self.regras}\n IN[{self.id}]: {self.inb}\n OUT[{self.id}]: {self.outb}\n GenB: {self.genb}\n KillB: {self.killb}\n Predecessores: {self.predecessores}\n Sucessores: {self.sucessores}\n'

class CFG:
    def __init__(self):
        self.blocosBasicos = []

    def inserirBlocoBasico(self, id, regras, sucessores):
        novoBloco = BlocoBasico(id, regras, sucessores)
        self.blocosBasicos.append(novoBloco)
    
    def showCFG(self):
        for bloco in self.blocosBasicos:
            print(bloco)

    def showInOut(self):
        for bloco in self.blocosBasicos:
            sorted_outb = sorted(bloco.outb)
            sorted_inb = sorted(bloco.inb)
            
            print(f'OUT[{bloco.id}] = {sorted_outb if len(sorted_outb) > 0 else []}\t\t\tIN[{bloco.id}] = {sorted_inb if len(sorted_inb) > 0 else []}')



class CFGAL(CFG):
    def __init__(self):
        super().__init__()
    
    def inserirBlocoBasico(self, id, regras, sucessores):
        novoBloco = BlocoBasicoAL(id, regras, sucessores)
        self.blocosBasicos.append(novoBloco)

    def calcularUseDef(self):
        for bloco in self.blocosBasicos:
            for regra in bloco.regras:
                if '=' in regra:
                    regraSplit = regra.split('=')
                    regraEsq = ''.join(regraSplit[0].split())
                    regraDir = ''.join(regraSplit[1].split())

                    if '+' in regraDir:
                        regraDir = regraDir.split('+')
                    elif '-' in regraDir:
                        regraDir = regraDir.split('-')
                    elif '*' in regraDir:
                        regraDir = regraDir.split('*')
                    elif '/' in regraDir:
                        regraDir = regraDir.split('/')
                    elif '%' in regraDir:
                        regraDir = regraDir.split('%')

                    if (regraEsq not in bloco.defb) and (regraEsq not in bloco.useb):
                        if (regraEsq in regraDir):
                            bloco.useb.add(regraEsq)
                        else:
                            bloco.defb.add(regraEsq)
                    
                    for valor in regraDir:
                        if (valor not in bloco.defb) and (not valor.isdigit() and valor.islower()):
                            bloco.useb.add(valor)
                elif 'if' in regra:
                    regraSplit = ''.join(''.join(regra.split('if')[1].split('goto')).split())
                    if '<' in regraSplit:
                        regraSplit = ''.join(regraSplit.split('<'))
                    if '>' in regraSplit:
                        regraSplit = ''.join(regraSplit.split('>'))
                    if '==' in regraSplit:
                        regraSplit = ''.join(regraSplit.split('=='))
                    if '!=' in regraSplit:
                        regraSplit = ''.join(regraSplit.split('!='))
                    if '%' in regraSplit:
                        regraSplit = ''.join(regraSplit.split('%'))
                    for valor in list(regraSplit):
                        if not valor.isdigit() and valor.islower():
                            bloco.useb.add(valor)
                elif 'return' in regra:
                    regraSplit = ''.join(regra.split('return')[1].split())
                    if not regraSplit.isdigit() and regraSplit.islower():
                        bloco.useb.add(regraSplit)
            
            for sucessor in bloco.sucessores:
                if sucessor != 0:
                    self.blocosBasicos[sucessor - 1].predecessores.append(bloco.id)

    def analisarLongevidade(self):
        blocosParaAnalise = set()
        for bloco in self.blocosBasicos:
            blocosParaAnalise.add(bloco.id)
        
        while len(blocosParaAnalise) > 0:
            for blocoId in blocosParaAnalise.copy():
                bloco = self.blocosBasicos[blocoId - 1]
                alterou = False
                # Definindo o conjunto OUT[B]:
                for sucessorId in bloco.sucessores:
                    if sucessorId != 0:
                        sucessor = self.blocosBasicos[sucessorId - 1]
                        uniao = bloco.outb | sucessor.inb
                        if bloco.outb != uniao:
                            bloco.outb = uniao
                            alterou = True
                # Definindo o conjunto IN[B]:
                novoIn = bloco.useb | (bloco.outb - bloco.defb)
                if (bloco.inb != novoIn):
                    bloco.inb = novoIn
                    alterou = True
                # Verificando alterações no bloco:
                # Se houve alterações no bloco em questão, o mesmo e seus sucessores
                # são marcados para uma nova análise posterior
                # Caso contrário, o bloco será removido do conjunto para análise.
                if alterou:
                    blocosParaAnalise.add(bloco.id)
                    for predecessorId in bloco.predecessores:
                        if predecessorId != 0:
                            blocosParaAnalise.add(predecessorId)
                else:
                    if bloco.id in blocosParaAnalise:
                        blocosParaAnalise.remove(bloco.id)
        self.showInOut()

class CFGADA(CFG):
    def __init__(self):
        super().__init__()
        self.tabelaDefinicoes = {}
    
    def inserirBlocoBasico(self, id, idRegras, regras, sucessores):
        novoBloco = BlocoBasicoADA(id, idRegras, regras, sucessores)
        self.blocosBasicos.append(novoBloco)

    def construirTabelaDef(self):
        for bloco in self.blocosBasicos:
            for idRegra, regra in zip(bloco.idRegras, bloco.regras):
                if '=' in regra:
                    regraEsq = ''.join(regra.split('=')[0].split())
                    if regraEsq in self.tabelaDefinicoes:
                        self.tabelaDefinicoes[regraEsq] |= {idRegra}
                    else:
                        self.tabelaDefinicoes[regraEsq] = {idRegra}

    def calcularGenKill(self):
        for bloco in self.blocosBasicos:
            for idRegra, regra in zip(bloco.idRegras, bloco.regras):
                if '=' in regra:
                    regraSplit = regra.split('=')
                    regraEsq = ''.join(regraSplit[0].split())
                    bloco.genb.add(idRegra)
                    bloco.killb.update(self.tabelaDefinicoes[regraEsq] - {idRegra})

            for sucessor in bloco.sucessores:
                if sucessor != 0:
                    self.blocosBasicos[sucessor - 1].predecessores.append(bloco.id)

    def analisarCFG(self):
        blocosParaAnalise = set()
        for bloco in self.blocosBasicos:
            blocosParaAnalise.add(bloco.id)
        
        while len(blocosParaAnalise) > 0:
            for blocoId in blocosParaAnalise.copy():
                bloco = self.blocosBasicos[blocoId - 1]
                alterou = False
                # Definindo o conjunto IN[B]:
                for predecessorId in bloco.predecessores:
                    predecessor = self.blocosBasicos[predecessorId - 1]
                    uniao = bloco.inb | predecessor.outb
                    if bloco.inb != uniao:
                        bloco.inb = uniao
                        alterou = True
                # Definindo o conjunto OUT[B]:
                novoOut = bloco.genb | (bloco.inb - bloco.killb)
                if (bloco.outb != novoOut):
                    bloco.outb = novoOut
                    alterou = True
                # Verificando alterações no bloco:
                # Se houve alterações no bloco em questão, seus sucessores
                # são marcados para uma nova análise posterior
                if alterou:
                    for sucessorId in bloco.sucessores:
                        if sucessorId != 0:
                            blocosParaAnalise.add(sucessorId)
                # Bloco atual removido da análise posterior:
                if bloco.id in blocosParaAnalise:
                    blocosParaAnalise.remove(bloco.id)
        self.showInOut()

    def construirCFG(self):
        self.construirTabelaDef()
        self.calcularGenKill()

    def showInOut(self):
        for bloco in self.blocosBasicos:
            outb = set(f'd{outValue}' for outValue in bloco.outb)
            inb = set(f'd{inValue}' for inValue in bloco.inb)
            
            sorted_outb = sorted(outb)
            sorted_inb = sorted(inb)
            
            print(f'OUT[{bloco.id}] = {sorted_outb if len(sorted_outb) > 0 else {}}\t\t\tIN[{bloco.id}] = {sorted_inb if len(sorted_inb) > 0 else {}}')


class CFGAED(CFGADA):
    def __init__(self):
        super().__init__()
    
    def construirTabelaDef(self):
        for bloco in self.blocosBasicos:
            for idRegra, regra in zip(bloco.idRegras, bloco.regras):
                if '=' in regra:
                    regraDir = ''.join(regra.split('=')[1].split())
                    if not regraDir in self.tabelaDefinicoes and (not regraDir.isdigit() and regraDir.islower()):
                        self.tabelaDefinicoes[regraDir] = idRegra

    def calcularGenKill(self):
        for bloco in self.blocosBasicos:
            regrasDir = [''.join(regra.split('=')[1].split()) for regra in bloco.regras if '=' in regra]
            regrasEsq = [''.join(regra.split('=')[0].split()) for regra in bloco.regras if '=' in regra]
            for definicao in self.tabelaDefinicoes:
                redefinicao = False
                if definicao in regrasDir:
                    candidato = definicao
                    if '+' in candidato:
                        candidato = candidato.split('+')
                    elif '-' in candidato:
                        candidato = candidato.split('-')
                    elif '*' in candidato:
                        candidato = candidato.split('*')
                    elif '/' in candidato:
                        candidato = candidato.split('/')
                    elif '%' in candidato:
                        candidato = candidato.split('%')
                    
                    for regra in regrasEsq:
                        if regra in candidato:
                            redefinicao = True
                            break
                    
                    if not redefinicao:
                        bloco.genb.add(self.tabelaDefinicoes[definicao])

            for index, regra in enumerate(regrasEsq):
                for definicao in self.tabelaDefinicoes.keys():
                    if regra in definicao:
                        if not definicao in bloco.regras[index + 1:]:
                            bloco.killb.add(self.tabelaDefinicoes[definicao])

            for sucessor in bloco.sucessores:
                if sucessor != 0:
                    self.blocosBasicos[sucessor - 1].predecessores.append(bloco.id)

    def analisarCFG(self):
        blocosParaAnalise = set()
        for bloco in self.blocosBasicos:
            blocosParaAnalise.add(bloco.id)
        
        while len(blocosParaAnalise) > 0:
            for blocoId in blocosParaAnalise.copy():
                bloco = self.blocosBasicos[blocoId - 1]
                alterou = False
                # Definindo o conjunto IN[B]:
                intersecao = set()
                for index, predecessorId in enumerate(bloco.predecessores):
                    predecessor = self.blocosBasicos[predecessorId - 1]
                    if index == 0:
                        intersecao.update(predecessor.outb)
                    intersecao = intersecao & predecessor.outb
                
                if bloco.inb != intersecao:
                    bloco.inb = intersecao
                    alterou = True
                
                # Definindo o conjunto OUT[B]:
                novoOut = bloco.genb | (bloco.inb - bloco.killb)
                if (bloco.outb != novoOut):
                    bloco.outb = novoOut
                    alterou = True
                # Verificando alterações no bloco:
                # Se houve alterações no bloco em questão, seus sucessores
                # são marcados para uma nova análise posterior
                if alterou:
                    for sucessorId in bloco.sucessores:
                        if sucessorId != 0:
                            blocosParaAnalise.add(sucessorId)
                # Bloco atual removido da análise posterior:
                if bloco.id in blocosParaAnalise:
                    blocosParaAnalise.remove(bloco.id)
        self.showInOut()
