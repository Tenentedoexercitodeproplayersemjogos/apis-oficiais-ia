#!/usr/bin/env python3
"""Gera README.md e apis.csv a partir de apis.json."""
import csv
import json
from collections import Counter
from urllib.parse import quote

SITE = "https://tenentedoexercitodeproplayersemjogos.github.io/apis-oficiais-ia/"
ORDEM = [
    "Texto/Chat", "Multimodal", "Imagem", "Vídeo", "Áudio/Voz", "Embeddings",
    "Busca/RAG", "OCR/Documentos", "3D", "Tradução", "Inferência", "Cloud", "Local",
]


def main():
    P = json.load(open("apis.json", encoding="utf-8"))
    cats = Counter(p["categoria"] for p in P)
    paises = Counter(p["pais"] for p in P)
    livres = Counter(p["gratis"] for p in P)

    with open("apis.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "nome", "categoria", "pais", "gratis", "site", "criar_api", "docs", "modelos", "obs"])
        for p in P:
            w.writerow([p["id"], p["nome"], p["categoria"], p["pais"], p["gratis"], p["site"],
                        p["chave"], p["docs"], p["modelos"], p["obs"]])

    L = []
    A = L.append
    A("# Onde criar API de IA (links oficiais)\n")
    A(f"Diretório com **{len(P)} provedores de IA** e o link oficial para criar a chave de API. "
      "Inclui site, documentação, modelos principais, free tier e país de origem.\n")
    A(f"🌐 **Site com busca e filtros:** {SITE}\n")
    A("⚠️ **Grátis ≠ licença livre.** Aqui \"grátis\" significa custo zero para usar (com limites). "
      "Free tiers mudam sem aviso — confira sempre no site oficial.\n")
    A("📍 **Origem** = país-sede do provedor. Empresas chinesas, como Alibaba (Qwen) e DeepSeek, "
      "aparecem como **China** e podem ser filtradas no site.\n")
    A("## Resumo\n")
    A(f"- **{len(P)}** provedores em **{len(cats)}** categorias e **{len(paises)}** origens")
    A(f"- **{livres['Sim']}** com free tier · **{livres['Limitado']}** com créditos limitados · "
      f"**{livres['Não']}** só pagos · **{livres['Local']}** locais (sem API key)")
    A(f"- **{paises['China']}** provedores chineses, incluindo Alibaba (Qwen) e DeepSeek")
    A("- Verificação automática dos links toda segunda-feira\n")
    A("## Por categoria\n")
    A("| Categoria | Provedores | Exemplos |")
    A("|---|---:|---|")
    for c in ORDEM:
        if not cats.get(c):
            continue
        nomes = sorted((p["nome"] for p in P if p["categoria"] == c))
        exemplos = ", ".join(nomes[:4])
        if len(nomes) > 4:
            exemplos += ", …"
        A(f"| **{c}** | {cats[c]} | {exemplos} |")
    A("")
    A("## Por origem\n")
    A("| Origem | Provedores | Filtro |")
    A("|---|---:|---|")
    for pais, n in sorted(paises.items(), key=lambda x: (-x[1], x[0])):
        A(f"| **{pais}** | {n} | [ver]({SITE}?pais={quote(pais)}) |")
    A("")
    A("## Provedores chineses\n")
    chineses = sorted(p["nome"] for p in P if p["pais"] == "China")
    A(", ".join(chineses) + ".\n")
    A(f"🔎 [Ver todos os provedores chineses no site]({SITE}?pais=China)\n")
    A("## Onde ver tudo\n")
    A(f"- **Site completo, com busca e filtros:** {SITE}")
    A("- **CSV:** [apis.csv](apis.csv) · **JSON:** [apis.json](apis.json)")
    A("- **Status dos links:** [status.json](status.json)")
    A("")
    A("## Observações\n")
    A("- Os links de chave levam ao painel oficial do provedor (login necessário).")
    A("- `Local` = roda no seu computador; não existe chave de API.")
    A("- A origem é a sede do provedor; hospedagem e disponibilidade podem variar por região.")
    A("- Sem afiliação com os provedores. Preços, limites e países podem mudar.\n")
    A("_README e CSV gerados automaticamente a partir de `apis.json`._")
    open("README.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("README.md e apis.csv gerados | provedores:", len(P))


if __name__ == "__main__":
    main()
