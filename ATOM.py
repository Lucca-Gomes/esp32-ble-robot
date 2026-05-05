from machine import Pin
import time
import bluetooth

# ==============================
# CONFIGURAÇÃO DOS PINOS (PONTE H)
# ==============================
# Cada par controla um motor (A e B)

A_1A = Pin(23, Pin.OUT)  # Motor A - direção 1
A_1B = Pin(22, Pin.OUT)  # Motor A - direção 2
B_1A = Pin(19, Pin.OUT)  # Motor B - direção 1
B_1B = Pin(21, Pin.OUT)  # Motor B - direção 2

# ==============================
# LED DE STATUS (feedback visual)
# ==============================
led = Pin(2, Pin.OUT)
led.off()

# ==============================
# FUNÇÕES DE MOVIMENTO
# ==============================

def motores_frente():
    """Move o robô para frente"""
    A_1A.value(0)
    A_1B.value(1)
    B_1A.value(0)
    B_1B.value(1)

def motores_tras():
    """Move o robô para trás"""
    A_1A.value(1)
    A_1B.value(0)
    B_1A.value(1)
    B_1B.value(0)

def motores_esquerda():
    """
    Gira o robô para a esquerda (no próprio eixo)
    Motor A vai para trás
    Motor B vai para frente
    """
    A_1A.value(0)
    A_1B.value(1)
    B_1A.value(1)
    B_1B.value(0)

def motores_direita():
    """
    Gira o robô para a direita (no próprio eixo)
    Motor A vai para frente
    Motor B vai para trás
    """
    A_1A.value(1)
    A_1B.value(0)
    B_1A.value(0)
    B_1B.value(1)

def parar_motores():
    """Para todos os motores"""
    A_1A.value(0)
    A_1B.value(0)
    B_1A.value(0)
    B_1B.value(0)

# ==============================
# CONFIGURAÇÃO DO BLUETOOTH (BLE)
# ==============================

ble = bluetooth.BLE()
ble.active(True)

# UUID padrão do serviço UART (usado por apps como Dabble)
SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

# Estrutura do serviço BLE
UART_SERVICE = (
    (SERVICE_UUID, (
        (TX_UUID, bluetooth.FLAG_NOTIFY),  # envio de dados
        (RX_UUID, bluetooth.FLAG_WRITE),   # recebimento de dados
    )),
)

# ==============================
# CALLBACK DE EVENTOS BLE
# ==============================

def bt_irq(event, data):

    # Dispositivo conectou
    if event == 1:
        conn_handle, addr_type, addr = data
        print("Dispositivo conectado:", bytes(addr).hex(':'))

    # Dispositivo desconectou
    elif event == 2:
        print("Dispositivo desconectado")
        start_advertising()

    # Dados recebidos do celular
    elif event == 3:
        conn_handle, value_handle = data
        value = ble.gatts_read(value_handle)

        print("Comando recebido:", value.hex())

        # ==============================
        # CONTROLE DOS MOVIMENTOS
        # ==============================

        if value == b'\xff\x01\x01\x01\x02\x00\x01\x00':
            motores_frente()
            led.on()

        elif value == b'\xff\x01\x01\x01\x02\x00\x02\x00':
            motores_tras()
            led.off()

        elif value == b'\xff\x01\x01\x01\x02\x00\x04\x00':
            motores_esquerda()
            led.on()

        elif value == b'\xff\x01\x01\x01\x02\x00\x08\x00':
            motores_direita()
            led.on()

        elif value == b'\xff\x01\x01\x01\x02\x00\x00\x00':
            parar_motores()
            led.off()

# ==============================
# REGISTRO DO BLE
# ==============================

ble.irq(bt_irq)
ble.gatts_register_services(UART_SERVICE)

# ==============================
# INICIAR ANÚNCIO BLE
# ==============================

def start_advertising():
    name = "ATOM"  # pode mudar para ZEUS

    adv_data = (
        bytearray(b'\x02\x01\x06') +
        bytearray((len(name) + 1, 0x09)) +
        name.encode() +
        bytearray(b'\x03\x03\x6E\x40')
    )

    ble.gap_advertise(100, adv_data)
    print("Anunciando como:", name)

start_advertising()

print("Aguardando conexão BLE...")

# ==============================
# LOOP PRINCIPAL
# ==============================

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Desligando sistema...")
    parar_motores()
    led.off()
    ble.active(False)