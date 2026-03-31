import requests
import pandas as pd
import time  # necessário para usar sleep

base_url = "https://www.lancamentosrio.com.br/api/anuncios/search"
todos_dados = []
page = 1

# Headers simulando navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

while True:
    params = {"finalidade": "venda", "page": page}
    response = requests.get(base_url, params=params, headers=headers)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        print(f"Erro na página {page}: {response.status_code}")
        break

    try:
        info = response.json()
    except requests.JSONDecodeError:
        print(f"Não foi possível decodificar JSON na página {page}")
        break

    anuncios = info.get("items", [])
    if not anuncios:
        break  # fim das páginas

    for data in anuncios:
        condominio = data.get("condominio")
        endereco = f"{data.get('logradouro', '')}, {data.get('numero', '')}, {data.get('bairro', '')}, {data.get('cidade', '')}, {data.get('estadoSigla', '')}"
        status = data.get("lancamento") or ", ".join([c for c in data.get("caracteristicas", []) if "Obra" in c or "Habite-se" in c])
        preco = data.get("valorVenda")
        metro_quadrado = data.get("areaConstruida")

        todos_dados.append({
            "condominio": condominio,
            "endereco": endereco,
            "status": status,
            "preco": preco,
            "m2": metro_quadrado
        })

    print(f"Página {page} processada")
    page += 1

    time.sleep(1)  # pausa de 1 segundo entre requisições

print(f"Total de imóveis coletados: {len(todos_dados)}")

# Salva em Excel
df = pd.DataFrame(todos_dados)
df.to_excel("base lançamentosrio.xlsx", index=False, engine='openpyxl')
print("Dados salvos em 'base lançamentosrio.xlsx'")