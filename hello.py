import firebase_admin
import requests
from firebase_admin import credentials
from firebase_admin import firestore

# Carrega as credenciais
cred = credentials.Certificate("aula.json")

# Inicializa o app do Firebase
firebase_admin.initialize_app(cred)

# Obtém uma referência ao banco de dados Firestore
db = firestore.client()

url_autenticacao = "https://api.oplab.com.br/v3/domain/users/authenticate"
url_autorizacao = "https://api.oplab.com.br/v3/domain/users/authorize"

headers_autenticacao = {
    "content-type": "application/json"
}
payload = {
    "email": "romualdomr.c@gmail.com",
    "password": "32343040"
}

response = requests.post(url_autenticacao, headers=headers_autenticacao, json=payload)

if response.status_code == 200:
    dados = response.json()
    access_token = dados["access-token"]  # Extrai o token aqui
    print("Access Token:", access_token)

    headers_autorizacao = {
        "Access-Token": access_token
    }

    response = requests.get(url_autorizacao, headers=headers_autorizacao)

    if response.ok:
        dados = response.json()
        print("Resposta da API:", dados)


        symbol = "PETR4" 
        with_financials = "true"  

        url = f"https://api.oplab.com.br/v3/market/stocks/{symbol}?with_financials={with_financials}"
        headers = {
            "Access-Token": access_token
        }


        response = requests.get(url, headers=headers)

        if response.ok:
            dados = response.json()
            symbol = dados.get("symbol")
            open_value = dados.get("open")
            close_value = dados.get("close")
            print(f"Symbol: {symbol}")
            print(f"Open: {open_value}")
            print(f"Close: {close_value}")

            # Escreve um documento em uma coleção
            doc_ref = db.collection('acoes').document(symbol)
            doc_ref.set({
                     'Open': open_value,
                     'Close': close_value
            })

            print("Dados enviados ao Firestore!")

        else:
            print("Erro:", response.status_code, response.text)

else:
    print("Erro:", response.text)


