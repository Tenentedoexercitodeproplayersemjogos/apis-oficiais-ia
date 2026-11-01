#!/usr/bin/env python3
"""Verifica os links de apis.json e gera status.json (ok / protegido / erro)."""
import json, ssl, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def check(url):
    if not url:
        return {"code": 0, "status": "sem-chave"}
    for t in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25, context=CTX) as f:
                code = f.status
            return {"code": code, "status": "ok"}
        except urllib.error.HTTPError as e:
            code = e.code
            if code in (400, 401, 403, 405, 429):
                return {"code": code, "status": "protegido"}
            if code in (404, 410) or code >= 500:
                return {"code": code, "status": "erro"}
            return {"code": code, "status": "protegido"}
        except Exception:
            if t == 0:
                time.sleep(2); continue
            return {"code": 0, "status": "erro"}
    return {"code": 0, "status": "erro"}


def main():
    P = json.load(open("apis.json", encoding="utf-8"))
    jobs = []
    for p in P:
        for field in ("site", "chave", "docs"):
            jobs.append((p["id"], field, p.get(field, "")))

    results = {p["id"]: {} for p in P}
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(check, url): (pid, field) for pid, field, url in jobs}
        for fut in futs:
            pid, field = futs[fut]
            results[pid][field] = fut.result()

    resumo = {"ok": 0, "protegido": 0, "erro": 0, "sem-chave": 0}
    erros = []
    for pid, fields in results.items():
        for field, r in fields.items():
            resumo[r["status"]] = resumo.get(r["status"], 0) + 1
            if r["status"] == "erro":
                erros.append(f'{pid}.{field} ({r["code"]})')

    out = {
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "resumo": resumo,
        "erros": erros,
        "resultados": results,
    }
    json.dump(out, open("status.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("verificado:", resumo)
    if erros:
        print("links com erro:", ", ".join(erros))
    else:
        print("nenhum link com erro")


if __name__ == "__main__":
    main()
