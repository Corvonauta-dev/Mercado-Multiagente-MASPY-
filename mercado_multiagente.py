# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃Sistema de Mercado Multiagente (MASPY)┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃Aluno: Luiz Guilherme Monteiro Padilha┃
# ┃RA: 1924745                           ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
# ┏━━━━━━━━━━━━━━━━━━━━━┓
# ┃Descrição do Sistema:┃
# ┣━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃- Ambiente (Mercado): orquestra o mercado, recebe pedidos de compra e registra vendas.                                  ┃
# ┃  Percepts:                                                                                                             ┃
# ┃    - pedido(comprador, item) — quando um comprador anuncia seu interesse.                                              ┃
# ┃    - comprador_desconectado(comprador) — quando um comprador finaliza ou desiste.                                      ┃
# ┃  Ações:                                                                                                                ┃
# ┃    - anunciar_pedido(comprador, item) — imprime o pedido e gera o percept “pedido”.                                    ┃
# ┃    - finalizar_venda(comprador, vendedor, item, qtde, preco) — imprime a venda e gera percept “comprador_desconectado”.┃
# ┃    - finalizar_comprador(comprador) — gera percept “comprador_desconectado” sem venda.                                 ┃
# ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┛
# ┃- Agente Comprador (CompradorAgent):                                                                   ┃
# ┃  Crenças iniciais:                                                                                    ┃
# ┃    - item_desejado, quantidade_desejada, preco_maximo, n_vendedores                                   ┃
# ┃  Objetivo inicial:                                                                                    ┃
# ┃    - anunciar_pedido — dispara o protocolo de compra.                                                 ┃
# ┃  Planos principais:                                                                                   ┃
# ┃    1) anunciar_pedido → chama Mercado.anunciar_pedido(...)                                            ┃
# ┃    2) trata_oferta → recebe “oferta”, decrementa n_vendedores e envia comprar/contra_oferta/Sem_acordo┃
# ┃    3) trata_finalizar → recebe “finalizar” e chama Mercado.finalizar_venda(...)                       ┃
# ┃    4) trata_sem_item → decrementa n_vendedores e encerra                                              ┃
# ┃    5) trata_sem_item_contra_oferta → decrementa n_vendedores e encerra                                ┃
# ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━┓
# ┃- Agente Vendedor (VendedorAgent):                                                                                   ┃
# ┃  Crenças iniciais:                                                                                                  ┃
# ┃    - n_compradores, margem, inventario                                                                              ┃
# ┃  Planos principais:                                                                                                 ┃
# ┃    1) trata_pedido → ao percept “pedido”, agenda fazer_oferta ou envia sem_item                                     ┃
# ┃    2) fazer_oferta → envia “oferta” ao comprador                                                                    ┃
# ┃    3) trata_compra → recebe “comprar”, atualiza estoque e envia “finalizar” ou “sem_item_contra_oferta”             ┃
# ┃    4) trata_contra_oferta → recebe “contra_oferta”, calcula desconto e envia “finalizar” ou “sem_item_contra_oferta”┃
# ┃    5) trata_comprador_desconectado → decrementa n_compradores e encerra quando zero                                 ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
# ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃Protocolo de Negociação:┃
# ┣━┳━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃1┃ Anúncio de Pedido:                                                                ┃
# ┣━┛ - CompradorAgent anunciaa pedido.                                                 ┃
# ┃   - Mercado cria Percept("pedido", [comprador, item]) para todos os vendedores.     ┃
# ┣━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
# ┃2┃ Oferta do Vendedor:                                                               ┃
# ┣━┛ - Cada VendedorAgent percebe o pedido e dispara o plano "trata_pedido".           ┃
# ┃   - Se tiver estoque, faz uma oferta.                                               ┃
# ┃   - No plano "fazer_oferta, o vendedor envia ao comprador a oferta.                 ┃
# ┣━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
# ┃3┃ Avaliação da Oferta:                                                              ┃
# ┣━┛ - CompradorAgent recebe a oferta e executa o plano "trata_oferta".                ┃
# ┃   - Compara quantidade e preço:                                                     ┃
# ┃       – Se qtd_disp ≥ qtd_desejada e preço ≤ preco_maximo:                          ┃
# ┃           envia "comprar" ao vendedor                                               ┃
# ┃       – Se qtd_disp ≥ qtd_desejada mas preço > preco_maximo:                        ┃
# ┃           envia contra_oferta ao vendedor                                           ┃
# ┃       – Se qtd_disp < qtd_desejada:                                                 ┃
# ┃           envia Sem_acordo ao vendedor                                              ┃
# ┣━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
# ┃4┃ Tratamento da Compra:                                                             ┃
# ┣━┛ - VendedorAgent recebe comprar e executa o plano trata_compra.                    ┃
# ┃   - Se ainda houver estoque, reduz inventário e envia finalizar ao comprador:       ┃
# ┃     caso contrário, envia sem_item_contra_oferta ao comprador:                      ┃
# ┣━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
# ┃5┃ Contra-Oferta:                                                                    ┃
# ┣━┛ - VendedorAgent recebe contra_oferta e executa o plano trata_contra_oferta        ┃
# ┃   - Calcula margem de desconto:                                                     ┃
# ┃     - Desconto = valor * (1 - margem)                                               ┃
# ┃     – Se desconto ≤ preco_maximo: envia "finalizar" com preço negociado.            ┃
# ┃     – Caso contrário: envia que não pode dar desconto.                              ┃
# ┣━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
# ┃6┃ Finalização e Desconexão:                                                         ┃
# ┣━┛ - Após enviar finalizar, o CompradorAgent dispara trata_finalizar,                ┃
# ┃     executa a ação finalizar_venda no mercado e termina seu ciclo.                  ┃
# ┃   - Mercado cria Percept("comprador_desconectado", comprador).                      ┃
# ┃   - VendedorAgent recebe esse percept e dispara o plano trata_comprador_desconectado┃
# ┃     decrementa n_compradores e, se chegar a zero, termina seu ciclo.                ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

from maspy import *
import random

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃1. DICIONÁRIO GLOBAL DE ITENS┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
ITENS_PRECOS = {
    "Armadura Acolchoada": 1.0,
    "Armadura de Couro": 2.0,
    "Armadura de Couro batido": 3.0,
    "Camisa de Malha": 5.0,
    "Gibão de Peles": 2.0,
    "Cota de Escamas": 4.0,
    "Cota de Malha": 6.0,
    "Placa de Peitoral": 8.0,
    "Cota de Talas": 13.0,
    "Meia Armadura": 18.0,
    "Armadura Completa": 30.0
}

# ┏━━━━━━━━━━━━━━━━━━━━┓
# ┃2. AMBIENTE: Mercado┃
# ┗━━━━━━━━━━━━━━━━━━━━┛
class Mercado(Environment):
    def __init__(self, env_name="Mercado"):
        super().__init__(env_name)

    def anunciar_pedido(self, comprador, item):
        # Imprime o pedido do comprador e gera um percept "pedido" para os vendedores.
        self.print(f"{comprador} deseja comprar: {item}")
        self.create(Percept("pedido", [comprador, item]))

    def finalizar_venda(self, comprador, vendedor, item, qtde, preco):
        # Imprime a conclusão da venda e gera o percept "comprador_desconectado".
        total = qtde * preco
        self.print(
            f"Venda: {comprador} comprou {qtde} x {item} de {vendedor} "
            f"por {preco} po cada, totalizando {total:.2f} Po"
        )
        self.create(Percept("comprador_desconectado", comprador))

    def finalizar_comprador(self, comprador):
        # Gera o percept "comprador_desconectado" sem registro de venda.
        # Usado quando o comprador desiste ou esgota opções.
        self.create(Percept("comprador_desconectado", comprador))


# ┏━━━━━━━━━━━━━━━━━━━┓
# ┃3. AGENTE COMPRADOR┃
# ┗━━━━━━━━━━━━━━━━━━━┛
class CompradorAgent(Agent):
    def __init__(self, nome, item, quantidade, preco_maximo, n_vendedores):
        super().__init__(nome)
        # crenças iniciais
        self.add(Belief("item_desejado", item))
        self.add(Belief("quantidade_desejada", quantidade))
        self.add(Belief("preco_maximo", preco_maximo))
        self.add(Belief("n_vendedores", n_vendedores))
        # objetivo inicial
        self.add(Goal("anunciar_pedido"))

    @pl(gain, Goal("anunciar_pedido"))
    def anunciar_pedido(self, src):
        
        # Plano 1: Anunciar pedido ao Mercado.
        # Gatilho: Goal "anunciar_pedido".
        
        item = self.get(Belief("item_desejado", Any))
        if item:
            # publica interesse no mercado
            self.action("Mercado").anunciar_pedido(self.my_name, item.args)
        else:
            # não tem item desejado -> encerra
            self.print("comprador sem item desejado")
            self.action("Mercado").finalizar_comprador(self.my_name)
            self.stop_cycle()

    @pl(gain, Goal("oferta", Any))
    def trata_oferta(self, src, oferta):
        
        # Plano 2: Tratar mensagem de oferta de um vendedor.
        # Decrementa n_vendedores e escolhe entre comprar, contra_oferta ou Sem_acordo.
        
        vendedor, qtd_disp, valor_unit = oferta
        qtd_desejada = self.get(Belief("quantidade_desejada", Any)).args
        p_max = self.get(Belief("preco_maximo", Any)).args
        item = self.get(Belief("item_desejado", Any)).args

        # decrementa número de vendedores pendentes
        ref = self.get(Belief("n_vendedores", Any))
        n_vend = ref.args - 1
        self.rm(ref)
        self.add(Belief("n_vendedores", n_vend))

        self.print(f"{self.my_name} recebeu oferta de {vendedor}: "
                   f"{qtd_disp}x{item} a {valor_unit} Po")

        if qtd_desejada and qtd_disp >= qtd_desejada:
            if valor_unit <= p_max:
                # aceita
                self.send(vendedor, achieve, Goal("comprar", [self.my_name, item, qtd_desejada, valor_unit]), "Acordos")
            else:
                # contra-oferta de preço
                self.print(f"{self.my_name} negocia preço para {item}: até {p_max} Po")
                self.send( vendedor, achieve, Goal("contra_oferta", [self.my_name, item, qtd_desejada, valor_unit, p_max]), "Acordos")
        else:
            # sem acordo de quantidade
            self.print(f"Sem acordo: {vendedor} só tem {qtd_disp}, "f"desejo {qtd_desejada}")
            if n_vend <= 0:
                # último vendedor -> encerra
                self.action("Mercado").finalizar_comprador(self.my_name)
                self.stop_cycle()

    @pl(gain, Goal("finalizar", Any))
    def trata_finalizar(self, src, compra):
        
        # Plano 3: Finalizar compra com o vendedor.
        # Chama o ambiente e encerra.
        
        vendedor, item, qtd, valor = compra
        self.action("Mercado").finalizar_venda(self.my_name, vendedor, item, qtd, valor)
        self.stop_cycle()

    @pl(gain, Goal("sem_item", Any))
    def trata_sem_item(self, src, vendedor):
        
        # Plano 4: Vendedor não tem o item.
        # Decrementa n_vendedores; encerra se não restar nenhum.
        
        ref = self.get(Belief("n_vendedores", Any))
        n_vend = ref.args - 1
        self.rm(ref)
        self.add(Belief("n_vendedores", n_vend))
        if n_vend <= 0:
            self.action("Mercado").finalizar_comprador(self.my_name)
            self.stop_cycle()

    @pl(gain, Goal("sem_item_contra_oferta", Any))
    def trata_sem_item_contra_oferta(self, src, vendedor):
        
        # Plano 5: Nenhuma oferta viável após negociação.
        # Encerra se todos os vendedores foram consultados.
        
        if self.get(Belief("n_vendedores", Any)).args <= 0:
            self.action("Mercado").finalizar_comprador(self.my_name)
            self.stop_cycle()


# ┏━━━━━━━━━━━━━━━━━━┓
# ┃4. AGENTE VENDEDOR┃
# ┗━━━━━━━━━━━━━━━━━━┛
class VendedorAgent(Agent):
    def __init__(self, nome, n_compradores):
        super().__init__(nome)
        # crenças iniciais
        self.add(Belief("n_compradores", n_compradores))
        self.add(Belief("margem", random.uniform(0.1, 0.5)))

        # inventário inicial: itens aleatórios
        sel = random.sample(list(ITENS_PRECOS.keys()), random.randint(1, 5))
        inv = {item: [random.randint(1, 10), ITENS_PRECOS[item]] for item in sel}
        self.add(Belief("inventario", inv))

    @pl(gain, Belief("pedido", Any))
    def trata_pedido(self, src, pedido):
        
        # Plano 1: Chegou um pedido do comprador.
        # Se existe no inventário, agenda oferta; senão envia sem_item.
        
        comprador, item = pedido
        inventario = self.get(Belief("inventario", Any)).args

        if item in inventario:
            qtd_disp, preço = inventario[item]
            self.print(f"{self.my_name} recebeu pedido de {comprador} para {item}")
            self.add(Goal("fazer_oferta", [comprador, item, qtd_disp, preço]))
        else:
            self.send(comprador, achieve, Goal("sem_item", self.my_name), "Acordos")

    @pl(gain, Goal("fazer_oferta", Any))
    def fazer_oferta(self, src, args):
        
        # Plano 2: Envia oferta ao comprador, se ainda ativo.
        
        comprador, item, qtd, valor = args
        if Admin().running_class_agents(comprador):
            self.print( f"Oferta: {self.my_name} -> {comprador} | "f"{qtd}x {item} @ {valor} Po")
            self.send(comprador, achieve, Goal("oferta", [self.my_name, qtd, valor]),"Acordos")
        else:
            # comprador já encerrou, responde sem_item
            self.send(comprador, achieve, Goal("sem_item", self.my_name), "Acordos")

    @pl(gain, Goal("comprar", Any))
    def trata_compra(self, src, compra):
        
        # Plano 3: Comprador aceitou a oferta.
        # Se há estoque suficiente, envia finalizar; senão sem_item_contra_oferta.
        
        comprador, item, qtd, valor = compra
        inventario = self.get(Belief("inventario", Any)).args

        if Admin().running_class_agents(comprador):
            if item in inventario and qtd <= inventario[item][0]:
                inventario[item][0] -= qtd
                self.send(comprador, achieve, Goal("finalizar", [self.my_name, item, qtd, valor]), "Acordos")
            else:
                self.print(f"{self.my_name} sem estoque para {qtd}x {item}")
                self.send(comprador, achieve, Goal("sem_item_contra_oferta", self.my_name),"Acordos")

    @pl(gain, Goal("contra_oferta", Any))
    def trata_contra_oferta(self, src, compra):
        
        # Plano 4: Comprador propõe preço menor.
        # Calcula desconto e aceita ou recusa.
        
        comprador, item, qtd, valor, p_max = compra
        inventario = self.get(Belief("inventario", Any)).args
        margem = self.get(Belief("margem", Any)).args
        desconto = valor * (1 - margem)

        if (item in inventario and qtd <= inventario[item][0]
            and Admin().running_class_agents(comprador)):
            self.print(f"{self.my_name} pode dar até {margem*100:.0f}% de desconto "f"(mín {desconto:.2f} Po)")
            if desconto <= p_max:
                # aceita a contra-oferta
                self.send( comprador, achieve,  Goal("finalizar", [self.my_name, item, qtd, p_max]), "Acordos")
            else:
                # recusa: sem_item_contra_oferta
                self.print(f"{self.my_name} rejeita desconto para {item}")
                self.send( comprador, achieve, Goal("sem_item_contra_oferta", self.my_name), "Acordos")
        else:
            # sem estoque ou comprador inativo
            self.print(f"{self.my_name} sem estoque/inativo para {item}")
            self.send(comprador, achieve,  Goal("sem_item_contra_oferta", self.my_name),"Acordos")

    @pl(gain, Belief("comprador_desconectado", Any))
    def trata_comprador_desconectado(self, src, comprador):
        
        # Plano 5: Atualiza contador de compradores finalizados.
        # Encerra quando atingir zero.
        
        ref = self.get(Belief("n_compradores", Any))
        n = ref.args - 1
        self.rm(ref)
        self.add(Belief("n_compradores", n))
        if n <= 0:
            self.stop_cycle()

# ┏━━━━━━━━━━━━━━━━━━━━━━┓
# ┃5. EXECUÇÃO DO SISTEMA┃
# ┗━━━━━━━━━━━━━━━━━━━━━━┛
if __name__ == "__main__":
    # cria ambiente e canal de comunicação
    canal = Channel("Acordos")
    mercado = Mercado("Mercado")

    # parâmetros: quantos compradores e vendedores
    num_compradores = 10
    num_vendedores = 10

    # instancia agentes compradores
    compradores = [
        CompradorAgent(
            f"Comprador{i}",
            random.choice(list(ITENS_PRECOS.keys())),
            random.randint(1, 10),
            random.randint(1, 40),
            num_vendedores
        )
        for i in range(1, num_compradores + 1)
    ]

    # instancia agentes vendedores
    vendedores = [
        VendedorAgent(f"Vendedor{j}", num_compradores)
        for j in range(1, num_vendedores + 1)
    ]

    # conecta todos ao ambiente e inicia
    Admin().connect_to(compradores + vendedores, [canal, mercado])
    Admin().start_system()
