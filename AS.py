import math

class Interval:
    def __init__(self, min, max, direita = True, esquerda = True):
        self.min = min
        self.max = max
        self.direita = direita  #True se fechado, False se aberto
        self.esquerda = esquerda 

    def __str__(self):
        if self.direita and self.esquerda:
            return "[%s, %s]" %(self.min, self.max)
        if not self.direita and self.esquerda:
            return "[%s, %s)" %(self.min, self.max)
        if self.direita and not self.esquerda:
            return "(%s, %s]" %(self.min, self.max)
        if not self.direita and not self.esquerda:
            return "(%s, %s)" %(self.min, self.max) 
        
    def atualiza(self, min, max, direita, esquerda):
        self.min = min
        self.max = max
        self.esquerda = esquerda
        self.direita = direita

    def intervalIntersecta(self, interval):
        if self.intervalPertence(interval):
            return True
        if self.esquerda:
            maxIntersectaMin = self.min <= interval.max
            minIntersectaMin = self.min <= interval.min
        else:
            maxIntersectaMin = self.min < interval.max
            minIntersectaMin = self.min < interval.min
        if self.direita:
            maxIntersectaMax = self.max >= interval.max
            minIntersectaMax = self.max >= interval.min
        else:
            maxIntersectaMax = self.max > interval.max
            minIntersectaMax = self.max > interval.min
        if (maxIntersectaMin and maxIntersectaMax) or (minIntersectaMin and minIntersectaMax):
            return True
        return False
    
    def intervalPertence(self, interval):
        if self.esquerda:
            menorPert = self.min >= interval.min
        else:
            menorPert = self.min > interval.min
        if self.direita:
            maiorPert = self.max <= interval.max
        else:
            maiorPert = self.max < interval.max
        if self.min >= interval.min and self.max <= interval.max:
            return True
        return False

    def elementPertence(self, x):
        if self.esquerda:
            menorPert = self.min <= x
        else:
            menorPert = self.min < x
        if self.direita:
            maiorPert = self.max >= x
        else:
            maiorPert = self.max > x
        if menorPert and maiorPert:
            return True
        return False

    def equal(self, interval):
        if self.min == interval.min and self.max == interval.max:
            return True
        return False

class Node:
    def __init__(self, interval, left, right, size):
        self.interval = interval
        self.segmentos = []
        self.right = right
        self.left = left
        self.size = size


class AS:  
    def __init__(self, S):
        intervalos = []
        for i in S:
            intervalos.append(i.min)
            intervalos.append(i.max)
        root = None
        intervalos = sort(intervalos)
        for i in range(0, len(intervalos)):
            if i == 0:
                esquerda = Node(Interval(-math.inf, intervalos[i], False, False), None, None, 1)
                direita = Node(Interval(intervalos[i], intervalos[i], True, True), None, None, 1)
                root = criaSubArvore(esquerda, direita)
            else:
                root = insert(root, Interval(intervalos[i - 1], intervalos[i], False, False))
                root = insert(root, Interval(intervalos[i], intervalos[i], True, True))
                if i == len(intervalos) - 1:
                    root = insert(root, Interval(intervalos[i], math.inf, False, False))
        for interval in S:
            adicionaSegmento(root, interval)

        self.root = root
        self.S = S
    
    def Segments(self, x):
        aux = self.root
        segmentos = []
        self.SegmentsRec(aux, x, segmentos)
        return segmentos

    def SegmentsRec(self, node, x, segmentos):
        segmentos += node.segmentos
        if node.right != None and node.right.interval.elementPertence(x):
            self.SegmentsRec(node.right, x, segmentos)
        if node.left != None and node.left.interval.elementPertence(x):
            self.SegmentsRec(node.left, x, segmentos)

    
    def Print(self):
        self.PrintAux(self.root, 0)
    
    def PrintAux(self, node, d):
        if node == None:
            return
        self.PrintAux(node.right, d + 1)
        for i in range(d):
            print("         ", end = "")
        if node.segmentos == []:
            print(node.segmentos)
        else:
            for i in node.segmentos:
                print(i, end = "")
            print()
        self.PrintAux(node.left, d + 1)

def insert(node, interval):
    if size(node.left) <= size(node.right):
        new = Node(interval, None, None, 1)
        return Node(Interval(node.interval.min, interval.max, interval.direita, node.interval.esquerda), node, new, 1 + node.size)
    else:
        node.right = insert(node.right, interval)
        node.size = size(node.right) + size(node.left)
        node.interval.atualiza(node.left.interval.min, node.right.interval.max, node.right.interval.direita, node.left.interval.esquerda)
        return node

def adicionaSegmento(r, interval):
    if r.interval.intervalPertence(interval):
        r.segmentos.append(interval)
        return
    direita = r.right
    esquerda = r.left
    if direita != None:
        pertenceDir = direita.interval.intervalIntersecta(interval)
    else:
        pertenceDir = False
    if esquerda != None:
        pertenceEsq = esquerda.interval.intervalIntersecta(interval)
    else:
        pertenceEsq = False
    if pertenceDir:
        adicionaSegmento(r.right, interval)
    if pertenceEsq:
        adicionaSegmento(r.left, interval)
        
    
class ASDinamica:
    def __init__(self):
        self.AS = []
    
    def insert(self, s):
        self.AS.append(AS([s]))
        while len(self.AS) > 1 and size(self.AS[-1].root) == size(self.AS[-2].root):
            new = self.AS[-1].S + self.AS[-2].S
            self.AS.pop()
            self.AS.pop()
            self.AS.append(AS(new))

    def Segments(self, x):
        resp = []
        for AS in self.AS:
            resp += AS.Segments(x)
        return resp



def printArvore(r):
    printArvoreAux(r, 0)
    print()
    print()

def printArvoreAux(r, d):
    if r == None:
        return
    printArvoreAux(r.right, d + 1)
    for i in range(0, d):
        print("      ", end = "")
    print(r.interval)
    printArvoreAux(r.left, d + 1)

def size(node):
    if node == None:
        return 0
    return node.size


            
def criaSubArvore(esquerda, direita):
    return Node(Interval(esquerda.interval.min, direita.interval.max, direita.interval.direita, esquerda.interval.esquerda), esquerda, direita, esquerda.size + direita.size)



def sort(v):
    if len(v) > 1:
        meio = len(v)//2
        v1 = v[0:meio]
        v2 = v[meio:len(v)]
        return merge(sort(v1),sort(v2))
    else:
        return v

def merge(v1, v2):
    p1 = 0
    p2 = 0
    resp = []
    while p1 < len(v1) and p2 < len(v2):
        if v1[p1] < v2[p2]:
            resp.append(v1[p1])
            p1 += 1
        elif v1[p1] > v2[p2]:
            resp.append(v2[p2])
            p2 += 1
        else:
            resp.append(v2[p2])
            p2 += 1
            p1 += 1
    while p1 < len(v1):
        resp.append(v1[p1])
        p1 += 1
    while p2 < len(v2):
        resp.append(v2[p2])
        p2 += 1
    return resp

def pegaComando(s):
    i = 0
    while i < len(s) and s[i] != "(":
        i +=1
    return i

def pegaLista(s, i):
    lista = s[i + 1: -2]
    prov = 0
    intervalos = []
    index = 0
    while index < len(lista):
        if lista[index] == "[" or lista[index] == "," or lista[index] == " " or lista[index] == "]":
            index += 1
            continue
        else:
            j = 0
            while lista[index + j] != " " and lista[index + j] != "," and lista[index + j] != "[" and lista[index + j] != "]":
                j += 1
            if prov % 2 == 0:
                min = int(lista[index:index + j])
                prov += 1
            else:
                max = int(lista[index:index + j])
                prov += 1
                intervalos.append(Interval(min, max))
            index += j

    return intervalos

def pegaArgumento(s, i):
    args = []
    i += 1
    while i < len(s) and s[i] != ")":
        if s[i] != " " and s[i] != ",":
            j = 0
            while s[j + i] != " " and s[j + i] != "," and s[j + i] != ")":
                j += 1
            args.append(int(s[i:i + j]))
            i += j
        i += 1
    return args

            

def main():
    modo = int(input("Escolha um modo de execução(1 - Árvore de segmentos estática e 2 - Árvore de segmentos dinâmica): "))
    if modo == 1:
        print("***********Árvore de segmentos estática***********")
        while True:
            comando = input()
            i = pegaComando(comando)
            if comando == "exit()":
                return
            elif comando[0: i] == "AS":
                intervalos = pegaLista(comando, i)
                r = AS(intervalos)
            elif comando[0:i] == "Segments":
                args = pegaArgumento(comando, i)
                segmentos = r.Segments(args[0])
                for seg in segmentos:
                    print(seg, end = " ")
                print()
            elif comando[0: i] == "Print":
                r.Print()
            else:
                print("Comando inválido")
    elif modo == 2:
        print("***********Árvore de segmentos dinâmica***********")
        while True:
            comando = input()
            i = pegaComando(comando)
            if comando == "exit()":
                return
            elif comando == "AS()":
                r = ASDinamica()
            elif comando[0:i] == "Insert":
                intervalo = pegaArgumento(comando, i)
                r.insert(Interval(intervalo[0], intervalo[1]))
            elif comando[0:i] == "Segments":
                args = pegaArgumento(comando, i)
                segmentos = r.Segments(args[0])
                for seg in segmentos:
                    print(seg, end = " ")
                print()
                
            else:
                print("Comando inválido")
    else:
        print("Modo de execução inválido")

#r = AS([Interval(0,1),Interval(5,7),Interval(1,10), Interval(3,7)])
#printArvore(r.root)
#segmentos = r.Segments(1)
#for i in segmentos:
#    print(i)
#r.Print()

#r = ASDinamica()
#r.insert(Interval(0,1))
#r.insert(Interval(5,7))
#r.insert(Interval(1,10))
#r.insert(Interval(3,7))
#segmentos = r.Segments(1)
#for i in segmentos:
#    print(i)
main()