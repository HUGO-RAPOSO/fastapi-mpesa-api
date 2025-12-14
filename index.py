from fastapi import FastAPI
from pydantic import BaseModel
from portalsdk import APIContext, APIMethodType, APIRequest
from pprint import pprint
import time

app = FastAPI()

# 1. Defina o Modelo de Dados de Entrada
# O Flutter enviará dados neste formato JSON.
class PaymentDetails(BaseModel):
    amount: str  # String para valores monetários, como no seu código original
    msisdn: str  # Número de telefone do cliente
    
    # Você pode adicionar mais campos se quiser controlar 'input_ThirdPartyReference' ou outros.

# 2. Crie o Endpoint da API
@app.post("/realizar_pagamento/")
def realizar_pagamento(details: PaymentDetails):
    """
    Recebe o valor e o MSISDN do Flutter e executa a transação C2B.
    """
    
    # Seus dados fixos da API
    api_context = APIContext()
    api_context.api_key = 't4kk96znpbdud5z91p5s93m1yzwpfdgd'
    api_context.public_key = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAmptSWqV7cGUUJJhUBxsMLonux24u+FoTlrb+4Kgc6092JIszmI1QUoMohaDDXSVueXx6IXwYGsjjWY32HGXj1iQhkALXfObJ4DqXn5h6E8y5/xQYNAyd5bpN5Z8r892B6toGzZQVB7qtebH4apDjmvTi5FGZVjVYxalyyQkj4uQbbRQjgCkubSi45Xl4CGtLqZztsKssWz3mcKncgTnq3DHGYYEYiKq0xIj100LGbnvNz20Sgqmw/cH+Bua4GJsWYLEqf/h/yiMgiBbxFxsnwZl0im5vXDlwKPw+QnO2fscDhxZFAwV06bgG0oEoWm9FnjMsfvwm0rUNYFlZ+TOtCEhmhtFp+Tsx9jPCuOd5h2emGdSKD8A6jtwhNa7oQ8RtLEEqwAn44orENa1ibOkxMiiiFpmmJkwgZPOG/zMCjXIrrhDWTDUOZaPx/lEQoInJoE2i43VN/HTGCCw8dKQAwg0jsEXau5ixD0GUothqvuX3B9taoeoFAIvUPEq35YulprMM7ThdKodSHvhnwKG82dCsodRwY428kg2xM/UjiTENog4B6zzZfPhMxFlOSFX4MnrqkAS+8Jamhy1GgoHkEMrsT5+/ofjCx0HjKbT5NuA2V/lmzgJLl3jIERadLzuTYnKGWxVJcGLkWXlEPYLbiaKzbJb2sYxt+Kt5OxQqC1MCAwEAAQ=='
    api_context.ssl = True
    api_context.method_type = APIMethodType.POST
    api_context.address = 'api.sandbox.vm.co.mz'
    api_context.port = 18352
    api_context.path = '/ipg/v1x/c2bPayment/singleStage/'
    api_context.add_header('Origin', '*')

    # Seus dados fixos de transação (pode mudar se necessário)
    api_context.add_parameter('input_TransactionReference', 'T' + str(int(time.time()))) # Use um valor dinâmico
    api_context.add_parameter('input_ThirdPartyReference', '111PA2D')
    api_context.add_parameter('input_ServiceProviderCode', '171717')

    # 3. Use os Parâmetros Recebidos do Flutter
    api_context.add_parameter('input_CustomerMSISDN', details.msisdn)
    api_context.add_parameter('input_Amount', details.amount)

    # 4. Executa a Requisição
    try:
        api_request = APIRequest(api_context)
        result = api_request.execute()

        # 5. Retorna o resultado para o Flutter
        # O `result.body` provavelmente é um JSON/dicionário.
        # Estamos retornando a resposta completa, incluindo o status code da API externa.
        return {
            "status_code": result.status_code,
            "headers": result.headers,
            "body": result.body
        }
    except Exception as e:
        # Lida com erros de rede ou do SDK
        return {
            "status_code": 500,
            "error": "Erro ao executar a transação: " + str(e)
        }

# Endpoint de teste
@app.get("/")
def read_root():
    return {"message": "API de Pagamento M-Pesa pronta. Use o endpoint /realizar_pagamento/"}