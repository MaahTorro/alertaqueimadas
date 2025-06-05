#INTEGRANTES:
# Marcela Torro RM557658 <3
# Rodrigo RM550266

import heapq
import random
import time
from collections import deque
import matplotlib.pyplot as plt

# ---------- cores ----------
class Cor:
    RESET = '\033[0m'
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    CIANO = '\033[96m'
    NEGRITO = '\033[1m'

# ---------- classes ----------

class Ocorrencia:
    def __init__(self, regiao, severidade, descricao):
        self.regiao = regiao
        self.severidade = severidade
        self.descricao = descricao
        self.timestamp = time.time()  # Adiciona timestamp para ordenação secundária

    def __lt__(self, other):
        # Prioriza por severidade, em caso de empate usa timestamp (mais antigo primeiro)
        if self.severidade == other.severidade:
            return self.timestamp < other.timestamp
        return self.severidade > other.severidade  

    def __str__(self):
        return f"📍 [{self.regiao}] | 🔥 Severidade: {self.severidade} | 📝 {self.descricao}"

# lista para historico

class NoHistorico:
    def __init__(self, ocorrencia):
        self.ocorrencia = ocorrencia
        self.proximo = None

class ListaHistorico:
    def __init__(self):
        self.inicio = None
        self.tamanho = 0

    def adicionar(self, ocorrencia):
        novo = NoHistorico(ocorrencia)
        novo.proximo = self.inicio
        self.inicio = novo
        self.tamanho += 1

    def listar(self):
        if not self.inicio:
            print("🕸️ Nenhum atendimento registrado.")
            return
            
        atual = self.inicio
        while atual:
            print(f"{Cor.CIANO}{atual.ocorrencia}{Cor.RESET}")
            atual = atual.proximo
            
    def tamanho(self):
        return self.tamanho

# Árvore para organizar ocorrências por região
class NoArvore:
    def __init__(self, regiao):
        self.regiao = regiao
        self.ocorrencias = []
        self.esquerda = None
        self.direita = None

class ArvoreRegioes:
    def __init__(self):
        self.raiz = None
        
    def inserir(self, regiao, ocorrencia):
        if not self.raiz:
            self.raiz = NoArvore(regiao)
            self.raiz.ocorrencias.append(ocorrencia)
        else:
            self._inserir_recursivo(self.raiz, regiao, ocorrencia)
    
    def _inserir_recursivo(self, no, regiao, ocorrencia):
        if regiao < no.regiao:
            if no.esquerda is None:
                no.esquerda = NoArvore(regiao)
                no.esquerda.ocorrencias.append(ocorrencia)
            else:
                self._inserir_recursivo(no.esquerda, regiao, ocorrencia)
        elif regiao > no.regiao:
            if no.direita is None:
                no.direita = NoArvore(regiao)
                no.direita.ocorrencias.append(ocorrencia)
            else:
                self._inserir_recursivo(no.direita, regiao, ocorrencia)
        else:
            no.ocorrencias.append(ocorrencia)
    
    def listar_por_regiao(self, regiao):
        return self._buscar(self.raiz, regiao)
    
    def _buscar(self, no, regiao):
        if no is None:
            return []
        if regiao == no.regiao:
            return no.ocorrencias
        if regiao < no.regiao:
            return self._buscar(no.esquerda, regiao)
        return self._buscar(no.direita, regiao)
    
    def listar_todas_regioes(self):
        regioes = []
        self._in_order_traversal(self.raiz, regioes)
        return regioes
    
    def _in_order_traversal(self, no, regioes):
        if no:
            self._in_order_traversal(no.esquerda, regioes)
            regioes.append(no.regiao)
            self._in_order_traversal(no.direita, regioes)

# ---------- sistema principal ----------

class FireResponseSim:
    def __init__(self):
        self.heap_ocorrencias = []  # Heap para priorização
        self.fila_espera = deque()  # Fila para ocorrências em espera
        self.historico = ListaHistorico()  # Lista ligada para histórico
        self.arvore_regioes = ArvoreRegioes()  # Árvore para organizar por região
        self.total_ocorrencias = 0

    def inserir_ocorrencia(self, regiao, severidade, descricao):
        ocorrencia = Ocorrencia(regiao, severidade, descricao)
        self.total_ocorrencias += 1
        
        # Adiciona na árvore de regiões
        self.arvore_regioes.inserir(regiao, ocorrencia)
        
        # Adiciona no heap ou na fila de espera
        if len(self.heap_ocorrencias) < 5:
            heapq.heappush(self.heap_ocorrencias, ocorrencia)
        else:
            self.fila_espera.append(ocorrencia)
            
        print(f"{Cor.VERDE}✅ Nova ocorrência registrada com sucesso!{Cor.RESET}")
        print(f"   Região: {regiao} | Severidade: {severidade} | ID: #{self.total_ocorrencias}")

    def atender_ocorrencia(self):
        if self.heap_ocorrencias:
            ocorrencia = heapq.heappop(self.heap_ocorrencias)
            self.historico.adicionar(ocorrencia)
            print(f"{Cor.AMARELO}🚨 Atendimento em andamento:{Cor.RESET}")
            print(f"{Cor.AMARELO}   {ocorrencia}{Cor.RESET}")
            
            # Se houver ocorrências na fila de espera, move uma para o heap
            if self.fila_espera:
                nova = self.fila_espera.popleft()
                heapq.heappush(self.heap_ocorrencias, nova)
                print(f"{Cor.VERDE}📋 Ocorrência movida da fila de espera para atendimento prioritário.{Cor.RESET}")
        else:
            print(f"{Cor.VERMELHO}⚠️ Nenhuma ocorrência disponível para atendimento.{Cor.RESET}")

    def listar_ocorrencias_pendentes(self):
        print(f"{Cor.AZUL}\n🔄 Ocorrências Pendentes (Prioridade):{Cor.RESET}")
        if not self.heap_ocorrencias:
            print("🕸️ Nenhuma ocorrência prioritária pendente.")
        else:
            # Cria uma cópia do heap para não afetar a estrutura original
            heap_copia = self.heap_ocorrencias.copy()
            while heap_copia:
                ocorrencia = heapq.heappop(heap_copia)
                print(f"🔥 {ocorrencia}")
                
        print(f"{Cor.AZUL}\n⏳ Fila de Espera:{Cor.RESET}")
        if not self.fila_espera:
            print("🕸️ Nenhuma ocorrência na fila de espera.")
        else:
            for i, ocorrencia in enumerate(self.fila_espera):
                print(f"⏱️ {i+1}. {ocorrencia}")

    def listar_historico(self):
        print(f"{Cor.CIANO}\n📚 Histórico completo de ocorrências atendidas:{Cor.RESET}")
        self.historico.listar()

    def gerar_relatorio_por_regiao(self):
        print(f"{Cor.AZUL}\n📊 Relatório de Atendimentos por Região:{Cor.RESET}")
        regioes = self.arvore_regioes.listar_todas_regioes()
        
        if not regioes:
            print("🏜️ Nenhuma região com ocorrências registradas.")
            return
        
        for regiao in regioes:
            ocorrencias = self.arvore_regioes.listar_por_regiao(regiao)
            print(f"\n{Cor.NEGRITO}{Cor.VERDE}🌍 Região: {regiao}{Cor.RESET}")
            print(f"📈 Total de ocorrências: {len(ocorrencias)}")
            
            if ocorrencias:
                severidade_total = sum(o.severidade for o in ocorrencias)
                media_severidade = severidade_total / len(ocorrencias)
                print(f"🔥 Severidade média: {media_severidade:.1f}")
                
                print(f"\n{Cor.AMARELO}Listagem de ocorrências:{Cor.RESET}")
                for o in ocorrencias:
                    print(f"  - {o.descricao} (Severidade: {o.severidade})")
                    
    # -------------------  Gráfico de severidade :) 
    
    def gerar_grafico_severidade_por_regiao(self):
        regioes = self.arvore_regioes.listar_todas_regioes()
        if not regioes:
            print("🏜️ Nenhuma região com ocorrências registradas para gerar gráfico.")
            return
        
        regioes_grafico = []
        severidades_medias = []
        
        for regiao in regioes:
            ocorrencias = self.arvore_regioes.listar_por_regiao(regiao)
            if ocorrencias:
                media = sum(o.severidade for o in ocorrencias) / len(ocorrencias)
                regioes_grafico.append(regiao)
                severidades_medias.append(media)
        
        plt.figure(figsize=(8,5))
        plt.bar(regioes_grafico, severidades_medias, color='orange')
        plt.title('Severidade Média das Ocorrências por Região')
        plt.xlabel('Região')
        plt.ylabel('Severidade Média')
        plt.ylim(0,10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def simular_chamadas(self, n=5):
        regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
        print(f"{Cor.AMARELO}🔁 Simulando {n} chamadas aleatórias...{Cor.RESET}")
        for i in range(n):
            self.inserir_ocorrencia(
                regiao=random.choice(regioes),
                severidade=random.randint(1, 10),
                descricao=f"Incêndio florestal {i+1}"
            )
            time.sleep(0.3)

    def simular_chamadas_crescentes(self, n=5):
        regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
        print(f"{Cor.AMARELO}🔄 Simulando {n} chamadas com severidade crescente...{Cor.RESET}")
        
        for i in range(n):
            # Severidade aumenta gradualmente
            severidade = min(i + 1 + random.randint(0, 2), 10)
            regiao = random.choice(regioes)
            descricao = f"Incêndio florestal de nível {severidade}"
            
            self.inserir_ocorrencia(regiao, severidade, descricao)
            time.sleep(0.3)

# ---------- interface ----------

def menu():
    sim = FireResponseSim()
    while True:
        print(f"""{Cor.NEGRITO}
{Cor.AZUL}🔥 SIMULADOR DE RESPOSTA A QUEIMADAS 🔥{Cor.RESET}
{Cor.NEGRITO}Escolha uma opção:{Cor.RESET}
1️⃣  Inserir nova ocorrência
2️⃣  Atender ocorrência prioritária
3️⃣  Listar ocorrências pendentes
4️⃣  Ver histórico de atendimentos
5️⃣  Gerar relatório por região
6️⃣  Gerar gráfico de severidade por região
7️⃣  Simular chamadas aleatórias
8️⃣  Simular chamadas com severidade crescente
9️⃣  Sair
""")
        op = input("👉 Sua escolha: ")
        if op == '1':
            r = input("Região: ")
            while True:
                try:
                    s = int(input("🔥 Severidade (1-10): "))
                    if 1 <= s <= 10:
                        break
                    else:
                        print(f"{Cor.VERMELHO}❌ Insira um valor entre 1 e 10.{Cor.RESET}")
                except ValueError:
                    print(f"{Cor.VERMELHO}❌ Valor inválido! Digite um número inteiro.{Cor.RESET}")
            d = input("📝 Descrição: ")
            sim.inserir_ocorrencia(r, s, d)
        elif op == '2':
            sim.atender_ocorrencia()
        elif op == '3':
            sim.listar_ocorrencias_pendentes()
        elif op == '4':
            sim.listar_historico()
        elif op == '5':
            sim.gerar_relatorio_por_regiao()
        elif op == '6':
            sim.gerar_grafico_severidade_por_regiao()
        elif op == '7':
            n = int(input("Número de chamadas a simular: "))
            sim.simular_chamadas(n)
        elif op == '8':
            n = int(input("Número de chamadas a simular: "))
            sim.simular_chamadas_crescentes(n)
        elif op == '9':
            print(f"{Cor.VERDE}👋 Encerrando o simulador. Até mais!{Cor.RESET}")
            break
        else:
            print(f"{Cor.VERMELHO}❌ Opção inválida. Tente novamente.{Cor.RESET}")

if __name__ == '__main__':
    menu()
