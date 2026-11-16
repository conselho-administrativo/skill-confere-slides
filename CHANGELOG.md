# Changelog

Registro de alterações da skill `/confere-slides`.

Durante o ciclo — entre a abertura da demonstração de interesse e a proclamação dos
resultados — só entram **erratas**: correção de informação já divulgada, sem mudança de
regra (Código Eleitoral, Art. 124º §2º). Cada errata registra **o que mudou e a data**, na
forma do Art. 18º.

**Publicar errata exige duas ações:** `git push` **e** avisar quem instalou por ZIP, porque
essa cópia não se atualiza sozinha.

---

## [1.0.1] — 2026-11-16

**Errata.** Correção de bug, sem mudança de regra nem de critério.

### Corrigido
- **`ferramentas/inventario.py` quebrava no Windows.** O console usa cp1252 e o script
  morria com `UnicodeEncodeError` ao imprimir o aviso da seção de períodos, saindo com
  código 1 — justamente a seção que sinaliza período de calendário citado num documento e
  não no outro. Os acentos das seções anteriores também saíam corrompidos.

  Duas correções: `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` no início do
  `main()`, e troca de todo emoji por marcador ASCII `[!]`. O script agora roda com exit 0
  no console cru do Windows, sem precisar de `PYTHONIOENCODING`.

  Achado em teste de comportamento em sessão limpa, não em revisão. Como o público é
  majoritariamente Windows e o README manda rodar a ferramenta como primeira camada, o bug
  atingiria quase todo mundo logo no primeiro uso.

### Verificado no mesmo teste
- As três divergências plantadas no par de teste foram detectadas, sem falso positivo:
  meta de NPS 60→75, retenção 78%→90% e um valor que só existe no slide.
- As duas armadilhas foram evitadas: diagnóstico encurtado ficou como condensação, e
  período ausente do slide ficou como omissão — nenhum dos dois virou achado.
- Detecção de PDF sem camada de texto confirmada com slides convertidos em imagem: avisa
  antes de qualquer resultado e manda ler visualmente.

---

## [1.0.0] — 2026-11-16

Primeira versão. Ciclo 2027, para a etapa Proposta Final e Sabatina.

### O problema que ela resolve
A Proposta Final é um documento completo, entregue em 22/11 a toda a Empresa, e a
apresentação do dia da sabatina é necessariamente mais curta — 15 minutos (Art. 56º §3º).
Condensar é esperado. O risco é outro: que a versão falada mude o que foi escrito, e o
membro que leu a proposta e preparou perguntas sobre ela (Art. 59º, Art. 75º III e IV) vote
sobre uma base diferente da que examinou.

### Conteúdo
- **A assimetria** como regra central: omitir e resumir é permitido; trocar número, meta,
  indicador, compromisso, diagnóstico, argumento ou escopo é achado. Cinco vereditos —
  `MANTIDO`, `CONDENSADO`, `OMITIDO`, `DIVERGENTE`, `NOVO`.
- **Oito travas**, entre elas: comparar teor e não palavra; citar os dois lados de toda
  divergência, com página, sob pena de não ser achado; não avaliar qualidade; não inventar
  consequência; um candidato por vez; na dúvida listar em vez de decidir.
- **`ferramentas/inventario.py`** — extrai número, percentual, valor, data e período dos
  dois PDFs e aponta as prováveis trocas de valor, ranqueadas por contexto em comum, mesmo
  tipo e desaparecimento do valor original. Detecta e avisa quando um PDF não tem camada de
  texto, caso comum em slides exportados como imagem.
- **Laudo padronizado**, com contagens e sem percentual, e com a frase obrigatória de que
  laudo limpo não quer dizer proposta boa.
- **Segundo modo**: Análise Crítica × Proposta, coerência que o Art. 56º §1º exige.
- **Portão** com 8 checagens e casos dourados de comportamento.

### Decisões de construção
- **Omissão nunca é achado.** Entra no laudo como informação, para a pessoa conferir se
  deixou de fora algo que pretendia dizer, e explicitamente rotulada como "não é erro".
- **Nenhuma consequência é afirmada.** Divergência entre slides e proposta não está no rol
  do Art. 108º nem na hipótese do Art. 39º. A skill não diz que desclassifica e também não
  diz que "não dá nada" — relata e remete ao Conselho. Regra herdada da errata 1.4.1 da
  `/edital2027`, em que a skill afirmava pena que o Código não previa.
- **Toda marcação de conteúdo novo declara o que foi procurado.** A linha "Procurei por: …"
  torna auditável uma afirmação negativa.
- **Sem percentual de coerência.** Contagens. Um número único viraria nota, e nota é mérito.
