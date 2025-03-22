import sys # É necessário fazer isso para conseguirmos importar o payments já que é o test não é um arquivo que está na raiz
sys.path.append("../") #Colocamos tudo numa pasta atrás
import pytest
import os #Biblioteca para verificar se o artigo existe ou não existe
from payments.pix import Pix


def test_pix_create_payment():
    pix_instance = Pix()

    # create a payment 
    payment_info = pix_instance.create_payment(base_dir="../")

    assert "bank_payment_id" in payment_info
    assert "qr_code_path" in payment_info

    qr_code_path = payment_info["qr_code_path"]
    
    assert os.path.isfile(f"../static/img/{qr_code_path}.png")