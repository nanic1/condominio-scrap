import requests
import pandas as pd
import time

# URL PODE VARIAR, VERIFICAR NO SITE APTO.VC
url = "https://apto.vc/_next/data/c4CV659C9opeV5h-S4PrC/br/sp/sao-paulo.json?"

HEADERS = {
    "x-nextjs-data": "1",
    "User-Agent": "Mozilla/5.0"
}

def buscar_pagina(path, tries=5, timeout=5):
    for i in range(tries):
        try:
            response = requests.get(path, headers=HEADERS, timeout=timeout)

            print(f"STATUS: {response.status_code}")
            response.raise_for_status()

            return response.json()
        except requests.exceptions.ReadTimeout:
            print(f"Demora para obter informações. Tentando novamente...")
            time.sleep(2)
        except requests.exceptions.HTTPError as erro:
            print(f"Erro: {erro}")

    return None


def verifica_dados(data):
    try:
        return data["pageProps"]["realties"]["data"]
    except:
        return []

def montar_card(card):
    return {
        "nome": card.get("name"),
        "endereco": card.get("address"),
        "bairro": card.get("neighborhoods", [{}])[0].get("name"),
        "preco": card.get("price"),
        "area m2": card.get("area"),
        "quartos": card.get("bedrooms"),
        "banheiros": card.get("bathrooms"),
        "vagas": card.get("parking"),
        "status": card.get("status", {}).get("name"),
        "link": card.get("permalink")
    }

def main():
    page = 1
    todos = []

    while True:
        # API por algum motivo NÃO lê ?page=1 por algum motivo.
        # condição para ler url padrão (sem page) e apos a primeira pagina, adicionar ?page=x ao final da url
        if page >= 2:
            path = f"{url}?page={page}"
        else:
            path = url

        print(f"\nPágina: {page}")

        data = buscar_pagina(path)
        if not data:
            print("Erro ao buscar a página. Encerrando...")
            break

        cards = verifica_dados(data)
        if not cards:
            print("Não foram encontrados imóveis. Encerrando scraping.")
            break

        print(f"{len(cards)} imóveis encontrados na página {page}")

        for c in cards:
            todos.append(montar_card(c))

        page += 1
        time.sleep(1)

    dataframe = pd.DataFrame(todos)

    if dataframe.empty:
        print("Dataframe vazio.")
    else:
        dataframe.to_excel("base_apto.xlsx", index=False, engine='openpyxl')
        print("Scrap realizado com sucesso!")

main()