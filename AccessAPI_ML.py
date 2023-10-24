"""
Essa classe fornece uma maneira conveniente de interagir com a API do Mercado Livre e 
extrair informações relacionadas a vendas e produtos. Ela encapsula as chamadas de API e 
gerencia a autenticação e a paginação.
"""
import requests
import json

class AccessAPI_ML:

    def __init__(self, client_id, client_secret, refresh_token):
        """
        O construtor da classe que inicializa os atributos necessários para obter um token de acesso

        Argumentos:
            client_id: 
            client_secret: chave secreta do aplicativo 
            refresh_token:

        Retorno:

        """
        self.access_token = self._get_access_token(client_id, client_secret, refresh_token)
        self.base_url = "https://api.mercadolibre.com/"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

    def _get_access_token(self, client_id, client_secret, refresh_token):
        """
        Um método privado que faz uma solicitação HTTP POST para obter um token de acesso à API do Mercado Livre. 
        Ele usa as credenciais do cliente abaixo para autenticação.

        Argumentos:
            client_id: 
            client_secret: 
            refresh_token: 

        Retorno:

        """
                
        url = "https://api.mercadolibre.com/oauth/token"
        payload = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token
        }
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, headers=headers, data=payload)
        token = response.json()
        return token['access_token']

    def _make_api_request(self, endpoint, params=None):
        """
        Ele recebe um endpoint específico e parâmetros para a solicitação e usa o token de acesso para autenticar a solicitação

        Argumentos:
            endpoint: 

        Retorno:

        """
        url = self.base_url + endpoint
        headers = {
            'Authorization': self.access_token,
            'User-Agent': self.user_agent
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_vendas(self, seller_id):
        """
        Retorna informações de vendas para um vendedor específico, usando o endpoint "orders/search" e parâmetros relacionados ao vendedor.

        Argumentos:
            seller_id: 

        Retorno:

        """
        endpoint = "orders/search"
        params = {'seller': seller_id, 'access_token': self.access_token}
        return self._make_api_request(endpoint, params)

    def get_vendas_by_range(self, seller_id, dt_ini, dt_fim):
        """
        Retorna informações de vendas para um vendedor em um intervalo de datas específico. 
        Ele usa o mesmo endpoint "orders/search" e parâmetros para definir as datas de início e término.

        Argumentos:
            seller_id: 
            dt_ini:
            dt_fim:

        Retorno:

        """
        endpoint = "orders/search"
        params = {
            'seller': seller_id,
            'order.date_created.from': f'{dt_ini}T00:00:00.000-00:00',
            'order.date_created.to': f'{dt_fim}T23:59:59.000-00:00',
            'access_token': self.access_token
        }
        return self._make_api_request(endpoint, params)

    def get_produtos(self, palavra_chave):
        """
        Retorna produtos com base em uma palavra-chave usando o endpoint "sites/MLB/search" e um parâmetro de consulta.

        Argumentos:
            palavra_chave:

        Retorno:

        """
        endpoint = "sites/MLB/search"
        params = {'q': palavra_chave}
        return self._make_api_request(endpoint, params)

    def get_produtos_paginacao(self, palavra_chave, limit=50):
        """
        Retorna uma lista paginada de produtos com base em uma palavra-chave e limite de resultados. 
        Ele faz várias solicitações para obter todos os resultados paginados.

        Argumentos:
            palavra_chave:

        Retorno:

        """
        endpoint = "sites/MLB/search"
        offset = 0
        resultados = []
        while True:

          params = {'q': palavra_chave, 'limit': limit, 'offset': 0}
          response = self._make_api_request(endpoint, params)
          if response is not None:
            resultados.extend(response['results'])
            offset += limit

            if offset >= response['paging']['total']:
              break
            else:
              break

        return resultados

    def get_items_details(self, id_produto):
        """
        Retorna detalhes de um item específico com base no seu ID. 
        
        Argumentos:
            id_produto:

        Retorno:
            Ele usa o endpoint "items/{id_produto}" para obter informações como a data de início, o ID do vendedor e a quantidade vendida.
            start_time: data de crição do anúncio
            seller_id: código do vendedor
            sold_quantity: quantidade de vendas do produto
        """
        endpoint = f'items/{id_produto}'
        #return self._make_api_request(endpoint)
        dados = self._make_api_request(endpoint)
        return dados['start_time'][:10], dados['seller_id'], dados['sold_quantity']

    def get_items_by_seller(self, id_seller):
        """
        Retorna uma lista de itens de um vendedor específico, ordenados por preço ascendente.
        
        Argumentos:
            id_seller: código do vendedor

        Retorno:

        """
        endpoint = "sites/MLB/search"
        params = {'seller_id': id_seller, 'sort': 'price_asc'}
        return self._make_api_request(endpoint, params)

    def get_all_categories(self):
        """
        Retorna todas as categorias de produtos disponíveis no Mercado Livre.
        
        Argumentos:

        Retorno:

        """
        endpoint = 'sites/MLB/categories'
        return self._make_api_request(endpoint)

    def get_items_by_category(self, categoria):
        """
        Retorna uma lista de itens com base em uma categoria específica.
        
        Argumentos:
            categoria: categoria do produto

        Retorno:

        """
        endpoint = "sites/MLB/search"
        params = {'category': categoria}
        return self._make_api_request(endpoint, params)

    def get_items_by_category_paging(self, categoria, limit=50):
        """
        Retorna uma lista paginada de itens com base em uma categoria específica.
        
        Argumentos:
            categoria: categoria do produto
            
        Retorno:

        """
        endpoint = "sites/MLB/search"
        offset = 0
        resultados = []

        while True:

            params = {'category': categoria, 'limit': limit, 'offset': 0}
            response = self._make_api_request(endpoint, params)

            if response is not None:
                resultados.extend(response['results'])
                offset += limit

                if offset >= response['paging']['total']:
                    break
            else:
                break

        return resultados

    def get_items_by_seller_category(self, seller_id, categoria):
        """
        Retorna itens de um vendedor específico dentro de uma categoria específica.
        
        Argumentos:
            seller_id: código do vendedor
            categoria: categoria do produto
            
        Retorno:

        """
        endpoint = "sites/MLB/search"
        params = {'seller_id': seller_id, 'category': categoria}
        return self._make_api_request(endpoint, params)

    def get_visits_by_items(self, id_produto, dias, data_final):
        """
        Retorna informações de visitas a um item específico em um período de tempo específico.
        
        Argumentos:
            id_produto: código do produto
            dias: período a retornar ( 7 dias, 30 dias )
            data_final: data a partir do qual será contado os dias para trás
            
        Retorno:

        """
        endpoint = f'items/{id_produto}/visits/time_window'
        params = {'last': dias, 'unit': 'day', 'ending': data_final}
        return self._make_api_request(endpoint, params)

    def get_selled_items_by_seller(self, seller_id):
        """
        Retorna itens vendidos por um vendedor específico com status "paid" (pago).
        
        Argumentos:
            seller_id: código do vendedor
            
        Retorno:

        """
        endpoint = "orders/search"
        params = {'seller': seller_id, 'order.status': 'paid'}
        return self._make_api_request(endpoint, params)