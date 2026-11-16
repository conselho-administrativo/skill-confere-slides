#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventário objetivo de dois PDFs do Edital 2027 — EJ ADM UFBA.

    python ferramentas/inventario.py PROPOSTA.pdf SLIDES.pdf

Extrai de cada documento todo número, percentual, valor, data e período, com a página e
o contexto em que aparecem, e aponta:

  · números que aparecem só num dos lados;
  · pares com contexto parecido e valor diferente — as prováveis trocas.

É a parte falsificável do laudo. NÃO decide nada: "provável troca" é hipótese para
conferência humana, e número ausente de um lado quase sempre é só condensação.

Avisa quando um PDF não tem camada de texto (slides exportados como imagem). Nesse caso
a comparação automática não vale, e os slides precisam ser lidos página a página.

Saída em Markdown, no stdout. Código 0 sempre que conseguir ler os dois arquivos.
"""
import os
import re
import sys
import unicodedata

JANELA = 70          # caracteres de contexto para cada lado do número
MIN_SOBREPOSICAO = 2  # palavras em comum para sugerir que dois números falam do mesmo

VAZIAS = {
    "para", "pela", "pelo", "como", "mais", "menos", "cada", "esse", "essa", "este",
    "esta", "isso", "aquele", "aquela", "pelos", "pelas", "entre", "sobre", "ainda",
    "todos", "todas", "nossa", "nosso", "nossas", "nossos", "sera", "serao", "ser",
    "tem", "temos", "foi", "foram", "com", "sem", "por", "que", "dos", "das", "nos",
    "nas", "uma", "uns", "umas", "dia", "dias", "ano", "anos", "mes", "meses",
    "area", "areas", "forma", "ate", "the", "and",
}


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def paginas(caminho):
    """Lista de (numero_da_pagina, texto). Usa PyMuPDF; cai para pypdf."""
    try:
        import fitz
        with fitz.open(caminho) as d:
            return [(i + 1, p.get_text()) for i, p in enumerate(d)]
    except ImportError:
        pass
    try:
        from pypdf import PdfReader
        r = PdfReader(caminho)
        return [(i + 1, (pg.extract_text() or "")) for i, pg in enumerate(r.pages)]
    except ImportError:
        sys.exit("ERRO: instale PyMuPDF ou pypdf  ->  pip install pymupdf")


# ----------------------------------------------------------------- números

NUM = re.compile(
    r"R\$\s*\d[\d.\s]*(?:,\d+)?"            # R$ 1.200,50
    r"|\d[\d.]*(?:,\d+)?\s*%"               # 12,5%
    r"|\b\d{1,2}[ºª]"                       # 1º trimestre
    r"|\b\d[\d.]*(?:,\d+)?\b"               # 12.480 / 42 / 3,5
)

MESES = ("janeiro fevereiro marco abril maio junho julho agosto setembro outubro "
         "novembro dezembro").split()
ORDINAIS = r"(?:primeiro|segundo|terceiro|quarto|1[ºo]|2[ºo]|3[ºo]|4[ºo])\s+"
PERIODO = re.compile(
    r"\b(?:" + ORDINAIS + r")?(?:" + "|".join(MESES) +
    r"|trimestre|semestre|bimestre|quinzena)\b", re.I)


def valor(txt):
    """Normaliza o texto do número para um float comparável, ou None."""
    t = txt.strip()
    t = re.sub(r"R\$\s*", "", t)
    t = re.sub(r"\s*%$", "", t)
    t = re.sub(r"[ºª]$", "", t)
    t = t.replace(" ", "")
    if "," in t:                       # 1.200,50 -> 1200.50
        t = t.replace(".", "").replace(",", ".")
    elif t.count(".") >= 1:
        partes = t.split(".")
        # 12.480 é milhar; 3.5 seria decimal, raro em pt-BR
        if all(len(p) == 3 for p in partes[1:]):
            t = "".join(partes)
    try:
        return float(t)
    except ValueError:
        return None


def tipo(txt):
    if txt.strip().startswith("R$"):
        return "valor"
    if txt.strip().endswith("%"):
        return "percentual"
    if re.search(r"[ºª]$", txt.strip()):
        return "ordinal"
    v = valor(txt)
    if v is not None and 2000 <= v <= 2100 and float(v).is_integer():
        return "ano"
    return "numero"


def palavras(ctx):
    bruto = sem_acento(ctx.lower())
    return {p for p in re.findall(r"[a-z]{4,}", bruto) if p not in VAZIAS}


def coletar(pgs):
    itens = []
    for n, texto in pgs:
        plano = re.sub(r"\s+", " ", texto)
        for m in NUM.finditer(plano):
            bruto = m.group(0).strip()
            v = valor(bruto)
            if v is None:
                continue
            ini, fim = max(0, m.start() - JANELA), min(len(plano), m.end() + JANELA)
            ctx = plano[ini:fim].strip()
            itens.append({"pagina": n, "bruto": bruto, "valor": v,
                          "tipo": tipo(bruto), "contexto": ctx,
                          "palavras": palavras(ctx)})
    return itens


def periodos(pgs):
    achados = {}
    for n, texto in pgs:
        plano = re.sub(r"\s+", " ", texto)
        for m in PERIODO.finditer(plano):
            chave = sem_acento(m.group(0).lower())
            achados.setdefault(chave, []).append(n)
    return achados


# ----------------------------------------------------------------- relatório

def corta(s, n=110):
    s = s.replace("|", "/")
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    cam_a, cam_b = sys.argv[1], sys.argv[2]
    for c in (cam_a, cam_b):
        if not os.path.exists(c):
            sys.exit(f"ERRO: arquivo não encontrado: {c}")

    pa, pb = paginas(cam_a), paginas(cam_b)
    ta = "".join(t for _, t in pa)
    tb = "".join(t for _, t in pb)

    print("# Inventário objetivo — proposta × apresentação\n")
    print(f"**A — Proposta:** `{os.path.basename(cam_a)}` · {len(pa)} páginas · {len(ta)} caracteres de texto")
    print(f"**B — Apresentação:** `{os.path.basename(cam_b)}` · {len(pb)} páginas · {len(tb)} caracteres de texto\n")

    alerta = False
    for rot, pgs, txt in (("A — Proposta", pa, ta), ("B — Apresentação", pb, tb)):
        vazias = sum(1 for _, t in pgs if len(t.strip()) < 20)
        if len(txt.strip()) < 200 or (pgs and vazias / len(pgs) > 0.5):
            alerta = True
            print(f"> ⚠️ **{rot} quase não tem texto extraível** "
                  f"({vazias} de {len(pgs)} páginas vazias). É provável que seja "
                  f"exportado como imagem.\n>\n"
                  f"> **A comparação automática não vale para este documento.** "
                  f"Leia as páginas uma a uma antes de montar o laudo, e registre no "
                  f"laudo que a conferência foi visual.\n")
    if alerta:
        print("---\n")

    ia, ib = coletar(pa), coletar(pb)
    print(f"Números capturados: **{len(ia)}** na proposta, **{len(ib)}** na apresentação.\n")

    va = {i["valor"] for i in ia}
    vb = {i["valor"] for i in ib}

    # 1. prováveis trocas: número só em B, com contexto parecido a um número de A
    print("## 1. Prováveis trocas de valor\n")
    print("Número que aparece **só na apresentação**, num contexto parecido com o de um "
          "número **diferente** da proposta. É hipótese, não achado: confira os dois "
          "trechos antes de registrar.\n")
    trocas = []
    for b in ib:
        if b["valor"] in va or not b["palavras"]:
            continue
        melhor, nota = None, -1
        for a in ia:
            if a["valor"] == b["valor"]:
                continue
            s = len(a["palavras"] & b["palavras"])
            if s < MIN_SOBREPOSICAO:
                continue
            pontos = s
            if a["tipo"] == b["tipo"]:
                pontos += 2          # número troca por número; percentual, por percentual
            if a["valor"] not in vb:
                pontos += 2          # sumiu da apresentação: candidato a ter sido substituído
            if pontos > nota:
                melhor, nota = a, pontos
        if melhor:
            trocas.append((nota, melhor, b))
    trocas.sort(key=lambda x: -x[0])
    if trocas:
        print("Força = palavras de contexto em comum, com bônus quando os dois são do mesmo "
              "tipo e quando o valor da proposta não reaparece na apresentação. "
              "Serve só para ordenar: confira de cima para baixo.\n")
        print("| Força | Proposta (pág.) | Apresentação (pág.) | Contexto na proposta | Contexto na apresentação |")
        print("|---|---|---|---|---|")
        for nota, a, b in trocas[:30]:
            print(f"| {nota} | **{a['bruto']}** (p.{a['pagina']}) | **{b['bruto']}** (p.{b['pagina']}) "
                  f"| {corta(a['contexto'], 80)} | {corta(b['contexto'], 80)} |")
        if len(trocas) > 30:
            print(f"\n_(+{len(trocas) - 30} pares com sobreposição menor, omitidos)_")
    else:
        print("_Nenhum par suspeito. Isso não garante ausência de divergência — "
              "só que nenhum número trocou de valor em contexto parecido._")
    print()

    # 2. números só na apresentação
    print("## 2. Números só na apresentação\n")
    print("Candidatos a **conteúdo novo**: o eleitor leu a proposta e não viu isto. "
          "Antes de marcar como novo, procure o número na proposta inteira — pode estar "
          "escrito por extenso ou em outra seção.\n")
    so_b = [b for b in ib if b["valor"] not in va]
    if so_b:
        print("| Valor | Tipo | Pág. | Contexto |")
        print("|---|---|---|---|")
        for b in sorted(so_b, key=lambda x: x["pagina"])[:40]:
            print(f"| **{b['bruto']}** | {b['tipo']} | {b['pagina']} | {corta(b['contexto'])} |")
        if len(so_b) > 40:
            print(f"\n_(+{len(so_b) - 40} omitidos)_")
    else:
        print("_Nenhum. Todo número da apresentação também está na proposta._")
    print()

    # 3. números só na proposta
    print("## 3. Números só na proposta\n")
    print("Normalmente é **só condensação** — a apresentação tem 15 minutos e não cabe "
          "tudo. Vale olhar apenas se for meta ou indicador central.\n")
    so_a = [a for a in ia if a["valor"] not in vb]
    print(f"Total: **{len(so_a)}**. Os de maior peso (percentuais e valores):\n")
    peso = [a for a in so_a if a["tipo"] in ("percentual", "valor")]
    if peso:
        print("| Valor | Tipo | Pág. | Contexto |")
        print("|---|---|---|---|")
        for a in sorted(peso, key=lambda x: x["pagina"])[:25]:
            print(f"| {a['bruto']} | {a['tipo']} | {a['pagina']} | {corta(a['contexto'])} |")
        if len(peso) > 25:
            print(f"\n_(+{len(peso) - 25} omitidos)_")
    else:
        print("_Nenhum percentual ou valor exclusivo da proposta._")
    print()

    # 4. períodos
    print("## 4. Períodos e meses citados\n")
    ja, jb = periodos(pa), periodos(pb)
    chaves = sorted(set(ja) | set(jb))
    if chaves:
        print("| Termo | Proposta (págs.) | Apresentação (págs.) |")
        print("|---|---|---|")
        for k in chaves:
            la = ", ".join(map(str, sorted(set(ja.get(k, []))))) or "—"
            lb = ", ".join(map(str, sorted(set(jb.get(k, []))))) or "—"
            marca = " ⚠️" if bool(ja.get(k)) != bool(jb.get(k)) else ""
            print(f"| {k}{marca} | {la} | {lb} |")
        print("\n⚠️ = citado num documento e não no outro. Em calendário de ações "
              "`(Art. 56º II)`, vale conferir.")
    else:
        print("_Nenhum período nomeado encontrado._")
    print()

    print("---\n")
    print("> Inventário mecânico. Não substitui a leitura dos dois documentos: ele vê "
          "número, não argumento. Divergência de diagnóstico, de escopo ou de "
          "raciocínio não aparece aqui.")


if __name__ == "__main__":
    main()
