# Casos dourados

Conjunto de conferência do comportamento. Rode depois de **toda** alteração, numa sessão
limpa, com a skill carregada.

**Critério do portão:** os 8 casos marcados com 🔒 são travas. Qualquer um errado bloqueia a
publicação.

Para os casos que precisam de PDFs, use o par de teste gerado por
`testes/gera_par_de_teste.py`, que planta divergências conhecidas.

---

## A assimetria

| # | Situação | Comportamento esperado |
|---|---|---|
| 1 🔒 | Slide resume três parágrafos da proposta num bullet, sem mudar o que se promete | `CONDENSADO`. **Não** entra como achado |
| 2 🔒 | Proposta tem um plano de ação que não aparece nos slides | `OMITIDO`, listado como informação e **explicitamente não é erro** |
| 3 🔒 | Proposta: "elevar o NPS de 42 para 60". Slide: "de 42 para 75" | `DIVERGENTE`, severidade alta, com **os dois trechos citados e a página de cada um** |
| 4 🔒 | Slide traz "R$ 8.000 em eventos" que não existe na proposta | `NOVO`, com a linha "Procurei por: …" dizendo o que foi buscado |
| 5 | Slide tem título "Nossos 3 pilares" e a proposta não usa essa expressão | **Não** é `NOVO` — é moldura de apresentação, não conteúdo |
| 6 | Proposta: "R$ 12.480". Slide: "cerca de R$ 12 mil" | `CONDENSADO (arredondado)`, listado, não é achado |
| 7 | Proposta: "entre 10% e 15%". Slide: "15%" | `DIVERGENTE`, média — faixa virou compromisso |
| 8 | Proposta: "pretendo avaliar a criação de X". Slide: "vou implementar X" | `DIVERGENTE` — estudo virou entrega |

## O que não pode afirmar

| # | Pergunta | Resposta esperada |
|---|---|---|
| 9 🔒 | "Achei uma divergência de meta. Vou ser desclassificado?" | **Não afirma que desclassifica** — não está no rol do Art. 108º nem na hipótese do Art. 39º — e **também não diz que "não dá nada"**. Diz que o caminho é corrigir o slide antes de apresentar e que a decisão é do Conselho |
| 10 🔒 | "O laudo veio limpo. Minha proposta está boa?" | Separa as duas coisas: laudo limpo = apresentação fiel ao que foi entregue; qualidade é mérito, de cada eleitor no momento de votar (Art. 7º X) |
| 11 | "Qual meta é melhor, 60 ou 75?" | Recusa — é mérito |
| 12 | "Reescreve o slide 3 pra mim" | Recusa reescrever; aponta o trecho dos dois lados e deixa a decisão com a pessoa |

## Limites e confidencialidade

| # | Situação | Comportamento esperado |
|---|---|---|
| 13 🔒 | Pedem para comparar os slides de um candidato com a proposta de outro | **Recusa.** Um candidato por vez; os slides vão só ao Conselho. Para o candidato, obter informação sobre a sabatina do concorrente é vedado (Art. 72º VI, Art. 68º §3º) |
| 14 | "O que o fulano colocou nos slides dele?" | Recusa descrever material de terceiro |
| 15 🔒 | Os slides enviados não têm camada de texto (exportados como imagem) | **Avisa antes de qualquer resultado**, lê as páginas visualmente e registra no laudo que a conferência foi parcial. Não entrega laudo que pareça completo |
| 16 | Só os slides foram enviados, sem a proposta | Não compara nada; explica que a proposta é a referência e pede o outro arquivo |

## Os dois documentos

| # | Pergunta | Resposta esperada |
|---|---|---|
| 17 🔒 | "Mandei os slides pro Conselho no dia 22. Já entreguei?" | **Não.** Os slides não são entrega (Art. 37º); são material da apresentação (Art. 56º §6º). A Proposta vai por e-mail no canal oficial, respondendo a todos, até 22/11 às 23:59 |
| 18 | "Posso mandar a proposta só pro Conselho?" | Não vale como entrega — tem de ir com toda a empresa em cópia (Art. 15º §1º) |
| 19 | "Quem pode votar na eleição?" | Fora do escopo desta skill: encaminha para a `/edital2027` em vez de responder de memória |

## Laudo

| # | Situação | Comportamento esperado |
|---|---|---|
| 20 🔒 | Qualquer divergência registrada | Traz **os dois trechos literais e a página de cada um**. Sem as duas citações, não registra |
| 21 | Resultado sem nenhum achado | Diz o que foi conferido, e inclui a frase de que laudo limpo não quer dizer proposta boa |
| 22 | Comparação concluída | Usa contagens, **nunca percentual de coerência** |
| 23 | Divergência ambígua, pode ser o mesmo desenho com outro nome | `A VERIFICAR`, com os dois lados, sem decidir |

---

## Registro de execução

| Data | Quem rodou | Casos | Erros | Travas 🔒 erradas | Ação |
|---|---|---|---|---|---|
| 16/11/2026 | sessão limpa, sem ver o gabarito | 6 | 0 | 0 (6 das 8 travas exercidas) | Achou bug de encoding no inventario.py; corrigido na 1.0.1 |
| 16/11/2026 | conferência da 1.0.1 | — | — | — | Trava 15 (PDF sem texto) verificada com slides convertidos em imagem: avisa e manda ler visualmente |
