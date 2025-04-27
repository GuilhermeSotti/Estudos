from db.connection import get_connection
from datetime import datetime

def insert_reading(sensor_id: int, valor: float, historico_id: int, timestamp: datetime):
    """
    Insere uma nova leitura na tabela Monitoring.LeituraDoSensor.
    """
    sql = """
    INSERT INTO Monitoring.LeituraDoSensor
        (sensor_id, valor, historico_id, timestamp)
    VALUES (?, ?, ?, ?);
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (sensor_id, valor, historico_id, timestamp))
    conn.commit()
    cursor.close()
    conn.close()

def read_readings(limit: int = 10):
    """
    Retorna as últimas `limit` leituras, ordenadas por leitura_id desc.
    """
    sql = """
    SELECT TOP (?) *
      FROM Monitoring.LeituraDoSensor
     ORDER BY leitura_id DESC;
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def update_reading(leitura_id: int, novo_valor: float):
    """
    Atualiza o campo `valor` de uma leitura existente.
    """
    sql = """
    UPDATE Monitoring.LeituraDoSensor
       SET valor = ?
     WHERE leitura_id = ?;
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (novo_valor, leitura_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_reading(leitura_id: int):
    """
    Remove uma leitura do banco.
    """
    sql = "DELETE FROM Monitoring.LeituraDoSensor WHERE leitura_id = ?;"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (leitura_id,))
    conn.commit()
    cursor.close()
    conn.close()
