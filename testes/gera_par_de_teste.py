# -*- coding: utf-8 -*-
"""Gera um par de PDFs de teste para o inventario.py, com divergências conhecidas.

PROPOSTA (A) e SLIDES (B) do mesmo candidato fictício. Diferenças plantadas:

  TROCA   NPS de 42 para 60   ->   de 42 para 75          (deve virar provável troca)
  TROCA   retenção 78%        ->   retenção 90%           (deve virar provável troca)
  NOVO    slide cita R$ 8.000 que não existe na proposta  (deve cair em "só na apresentação")
  OMITIDO proposta cita 12 processos, slide não cita      (deve cair em "só na proposta")
  IGUAL   3 frentes nos dois                              (não deve aparecer)
  PERÍODO proposta fala em "segundo trimestre", slide não (deve marcar ⚠️)
"""
import os
import fitz

SAIDA = os.path.dirname(os.path.abspath(__file__))

PROPOSTA = [
    ("Proposta Final 2027 - Diretoria de Mercado",
     "Diagnostico da area. O gargalo principal esta na qualificacao dos leads, "
     "e nao no volume. Em 2025 recebemos 1.240 leads e convertemos 97."),
    ("Objetivos e indicadores",
     "Vamos elevar o NPS de 42 para 60 ate o fim da gestao. "
     "A retencao de membros da area deve sair de 71% para 78%. "
     "Mediremos o sucesso pela taxa de conversao de leads qualificados."),
    ("Planos de acao",
     "Organizamos a gestao em 3 frentes. Vamos revisar 12 processos comerciais. "
     "O investimento previsto em ferramentas e de R$ 4.500 no ano."),
    ("Calendario",
     "No primeiro trimestre faremos o diagnostico. No segundo trimestre "
     "implantamos a nova cadencia comercial."),
]

SLIDES = [
    ("Proposta 2027 - Mercado", "Diretoria de Mercado"),
    ("O gargalo", "O gargalo esta na qualificacao dos leads. 1.240 leads em 2025."),
    ("Metas",
     "Elevar o NPS de 42 para 75. "
     "Retencao de membros de 71% para 90%."),
    ("Como vamos fazer",
     "3 frentes de trabalho. Investimento de R$ 4.500 em ferramentas "
     "e mais R$ 8.000 em eventos."),
    ("Calendario", "Primeiro trimestre: diagnostico."),
    ("Obrigado", "Conto com voces."),
]


def escreve(caminho, paginas, titulo):
    doc = fitz.open()
    for cab, corpo in paginas:
        pg = doc.new_page()
        pg.insert_text((60, 80), cab, fontsize=16)
        y = 120
        for linha in [corpo[i:i + 70] for i in range(0, len(corpo), 70)]:
            pg.insert_text((60, y), linha, fontsize=11)
            y += 18
    doc.save(caminho)
    doc.close()
    print(f"  {titulo}: {caminho} ({len(paginas)} páginas)")


escreve(os.path.join(SAIDA, "teste_proposta.pdf"), PROPOSTA, "A proposta")
escreve(os.path.join(SAIDA, "teste_slides.pdf"), SLIDES, "B slides")
print("\nEsperado do inventário:")
print("  provável troca: 60 -> 75 (NPS) e 78 -> 90 (retenção)")
print("  só na apresentação: R$ 8.000")
print("  só na proposta: 12 processos, 97 conversões")
print("  período marcado: segundo trimestre só na proposta")
