import uuid
import qrcode

class Pix:
    def __init__(self) -> None:
        pass

    def create_payment(self, base_dir=""):
        # Criar o pagamento na instituição financeira

        bank_bayment_id = str(uuid.uuid4()) # Criando um identificador que simula um pagamento numa instituição financeira e temos que tranformar em string porque ele retorna um objeto

        hash_payment = f'hash_payment_{bank_bayment_id}' # Gerar o copia e cola

        img = qrcode.make(hash_payment) # gerando o QRCODE

        #Salvar a imagem como arquivo PNG
        img.save(f"{base_dir}static/img/qr_code_payment_{bank_bayment_id}.png")

        return {"bank_payment_id": bank_bayment_id,
                "qr_code_path": f"qr_code_payment_{bank_bayment_id}"}