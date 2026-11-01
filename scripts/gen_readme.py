#!/usr/bin/env python3
"""Gera README.md e apis.csv a partir de apis.json."""
import json, csv
from collections import Counter

SITE = "https://tenentedoexercitodeproplayersemjogos.github.io/apis-oficiais-ia/"
ORDEM = ["Texto/Chat", "Multimodal", "Imagem", "Áudio/Voz", "Embeddings", "Cloud", "Local"]


def main():
    P = json.load(open("apis.json", encoding="utf-8"))
    cats = Counter(p["categoria"] for p in P)
    livres = Counter(p["gratis"] for p in P)

    with open("apis.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "nome", "categoria", "gratis", "site", "criar_api", "docs", "modelos", "obs"])
        for p in P:
            w.writerow([p["id"], p["nome"], p["categoria"], p["gratis"], p["site"],
                        p["chave"], p["docs"], p["modelos"], p["obs"]])

    L = []
    A = L.append
    A("# Onde criar API de IA (links oficiais)\n")
    A(f"Diretório com **{len(P)} provedores de IA** e o link oficial para criar a chave de API. "
      "Inclui site, documentação, modelos principais e se existe free tier.\n")
    A(f"🌐 **Site com busca e filtros:** {SITE}\n")
    A("⚠️ **Grátis ≠ licença livre.** Aqui \"grátis\" significa custo zero para usar (com limites). "
      "Free tiers mudam sem aviso — confira sempre no site oficial.\n")
    A("## Resumo\n")
    A(f"- **{len(P)}** provedores")
    A(f"- **{livres['Sim']}** com free tier · **{livres['Limitado']}** com créditos limitados · "
      f"**{livres['Não']}** só pagos · **{livres['Local']}** locais (sem API key)")
    A("- **" + str(len(cats)) + "** categorias: " + " · ".join(f"{c} ({cats[c]})" for c in ORDEM if cats.get(c)) + "\n")
    A("## Provedores\n")
    A("| Provedor | Categoria | Grátis | Criar API | Site | Docs | Modelos |")
    A("|---|---|---|---|---|---|---|")
    for p in sorted(P, key=lambda x: (ORDEM.index(x["categoria"]) if x["categoria"] in ORDEM else 99, x["nome"].lower())):
        chave = f"[criar]({p['chave']})" if p["chave"] else "— (local)"
        A(f"| **{p['nome']}** | {p['categoria']} | {p['gratis']} | {chave} | "
          f"[site]({p['site']}) | [docs]({p['docs']}) | {p['modelos']} |")
    A("")
    A("## Observações\n")
    A("- Os links de chave levam direto ao painel oficial do provedor (login necessário).")
    A("- `Local` = roda no seu computador; não existe chave de API.")
    A("- Dados: [`apis.csv`](apis.csv) · [`apis.json`](apis.json) · verificação: [`status.json`](status.json)")
    A("- Sem afiliação com os provedores. Preços e limites podem mudar.\n")
    A("_README e CSV gerados automaticamente a partir de `apis.json`._")
    open("README.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("README.md e apis.csv gerados | provedores:", len(P))


if __name__ == "__main__":
    main()
