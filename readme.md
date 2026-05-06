# 🤖 ESP32 BLE Robot (ATOM & ZEUS)

Projeto de robô controlado via Bluetooth Low Energy (BLE) utilizando ESP32 e MicroPython.

Os nomes **ATOM** e **ZEUS** foram inspirados no filme *Gigantes de Aço*, mas todo o desenvolvimento foi feito por mim.

---

## 🚀 Funcionalidades

- Controle remoto via celular
- Movimentação em tempo real:
  - Frente
  - Trás
  - Esquerda
  - Direita
- Feedback visual com LED
- Comunicação via BLE

---

## 🧠 Como funciona

O ESP32 atua como um servidor BLE, recebendo comandos enviados por um aplicativo no celular (ex: Dabble).

Esses comandos são interpretados e convertidos em sinais elétricos para a ponte H, que controla os motores do robô.

---

## 🔧 Tecnologias utilizadas

- ESP32
- MicroPython
- Bluetooth Low Energy (BLE)
- GPIO
- Ponte H (controle de motores)

---

## 📱 Controle

O robô pode ser controlado utilizando aplicativos que enviam comandos BLE, como:

- Dabble (modo Gamepad)

---

## 🤖 Robôs

- ATOM
- ZEUS

Ambos utilizam o mesmo código, alterando apenas o nome do dispositivo BLE.

---

## ▶️ Como executar

1. Instale o MicroPython no ESP32
2. Envie o arquivo `main.py` para a placa
3. Ligue o robô
4. Conecte via aplicativo BLE
5. Controle os movimentos

---

## 📌 Autores

Lucca Gomes Ramos | Rafael Seragioli
