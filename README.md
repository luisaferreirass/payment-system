# 💳 Payment System

## 📝 Sobre o projeto

Sistema de pagamentos com **PIX** desenvolvido com **Flask**, implementando geração de QR Codes, comunicação em tempo real via **WebSockets** e confirmação automática de pagamentos. O projeto simula um fluxo completo de pagamento digital com interface web responsiva.

Ideal para aprendizado de:
- Sistema de pagamentos PIX
- Geração de QR Codes
- WebSockets com Flask-SocketIO
- Comunicação em tempo real (Real-time)
- Webhooks para confirmação de pagamento
- Flask-SQLAlchemy e SQLite
- Renderização de templates com Jinja2
- Arquitetura MVC

## 🚀 Tecnologias utilizadas

- **Python 3.x**
- **Flask 2.3.0** - Framework web
- **Flask-SQLAlchemy 3.1.1** - ORM para banco de dados
- **Flask-SocketIO 5.3.6** - WebSockets para comunicação em tempo real
- **SQLite** - Banco de dados
- **QRCode 7.4.2** - Geração de QR Codes
- **Pillow 10.2.0** - Processamento de imagens
- **Pytest** - Framework de testes
- **Jinja2** - Template engine

## ⚙️ Como executar

### Pré-requisitos

- Python 3.x instalado
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/luisaferreirass/payment-system.git
cd payment-system
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Inicialize o banco de dados:
```bash
python
>>> from repository.database import db
>>> from app import app
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Executando a aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

### Executando os testes
```bash
pytest
```

ou para ver mais detalhes:
```bash
pytest -v
```

## 🎯 Funcionalidades

- 💳 **Criar pagamento PIX** com valor e data de expiração
- 🔲 **Gerar QR Code** automaticamente para pagamento
- ⏰ **Expiração automática** de 30 minutos
- 📱 **Interface web responsiva** para visualizar pagamento
- ✅ **Confirmação via webhook** simulando banco
- 🔄 **Atualização em tempo real** com WebSockets
- 📊 **Página de confirmação** após pagamento
- 🚫 **Página de erro 404** personalizada

## 🛠️ Modelo de dados

### Payment (Pagamento)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária (auto-incremento) |
| value | Float | Valor do pagamento |
| paid | Boolean | Status do pagamento (padrão: False) |
| bank_payment_id | String(200) | ID único gerado pelo "banco" |
| qrcode | String(100) | Nome do arquivo do QR Code |
| expiration_date | DateTime | Data de expiração (30 minutos) |

## 📸 Endpoints da API

### Pagamentos PIX

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/payments/pix` | Cria um novo pagamento PIX |
| GET | `/payments/pix/<id>` | Visualiza a página de pagamento |
| GET | `/payments/pix/qr_code/<file_name>` | Retorna a imagem do QR Code |
| POST | `/payments/pix/confirmation` | Webhook de confirmação do banco |

### WebSocket Events

| Evento | Descrição |
|--------|-----------|
| `connect` | Cliente conecta ao servidor |
| `disconnect` | Cliente desconecta do servidor |
| `payment-confirmed-<id>` | Notificação de pagamento confirmado |

## 💡 Exemplos de uso

### 1. Criar um pagamento PIX
```bash
POST /payments/pix
Content-Type: application/json

{
  "value": 100.50
}
```

**Resposta:**
```json
{
  "message": "The payment has been created",
  "payment": {
    "id": 1,
    "value": 100.50,
    "paid": false,
    "bank_payment_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
    "qrcode": "qr_code_payment_a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
    "expiration_date": "2024-02-04T11:00:00"
  }
}
```

### 2. Visualizar página de pagamento
```bash
GET /payments/pix/1
```

Retorna uma página HTML com:
- Valor do pagamento
- QR Code gerado
- Conexão WebSocket ativa
- Timer de expiração

### 3. Obter imagem do QR Code
```bash
GET /payments/pix/qr_code/qr_code_payment_a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8
```

Retorna a imagem PNG do QR Code.

### 4. Confirmar pagamento (Webhook do banco)
```bash
POST /payments/pix/confirmation
Content-Type: application/json

{
  "bank_payment_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "value": 100.50
}
```

**Resposta:**
```json
{
  "message": "The payment has been confirmed"
}
```

**Resultado:** 
- Marca o pagamento como `paid = True`
- Emite evento WebSocket `payment-confirmed-1`
- Cliente é redirecionado automaticamente para página de confirmação

## 🔄 Fluxo de Pagamento
```
1. Cliente cria pagamento
         ↓
2. Sistema gera QR Code e ID único
         ↓
3. Cliente acessa página de pagamento
         ↓
4. WebSocket conecta e aguarda confirmação
         ↓
5. "Banco" envia webhook de confirmação
         ↓
6. Sistema valida e confirma pagamento
         ↓
7. WebSocket notifica cliente em tempo real
         ↓
8. Cliente é redirecionado para página de sucesso
```

## 🎨 Estrutura de Páginas

### 1. payment.html
- Exibe QR Code do pagamento
- Mostra valor e ID da transação
- Timer de expiração (30 minutos)
- WebSocket listener para confirmação
- Redirecionamento automático após pagamento

### 2. confirmed_payment.html
- Confirmação visual do pagamento
- Exibe ID e valor do pagamento
- Mensagem de sucesso
- Opção para nova transação

### 3. 404.html
- Página de erro personalizada
- Exibida quando pagamento não é encontrado
- Link para voltar à página inicial

## 📁 Estrutura do Projeto
```
payment-system/
├── app.py                          # Aplicação principal
├── repository/
│   └── database.py                 # Configuração do banco
├── db_models/
│   └── payment.py                  # Model de Payment
├── payments/
│   └── pix.py                      # Lógica de geração PIX
├── templates/
│   ├── payment.html                # Página de pagamento
│   ├── confirmed_payment.html      # Página de confirmação
│   └── 404.html                    # Página de erro
├── static/
│   └── img/                        # QR Codes gerados
├── requirements.txt
└── README.md
```

## 🔐 Validações Implementadas

### Criação de Pagamento
- ✅ Verifica se o valor foi informado
- ✅ Gera ID único usando UUID
- ✅ Define expiração de 30 minutos
- ✅ Salva QR Code no disco

### Confirmação de Pagamento
- ✅ Valida `bank_payment_id` e `value`
- ✅ Verifica se pagamento existe
- ✅ Impede confirmação duplicada
- ✅ Valida correspondência de valor
- ✅ Atualiza status no banco
- ✅ Notifica cliente via WebSocket



## 🎯 Recursos do Sistema PIX

### Geração de QR Code
- ID único usando UUID4
- Hash de pagamento gerado automaticamente
- Imagem PNG salva em `/static/img/`
- Padrão: `qr_code_payment_{bank_payment_id}.png`

### Simulação de Banco
- Geração de `bank_payment_id` único
- Webhook para confirmação
- Validação de valor e ID
- Proteção contra duplicatas

### Expiração de Pagamento
- Tempo padrão: 30 minutos
- Armazenado em `expiration_date`
- Pode ser usado para limpeza automática


## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📄 Licença

Este projeto está sob a licença MIT.

## 👩‍💻 Autora

Desenvolvido por [Luisa Ferreira](https://github.com/luisaferreirass)
