from web3 import Web3
import time
import os

PRIVATE_KEY = os.getenv('PRIVATE_KEY', 'd0409024ed75016c496fa420ff693152aa0267bf863096bf72c047c7cf22df45')
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/03500aa353b94a3ea2e76d8bbd57716f'))  
account = w3.eth.account.from_key(PRIVATE_KEY)

# Configuración del contrato
CONTRACT_ABI = [
    {"inputs":[],"stateMutability":"nonpayable","type":"constructor"},
    {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"quien","type":"address"},{"indexed":False,"internalType":"int256","name":"nuevoValor","type":"int256"}],"name":"ValorModificado","type":"event"},
    {"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"addToWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"name":"decrementar","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"name":"incrementar","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"isWhitelisted","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"obtenerValor","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"removeFromWhitelist","outputs":[],"stateMutability":"nonpayable","type":"function"}
]
CONTRACT_ADDRESS = w3.to_checksum_address('0xFEF940B7A4A0530A4aEC6591341A79A276dAC4bD')
my_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)


#Leer la información del contrato
def read_counter():
    value = my_contract.functions.obtenerValor().call({'from': account.address})
    print(f"Valor del contador: {value}")

# Escribir en el contrato
def increment_counter():
    tx = {
        'chainId': 11155111,  
        'gas': 2000000,
        'nonce': w3.eth.get_transaction_count(account.address),
    }

    increment_txn = my_contract.functions.incrementar().build_transaction(tx)

    # Firmar y enviar la transacción
    signed_txn = w3.eth.account.sign_transaction(increment_txn, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transacción enviada: {tx_hash.hex()}")

#Escuchar el evento
def handle_event(event):
    print(f"Evento capturado!\nQuien: {event['args']['quien']}\nNuevo valor: {event['args']['nuevoValor']}")

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def listen_for_event():
    event_filter = my_contract.events.ValorModificado.create_filter(fromBlock='latest')
    log_loop(event_filter, 15)

is_on_whitelist = my_contract.functions.isWhitelisted(account.address).call()
print(f"Está en la whitelist? {is_on_whitelist}")
print(account.address)
read_counter()
increment_counter()  
listen_for_event()  
