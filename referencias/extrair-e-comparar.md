# Extrair o texto e alinhar os documentos

## 1. Extração

**Se você tem terminal** (Claude Code, Codex, Gemini CLI), rode primeiro o inventário — ele
já extrai, conta e compara os números:

```bash
python ferramentas/inventario.py PROPOSTA.pdf SLIDES.pdf
```

Para ler o texto corrido de um PDF:

```bash
python -c "import fitz,sys; d=fitz.open(sys.argv[1]); [print(f'--- p.{i+1} ---'); print(p.get_text()) for i,p in enumerate(d)]" ARQUIVO.pdf
```

**Se você não tem terminal** (Claude, ChatGPT ou Gemini pela interface), leia os dois PDFs
anexados diretamente. Nesse caso você não tem o inventário: compense sendo mais cuidadoso
com os números, e **anote a página de cada citação enquanto lê** — voltar depois para achar
a página custa mais do que anotar na hora.

## 2. Quando a extração falha

O caso mais comum deste edital: **slides exportados como imagem**. Canva, Figma e
PowerPoint "salvar como imagem" produzem PDFs sem camada de texto. Sinais:

- o inventário avisa que a maioria das páginas está vazia;
- o PDF tem muitas páginas e quase nenhum caractere.

Quando isso acontece: **leia as páginas visualmente, uma a uma**, e registre no laudo que a
conferência foi visual e é parcial. Veja o bloco "Quando não dá para conferir" em
`formato-do-laudo.md`. Não finja que a comparação automática valeu.

Se o problema for do lado da proposta, peça o arquivo original — proposta tem de ser
**integralmente legível** `(Art. 38º)`, e um PDF sem texto já é um problema anterior ao seu.

## 3. Alinhar as seções

Os dois documentos não têm a mesma estrutura, e tentar casar página com página não funciona:
a proposta tem capítulos, os slides têm uma ideia por tela.

Construa um mapa por **assunto**, não por posição. Os assuntos previsíveis, porque o
`Art. 56º` os exige da proposta:

| Assunto | Onde costuma estar na proposta | Onde costuma estar nos slides |
|---|---|---|
| Diagnóstico da área, gaps | primeiros capítulos | 1 a 3 slides iniciais |
| Estratégia retomada da Análise Crítica `(Art. 56º §1º)` | logo após o diagnóstico | slide de "direcionamento" |
| Planos de ação `(Art. 56º I)` | corpo principal | o maior bloco de slides |
| Calendário `(Art. 56º II)` | capítulo próprio ou tabela | 1 slide, quase sempre linha do tempo |
| Indicadores e metas `(Art. 56º III e §5º)` | capítulo próprio | 1 ou 2 slides, ou rodapé dos planos |

Monte o mapa antes de comparar, e **use-o para procurar**: quando um conteúdo do slide não
aparecer na seção equivalente da proposta, procure nos outros capítulos antes de marcar
`NOVO`. Conteúdo que migra de capítulo é o erro mais provável do laudo.

## 4. Ordem de trabalho

1. **Números** — do inventário. É o chão objetivo, e a troca de meta é o achado mais sério.
2. **Indicadores** — o que está sendo medido mudou? `(Art. 56º §5º)`
3. **Planos de ação** — cada plano do slide existe na proposta? O inverso não importa.
4. **Calendário** — o que estava no segundo trimestre continua no segundo trimestre?
5. **Diagnóstico e argumento** — a leitura da área e o porquê de cada plano.
6. **Escopo** — a promessa recai sobre as mesmas pessoas e as mesmas áreas?

Os passos 1 a 4 são quase mecânicos. Os passos 5 e 6 são onde mora a mudança silenciosa —
aquela em que todas as palavras parecem familiares e a afirmação é outra. Faça-os com os
dois textos lado a lado, não de memória.

## 5. Economia de leitura

Proposta de 40 páginas e 25 slides não cabem confortavelmente de uma vez. Ordem que
funciona:

1. Leia **os slides inteiros** primeiro — são curtos e definem o que precisa ser procurado.
2. Para cada afirmação dos slides, procure a correspondente na proposta.
3. Só então percorra a proposta atrás das omissões relevantes.

Assim você lê a proposta orientado por perguntas, em vez de tentar memorizá-la.
