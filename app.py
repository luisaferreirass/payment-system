from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix
from flask_socketio import SocketIO #Usamos o socketIO para conectar o cliente com o servidor


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key_websocket'

db.init_app(app)
socketio = SocketIO(app)

# Rota que vai permitir que seja criado um pagamento (vai criar um pagamento desejado)
@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    data = request.json

    #Validações

    if 'value' not in data:
        return jsonify({"message": "Invalid value"}), 400
    
    expiration_date = datetime.now() + timedelta(minutes=30) # Pega o tempo atual e soma 30 min

    new_payment = Payment(value= data['value'], expiration_date= expiration_date)

    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment_id = data_payment_pix["bank_payment_id"]
    new_payment.qrcode = data_payment_pix["qr_code_path"]

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "The payment has been created",
                   "payment": new_payment.to_dict()})


@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_image(file_name):
    return send_file(f"static/img/{file_name}.png", mimetype='image/png')

# Rota que ser responsavel pela abertura de uma conxeão com o banco para ver se o pagamento foi recebido ou não (webHook)
@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation():

    data = request.json # Request do banco que vai dizer qual foi o pagamento que foi pago

    if "bank_payment_id" not in data and "value" not in data:
        return jsonify({"message": "Invalid payment data"}), 400

    payment = Payment.query.filter_by(bank_payment_id= data.get("bank_payment_id")).first()

    if not payment or payment.paid:
        return jsonify({"message": "Payment not found"}), 404

    if data.get("value") != payment.value:
        return jsonify({"message": "Invalid payment data"}), 400
    

    payment.paid = True
    db.session.commit()
    socketio.emit(f'payment-confirmed-{payment.id}') # Emite uma notificação para todos os clientes conectados
    return jsonify({"message": "The payment has been confirmed"})

# Rota que vai permitir que o usuário veja o pagamento feito (aqui vamos estabelecer a conexão com o websocket)
@app.route('/payments/pix/<int:id>', methods=['GET'])
def payment_pix_page(id):
    payment = Payment.query.get(id)

    if not payment:
        return render_template('404.html')

    if payment.paid:
        return render_template('confirmed_payment.html',
                            id=payment.id, 
                            value= payment.value)

    return render_template('payment.html', 
                           id=payment.id, 
                           value= payment.value, 
                           host="http://127.0.0.1:5000", 
                           qr_code=payment.qrcode) # O arquivo tem que estar na pasta templates

#websockets 

# Rota que conecta o cliente ao servidor
@socketio.on('connect') # Espera o evento acontecer
def handle_connect():
    print("Client connected to the server")

@socketio.on('disconnect')
def handle_disconnect():
    print('Client has disconnected to the server')

if __name__ == '__main__':
    socketio.run(app, debug= True)
