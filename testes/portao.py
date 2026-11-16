#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Portão da skill /confere-slides.

    python testes/portao.py

Oito checagens mecânicas de integridade. Sai com 1 se qualquer uma falhar.
Não substitui os casos dourados, que conferem comportamento — os dois têm de estar verdes.
"""
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
falhas = []


def ler(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()


def arquivos(exts=(".md", ".py")):
    for dp, dirs, fs in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in fs:
            if f.endswith(exts):
                yield os.path.relpath(os.path.join(dp, f), RAIZ).replace(os.sep, "/")


def check(nome, ok, detalhe=""):
    print(f"  {'OK  ' if ok else 'FALHA'}  {nome}" + (f" — {detalhe}" if detalhe else ""))
    if not ok:
        falhas.append(nome)


print("PORTÃO — skill /confere-slides\n")

skill = ler("SKILL.md")

# 1. Frontmatter e nome.
tem_fm = skill.startswith("---\nname: confere-slides\n")
check("1. SKILL.md com frontmatter e nome correto", tem_fm, f"frontmatter={tem_fm}")

# 2. As travas e a assimetria, que são o núcleo do comportamento.
tem_travas = "As oito travas" in skill
tem_assim = "Tirar é permitido. Trocar não é." in skill
tem_aviso = "apoio e pode errar" in skill
check("2. SKILL.md com as oito travas, a assimetria e o aviso de falibilidade",
      tem_travas and tem_assim and tem_aviso,
      f"travas={tem_travas}, assimetria={tem_assim}, aviso={tem_aviso}")

# 3. Toda rota citada no SKILL.md existe.
rotas = set(re.findall(r"`((?:referencias|ferramentas|testes)/[\w\-/\.]+)`", skill))
quebradas = [r for r in rotas if not os.path.exists(os.path.join(RAIZ, r))]
check("3. Rotas do SKILL.md íntegras", not quebradas,
      f"{len(rotas)} rotas, quebradas={quebradas or '—'}")

# 4. Citações de artigo dentro de 1..125 (o Código tem 125 artigos).
#    Esta skill não carrega o Código; só confere que não cita artigo inexistente.
fora = []
total = 0
for rel in arquivos():
    t = ler(rel)
    t = re.sub(r"Art\.\s*\d+º?\s*(do|de)\s+(Estatuto|Regimento)[^.;)]*", "", t)
    for m in re.finditer(r"Art\.\s*(\d+)º", t):
        total += 1
        if not 1 <= int(m.group(1)) <= 125:
            fora.append(f"{rel}:Art. {m.group(1)}º")
check("4. Citações de artigo dentro de 1..125", not fora,
      f"{total} citações, fora da faixa={fora[:5] or '—'}")

# 5. Nenhum caractere de controle perdido no texto.
#    Herdado da /edital2027: um escape mal resolvido já injetou 0x07 num caminho.
PERMITIDOS = {9, 10, 13}
sujos = []
for rel in arquivos():
    for n, linha in enumerate(ler(rel).split(chr(10)), 1):
        if any(ord(c) < 32 and ord(c) not in PERMITIDOS for c in linha):
            sujos.append(f"{rel}:{n}")
            break
check("5. Sem caracteres de controle no texto", not sujos, str(sujos[:5] or "—"))

# 6. A ferramenta compila e responde sem argumentos.
ferr = os.path.join(RAIZ, "ferramentas", "inventario.py")
try:
    r = subprocess.run([sys.executable, ferr], capture_output=True, text=True, timeout=60)
    roda = r.returncode != 0 and "inventario.py" in (r.stdout + r.stderr)
except Exception as e:
    roda = False
    r = None
check("6. inventario.py roda e mostra o uso", roda,
      "sai com erro e imprime o modo de usar" if roda else "não executou como esperado")

# 7. Sem placeholder esquecido.
PLACEHOLDERS = ("<org>", "xxxxx", "TODO", "PREENCHER", "FIXME", "a publicar")
achados = []
for rel in arquivos():
    if rel.startswith("testes/") or rel == "CHANGELOG.md":
        continue
    t = ler(rel)
    for p in PLACEHOLDERS:
        if p in t:
            achados.append(f"{rel}:{p}")
check("7. Sem placeholders esquecidos", not achados, str(achados[:5] or "—"))

# 8. Versão do SKILL.md bate com a última do CHANGELOG.
m_sk = re.search(r"^\*\*Versão ([\d.]+)\*\*", skill, re.M)
m_ch = re.search(r"^## \[([\d.]+)\]", ler("CHANGELOG.md"), re.M)
v_sk = m_sk.group(1) if m_sk else None
v_ch = m_ch.group(1) if m_ch else None
check("8. Versão do SKILL.md bate com o CHANGELOG", bool(v_sk) and v_sk == v_ch,
      f"SKILL.md={v_sk or '—'}, CHANGELOG={v_ch or '—'}")

print()
if falhas:
    print(f"PORTÃO VERMELHO — {len(falhas)} checagem(ns) falhou/falharam:")
    for f in falhas:
        print(f"  · {f}")
    print("\nNão publique com o portão vermelho.")
    sys.exit(1)

print("PORTÃO VERDE — as 8 checagens passaram.")
print("Lembre: rode também testes/casos-dourados.md antes de publicar.")
sys.exit(0)
