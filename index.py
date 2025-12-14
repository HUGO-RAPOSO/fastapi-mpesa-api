from fastapi import FastAPI
from pydantic import BaseModel
from portalsdk import APIContext, APIMethodType, APIRequest
import time
import os # <<< NOVO: Importar a biblioteca 'os'

app = FastAPI()

# -----------------------------------------------------
# LEITURA DAS VARIÁVEIS DE AMBIENTE
# Usamos 'os.environ.get()' para ler as chaves que você configurou no Render.
API_KEY = os.environ.get('MPESA_API_KEY')
PUBLIC_KEY = os.environ.get('MPESA_PUBLIC_KEY')
SERVICE_CODE = os.environ.get('MPESA_SERVICE_CODE')

# É bom adicionar uma verificação básica para garantir que as chaves foram carregadas
if not API_KEY or not PUBLIC_KEY:
    raise Exception("Chaves MPESA API_KEY ou PUBLIC_KEY não encontradas nas variáveis de ambiente.")
# -----------------------------------------------------

class PaymentDetails(BaseModel):
    amount: str
    msisdn: str
    

@app.post("/realizar_pagamento/")
def realizar_pagamento(details: PaymentDetails):
    """
    Recebe o valor e o MSISDN do Flutter e executa a transação C2B.
    """
    
    # Seus dados fixos da API
    api_context = APIContext()
    
    # >>> CHAVES LIDOS DO AMBIENTE, NÃO MAIS EMBUTIDOS NO CÓDIGO <<<
    api_context.api_key = API_KEY
    api_context.public_key = PUBLIC_KEY
    # -----------------------------------------------------------------
    
    api_context.ssl = True
    api_context.method_type = APIMethodType.POST
    api_context.address = 'api.sandbox.vm.co.mz'
    api_context.port = 18352
    api_context.path = '/ipg/v1x/c2bPayment/singleStage/'
    api_context.add_header('Origin', '*')

    # Seus dados fixos de transação
    api_context.add_parameter('input_TransactionReference', 'T' + str(int(time.time())))
    api_context.add_parameter('input_ThirdPartyReference', '111PA2D')
    
    # >>> Usando o SERVICE_CODE lido do ambiente <<<
    api_context.add_parameter('input_ServiceProviderCode', SERVICE_CODE)

    # Parâmetros Recebidos do Flutter
    api_context.add_parameter('input_CustomerMSISDN', details.msisdn)
    api_context.add_parameter('input_Amount', details.amount)

    try:
        api_request = APIRequest(api_context)
        result = api_request.execute()

        # Retorna o resultado para o Flutter
        return {
            "status_code": result.status_code,
            "body": result.body
        }
    except Exception as e:
        return {
            "status_code": 500,
            "error": "Erro ao executar a transação: " + str(e)
        }