from random import random
import matplotlib.pyplot as plt

"""
Desenvolvido por:
 __     _______  ____  _____    _      _____ __  __          
 \ \   / / ____|/ __ \|  __ \  | |    |_   _|  \/  |   /\    
  \ \_/ / |  __| |  | | |__) | | |      | | | \  / |  /  \   
   \   /| | |_ | |  | |  _  /  | |      | | | |\/| | / /\ \  
    | | | |__| | |__| | | \ \  | |____ _| |_| |  | |/ ____ \ 
    |_|  \_____|\____/|_|  \_\ |______|_____|_|  |_/_/    \_\
        
Título: Algoritmo Genético p/ Logística
Data: 16/01/2022
Contato: contato@ygorml.org
                                                             
"""


class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.geracao = geracao
        self.nota_avaliacao = 0
        self.espaco_usado = 0
        self.cromossomo = []
        
        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
                
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espacos[i]
                
        if soma_espacos > self.limite_espacos:
            nota = 1
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos
        
    def mostraInformacoes(self):
        print("Espaco = %s" % str(self.espacos))
        print("Valores = %s" % str(self.valores))
        print("Cromossomo = %s" % str(self.cromossomo))
        
    def mostraAvaliacao(self):
        self.avaliacao()
        print("Nota do individuo: %s" % self.nota_avaliacao)
        print("Espaco utilizado pelo individuo: %s" % self.espaco_usado)
        
    def mostraComponentesCarga(self):
        print("\nComponentes da carga:")
        for i in range(len(lista_produtos)):
            if self.cromossomo[i] == '1':
                print("Nome: %s \t\t\tValor: %s" % (nomes[i], valores[i]))
                
    def resumo(self):
        self.mostraInformacoes()
        self.mostraAvaliacao()
        self.mostraComponentesCarga()
        
    def crossOver(self, outro_individuo):
        corte = round(random() * len(self.cromossomo))
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao+1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao+1)]
        
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    def mutacao(self, taxa_mutacao):
        #print("\nAntes: %s" % self.cromossomo)
        
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
                    
        #print("Depois: %s" % self.cromossomo)
        return self

class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
        
    def inicializaPopulacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        self.melhor_solucao = self.populacao[0]
        
    def ordenaPopulacao(self):
        self.populacao = sorted(self.populacao, key = lambda populacao: populacao.nota_avaliacao, reverse=True)
        
    def melhorIndividuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    def mostraPopulacao(self):
        for i in range(self.tamanho_populacao):
            print("\n=======Individuo %s====" % str(i+1))
            self.populacao[i].resumo()
            
    def somaAvaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return soma
    
    def selecionaPai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai
    
    def visualizaGeracao(self):
        melhor = self.populacao[0]
        print("Geracao: %s -> Valor: %s \t\tEspaço: %s\t\tCromossomo: %s" % (self.populacao[0].geracao,
                                                                             melhor.nota_avaliacao,
                                                                             melhor.espaco_usado,
                                                                             melhor.cromossomo))
        
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializaPopulacao(espacos, valores, limite_espacos)
        
        for individuo in self.populacao:
            individuo.avaliacao()
            
        self.ordenaPopulacao()
        
        melhor_solucao = self.populacao[0]
        
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        self.visualizaGeracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.somaAvaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.selecionaPai(soma_avaliacao)
                pai2 = self.selecionaPai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossOver(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao()
                
            self.ordenaPopulacao()
            
            self.visualizaGeracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhorIndividuo(melhor)

        print("\nMelhor solução -> G: %s -> Valor: %s -> Espaço: %s -> Cromossomo: %s" % (self.melhor_solucao.geracao,
                                                                                          self.melhor_solucao.nota_avaliacao,
                                                                                          self.melhor_solucao.espaco_usado,
                                                                                          self.melhor_solucao.cromossomo))
        return self.melhor_solucao
    
    def mostraGrafico(self):
        plt.plot(ag.lista_solucoes, color='red')
        plt.title('Evolução do Desempenho do Algoritmo Genético')
        plt.xlabel('Número de gerações')
        plt.ylabel('Valor ótimo encontrado')
        plt.show()
        
## ======= main() ======
        
if __name__ == '__main__':
    
    lista_produtos = []
    lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("iPhone X", 0.0000899, 2911.12))
    lista_produtos.append(Produto("iPhone 13 Pro", 0.0000899, 10911.12))
    lista_produtos.append(Produto("Tv 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto("Tv 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto("Tv 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))
    
    espacos = []
    valores = []
    nomes = []
    
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
        
    limite = 3 # limite de 3 metros cúbicos no caminhão
    tamanho_populacao = 20
    taxa_mutacao = 0.01
    numero_geracoes = 400
    
    ag = AlgoritmoGenetico(tamanho_populacao)
    
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    
    for i in range(len(lista_produtos)):
        if resultado.cromossomo[i] == '1':
            print("Nome: %s R$ %s" % (lista_produtos[i].nome, lista_produtos[i].valor))
            
    resultado.resumo()
    ag.mostraGrafico()
    
    
        
        
    
        

