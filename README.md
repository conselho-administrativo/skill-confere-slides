# /confere-slides

Confere se a **apresentação de slides** de um(a) candidato(a) diz a mesma coisa que a
**Proposta Final** que ele(a) entregou — Edital de Candidatura 2027 da **Empresa Júnior
ADM UFBA**. Mantida pelo Conselho Administrativo.

Serve ao candidato, antes de mandar os slides, e ao Conselho, ao receber.

> **Enxugar é permitido. Mudar não é.**
>
> A proposta é um documento completo, sem limite de páginas. A apresentação tem 15 minutos
> (Código Eleitoral, Art. 56º §3º). Resumir, reescrever, juntar tópicos, virar gráfico,
> cortar exemplo — tudo isso é esperado. O que a skill procura é outra coisa: número que
> trocou de valor, meta que mudou, indicador substituído, compromisso diferente,
> diagnóstico invertido, conteúdo que aparece no slide e não está na proposta.

---

## Por que isso importa

A Proposta é **pública para todos os membros desde o momento em que chega no canal oficial**
(Art. 16º), e o membro tem o dever de examiná-la e formar juízo próprio antes de votar
(Art. 75º III e IV). As perguntas da sabatina são escritas sobre ela e enviadas antes
(Art. 59º).

Se a apresentação disser outra coisa, o membro se preparou sobre uma base e vota sobre
outra. É esse o problema que a skill ajuda a evitar — de preferência antes de alguém subir
para apresentar.

---

## Os dois documentos

| | O quê | Prazo | Canal | É entrega? |
|---|---|---|---|---|
| **A** | **Proposta Final** — documento completo, PDF | 22/11 às 23:59 | e-mail oficial, **respondendo a todos** | **Sim** (Art. 37º) |
| **B** | **Apresentação** — os slides do dia | até o dia anterior à apresentação (Art. 56º §6º) | **direto ao Conselho** | **Não** |

**Enviar os slides não cumpre o prazo de 22/11.** As entregas do processo são três e os
slides não estão entre elas (Art. 37º); os slides são o material da apresentação.

---

## Instalar

**Pelo ZIP.** Baixe em
**[Code → Download ZIP](https://github.com/conselho-administrativo/skill-confere-slides/archive/refs/heads/main.zip)**,
descompacte e ponha a pasta — com o nome **`confere-slides`** — em:

| Sistema | Onde |
|---|---|
| Windows | `%USERPROFILE%\.claude\skills\confere-slides` |
| macOS e Linux | `~/.claude/skills/confere-slides` |

**Por git**, se quiser receber as correções com um comando:

```bash
git clone https://github.com/conselho-administrativo/skill-confere-slides.git ~/.claude/skills/confere-slides
```

```bash
git -C ~/.claude/skills/confere-slides pull
```

Depois é só mandar os dois PDFs e pedir a conferência — ou chamar `/confere-slides`.

**Em ChatGPT ou Gemini sem suporte a skills:** crie um Projeto ou um Gem, cole o conteúdo do
`SKILL.md` nas instruções e anexe os arquivos de `referencias/`. Sem terminal você não tem o
inventário automático; compense conferindo os números com mais cuidado.

---

## O que ela faz

| | |
|---|---|
| **Compara por teor** | número, meta, indicador, plano, calendário, diagnóstico, argumento, escopo |
| **Inventário objetivo** | `ferramentas/inventario.py` extrai todo número e data dos dois PDFs e aponta as prováveis trocas |
| **Laudo item a item** | cada divergência com os dois trechos citados e a página de cada um |
| **Segundo modo** | Análise Crítica × Proposta, que o Art. 56º §1º exige |

## O que ela não faz

- **Não avalia a proposta.** Laudo limpo quer dizer apresentação fiel ao que foi entregue —
  não quer dizer proposta boa. Qualidade é mérito, e mérito é de cada eleitor(a) no momento
  de votar (Art. 7º X).
- **Não cria consequência.** Divergência entre slides e proposta não está no rol do Art. 108º
  nem na hipótese do Art. 39º. A skill relata; quem decide é o Conselho.
- **Não compara candidatos diferentes.** Os slides vão só para o Conselho e não circulam.
- **Não reescreve** a proposta nem os slides.
- **Não tira dúvidas do edital.** Para regra, prazo, elegibilidade, votação ou recurso, use a
  **[/edital2027](https://github.com/conselho-administrativo/skill-edital2027)**.

---

## Usar

```bash
python ferramentas/inventario.py PROPOSTA.pdf SLIDES.pdf
```

Roda sozinho e já serve de primeira camada: lista os números dos dois lados, as prováveis
trocas de valor, o que só aparece nos slides e os períodos do calendário que não batem.
Precisa de `pymupdf` ou `pypdf`.

Depois, com a skill carregada, peça o laudo completo — ela lê os dois documentos e compara
também o que o inventário não vê: diagnóstico, argumento e escopo.

**Se os slides forem exportados como imagem** (Canva, Figma, "salvar como imagem"), não há
texto para extrair. A skill avisa e passa a ler as páginas visualmente, registrando no laudo
que a conferência foi parcial.

---

## Estrutura

```
SKILL.md                      orquestrador — a assimetria, as oito travas, o procedimento
referencias/
  criterios.md                o que é divergência e o que não é
  extrair-e-comparar.md       extração, falha de extração, como alinhar as seções
  formato-do-laudo.md         a saída padrão
  contexto-normativo.md       só o que ancora: prazos, canais, Art. 56º
ferramentas/
  inventario.py               números e datas dos dois PDFs, com as prováveis trocas
testes/
  portao.py                   checagens de integridade, exit 1 se falhar
  casos-dourados.md           casos de conferência do comportamento
```

---

## Manter

O conteúdo normativo é congelado entre a abertura da demonstração de interesse e a
proclamação dos resultados (Art. 124º §1º). No período só entram **erratas** — correção de
informação, sem mudança de regra (Art. 124º §2º) —, registradas no `CHANGELOG.md`.

**Publicar errata exige duas ações:** `git push` **e** avisar quem instalou por ZIP, porque
essa cópia não se atualiza sozinha.

Antes de publicar: `python testes/portao.py` e os casos dourados.

---

Conselho Administrativo 2026 — Gisele Silva da Encarnação e João Pedro da Paz Souza
**conselho1@empresajr.org**
