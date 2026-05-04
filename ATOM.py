from machine import Pin
import time
import bluetooth

# Configuração dos pinos da ponte H
A_1A = Pin(23, Pin.OUT)
A_1B = Pin(22, Pin.OUT)
B_1A = Pin(19, Pin.OUT)
B_1B = Pin(21, Pin.OUT)

# Configuração do LED 2 (opcional, para feedback visual)
led = Pin(2, Pin.OUT)
led.off()

# Funções de controle dos motores
def motores_frente():
    """Liga os motores para frente"""
    A_1A.value(0)
    A_1B.value(1)
    B_1A.value(0)
    B_1B.value(1)

def motores_tras():
    """Liga os motores para trás"""
    A_1A.value(1)
    A_1B.value(0)
    B_1A.value(1)
    B_1B.value(0)

def motores_esquerda():
    """
    Gira para a esquerda:
    Motor A vai para trás, Motor B vai para frente
    (rotação no próprio eixo)
    """
    A_1A.value(0)
    A_1B.value(1)  # Motor A: ré
    B_1A.value(1)
    B_1B.value(0)  # Motor B: frente

def motores_direita():
    """
    Gira para a direita:
    Motor A vai para frente, Motor B vai para trás
    (rotação no próprio eixo)
    """
    A_1A.value(1)
    A_1B.value(0)  # Motor A: frente
    B_1A.value(0)
    B_1B.value(1)  # Motor B: ré

def parar_motores():
    """Desliga os motores"""
    A_1A.value(0)
    A_1B.value(0)
    B_1A.value(0)
    B_1B.value(0)

# Inicializa o Bluetooth Low Energy (BLE)
ble = bluetooth.BLE()
ble.active(True)

# UUIDs padrão do Dabble (UART Service)
SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
TX_UUID      = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID      = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

# Configuração do serviço BLE (UART)
UART_SERVICE = (
    (SERVICE_UUID, (
        (TX_UUID, bluetooth.FLAG_NOTIFY),
        (RX_UUID, bluetooth.FLAG_WRITE),
    )),
)

# Callback para eventos BLE
def bt_irq(event, data):
    if event == 1:  # BLE_IRQ_CENTRAL_CONNECT
        conn_handle, addr_type, addr = data
        print("Dispositivo conectado:", bytes(addr).hex(':'))

    elif event == 2:  # BLE_IRQ_CENTRAL_DISCONNECT
        conn_handle, addr_type, addr = data
        print("Dispositivo desconectado")
        start_advertising()

    elif event == 3:  # BLE_IRQ_GATTS_WRITE
        conn_handle, value_handle = data
        value = ble.gatts_read(value_handle)
        print("Dados recebidos (hex):", value.hex())

        # ── Seta CIMA ──────────────────────────────────────────
        if value == b'\xff\x01\x01\x01\x02\x00\x01\x00':
            motores_frente()
            led.on()
            print("MOTORES PARA FRENTE")

        # ── Seta BAIXO ─────────────────────────────────────────
        elif value == b'\xff\x01\x01\x01\x02\x00\x02\x00':
            motores_tras()
            led.off()
            print("MOTORES PARA TRÁS")

        # ── Seta ESQUERDA ──────────────────────────────────────
        elif value == b'\xff\x01\x01\x01\x02\x00\x04\x00':
            motores_esquerda()
            led.on()
            print("GIRANDO PARA A ESQUERDA")

        # ── Seta DIREITA ───────────────────────────────────────
        elif value == b'\xff\x01\x01\x01\x02\x00\x08\x00':
            motores_direita()
            led.on()
            print("GIRANDO PARA A DIREITA")

        # ── Nenhum botão pressionado (parar) ───────────────────
        elif value == b'\xff\x01\x01\x01\x02\x00\x00\x00':
            parar_motores()
            led.off()
            print("MOTORES PARADOS")

# Configura o callback de eventos
ble.irq(bt_irq)

# Registra os serviços BLE
ble.gatts_register_services(UART_SERVICE)

# Inicia o anúncio BLE
def start_advertising():
    name = "ATOM"
    adv_data = (
        bytearray(b'\x02\x01\x06')
        + bytearray((len(name) + 1, 0x09))
        + name.encode()
        + bytearray(b'\x03\x03\x6E\x40')
    )
    ble.gap_advertise(100, adv_data)
    print("Anunciando dispositivo:", name)

start_advertising()
print("Servidor BLE inicializado. Aguardando conexões...")

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Desligando BLE e motores...")
    parar_motores()
    led.off()
    ble.active(False)

