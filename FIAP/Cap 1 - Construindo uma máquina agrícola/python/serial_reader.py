import time
import json
import serial

class SerialReader:
    """
    Abstrai a leitura de JSON via porta serial.
    """

    def __init__(self, port: str, baudrate: int, timeout: float = 2.0):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)

    def read_json(self) -> dict | None:
        """
        Lê uma linha do serial, tenta parsear como JSON e retorna um dict.
        Se a linha estiver vazia ou inválida, retorna None.
        """
        line = self.ser.readline().decode("utf-8", errors="ignore").strip()
        if not line:
            return None
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            print("Warning: JSON inválido recebido:", line)
            return None
