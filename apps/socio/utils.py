import requests

def preencher_endereco_por_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        endereco = {
            'logradouro': data.get('logradouro'),
            'bairro': data.get('bairro'),
            'cidade': data.get('localidade'),
            'estado': data.get('uf'),
            'cep': data.get('cep')
        }
        return endereco
    else:
        return None