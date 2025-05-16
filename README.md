# Mercado Multiagente (MASPY)

Este repositório foi criado para armazenar uma simulação de mercado baseada em um sistema multiagente utilizando a biblioteca <a href="https://corvonauta-dev.github.io/projeto-listagem-pokemon/">MASPY</a> (Multi-Agent Systems in Python). O projeto foi desenvolvido utilizando conceitos de Agentes BDI (Belief-Desire-Intention), com interações dinâmicas entre vendedores e compradores sem intervenção humana.

## Detalhes do projeto

* **Linguagem e Framework:** Python com MASPY (versão 0.6.0)

## O Problema

O objetivo é simular um mercado automatizado em que múltiplos vendedores e compradores interagem dinamicamente, realizando ofertas, contra-ofertas e negociações até a finalização ou desistência das transações.

## Descrição do Sistema

### Ambiente (Mercado)

* **Função:** Orquestrar o mercado, recebe pedidos de compra e registra vendas.
* **Percepts:**

  * `pedido(comprador, item)` — gerado quando um comprador anuncia seu interesse.
  * `comprador_desconectado(comprador)` — gerado quando um comprador finaliza ou desiste.
* **Ações:**

  * `anunciar_pedido(comprador, item)` — imprime o pedido e gera o percept "pedido".
  * `finalizar_venda(comprador, vendedor, item, qtde, preco)` — imprime a venda e gera percept "comprador\_desconectado".
  * `finalizar_comprador(comprador)` — gera percept "comprador\_desconectado" sem venda.

### Agente Comprador (CompradorAgent)

* **Crenças iniciais:**

  * `item_desejado`, `quantidade_desejada`, `preco_maximo`, `n_vendedores`
* **Objetivo inicial:**

  * `anunciar_pedido` — dispara o protocolo de compra.
* **Planos principais:**

  1. `anunciar_pedido` → chama `Mercado.anunciar_pedido(...)`
  2. `trata_oferta` → recebe "oferta", decrementa `n_vendedores` e envia `comprar`/`contra_oferta`/`Sem_acordo`
  3. `trata_finalizar` → recebe "finalizar" e chama `Mercado.finalizar_venda(...)`
  4. `trata_sem_item` → decrementa `n_vendedores` e encerra
  5. `trata_sem_item_contra_oferta` → decrementa `n_vendedores` e encerra

### Agente Vendedor (VendedorAgent)

* **Crenças iniciais:**

  * `n_compradores`, `margem`, `inventario`
* **Planos principais:**

  1. `trata_pedido` → ao percept "pedido", agenda `fazer_oferta` ou envia `sem_item`
  2. `fazer_oferta` → envia "oferta" ao comprador
  3. `trata_compra` → recebe "comprar", atualiza estoque e envia "finalizar" ou "sem\_item\_contra\_oferta"
  4. `trata_contra_oferta` → recebe "contra\_oferta", calcula desconto e envia "finalizar" ou "sem\_item\_contra\_oferta"
  5. `trata_comprador_desconectado` → decrementa `n_compradores` e encerra quando zero

## Funcionamento do sistema

1. **Anúncio de Pedido:**

   * CompradorAgent anuncia pedido.
   * Mercado cria `Percept("pedido", [comprador, item])` para todos os vendedores.

2. **Oferta do Vendedor:**

   * Cada VendedorAgent percebe o pedido e dispara o plano `trata_pedido`.
   * Se tiver estoque, faz uma oferta.
   * No plano `fazer_oferta`, o vendedor envia ao comprador a oferta.

3. **Avaliação da Oferta:**

   * CompradorAgent recebe a oferta e executa o plano `trata_oferta`.
   * Compara quantidade e preço:

     * Se qtd\_disp ≥ qtd\_desejada e preço ≤ preco\_maximo: envia "comprar" ao vendedor
     * Se qtd\_disp ≥ qtd\_desejada mas preço > preco\_maximo: envia "contra\_oferta" ao vendedor
     * Se qtd\_disp < qtd\_desejada: envia "Sem\_acordo" ao vendedor

4. **Tratamento da Compra:**

   * VendedorAgent recebe "comprar" e executa o plano `trata_compra`.
   * Se ainda houver estoque, reduz inventário e envia "finalizar" ao comprador.
   * Caso contrário, envia "sem\_item\_contra\_oferta" ao comprador.

5. **Contra-Oferta:**

   * VendedorAgent recebe "contra\_oferta" e executa o plano `trata_contra_oferta`.
   * Calcula margem de desconto:

     * Desconto = valor \* (1 - margem)
     * Se desconto ≤ preco\_maximo: envia "finalizar" com preço negociado.
     * Caso contrário: informa que não pode dar desconto.

6. **Finalização e Desconexão:**

   * Após enviar "finalizar", o CompradorAgent dispara `trata_finalizar`, executa a ação `finalizar_venda` no mercado e termina seu ciclo.
   * Mercado cria `Percept("comprador_desconectado", comprador)`.
   * VendedorAgent recebe esse percept e dispara o plano `trata_comprador_desconectado`, decrementa `n_compradores` e, se chegar a zero, termina seu ciclo.
