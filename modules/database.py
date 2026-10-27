import sqlite3
import os
from datetime import datetime

def obter_caminho_db():
    pasta_data = "data"
    if not os.path.exists(pasta_data):
        os.makedirs(pasta_data)
    return os.path.join(pasta_data, "driver_audit.db")

def init_db():
    """Inicializa o banco de dados e cria a tabela de histórico de varreduras."""
    conn = sqlite3.connect(obter_caminho_db())
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_auditorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            total_dispositivos INTEGER,
            desatualizados INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalhes_drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            auditoria_id INTEGER,
            nome_dispositivo TEXT,
            categoria TEXT,
            versao_atual TEXT,
            versao_recomendada TEXT,
            status TEXT,
            FOREIGN KEY (auditoria_id) REFERENCES historico_auditorias (id)
        )
    """)
    
    conn.commit()
    conn.close()

def salvar_auditoria(drivers_analisados):
    """Salva uma nova varredura e seus detalhes no banco SQLite."""
    init_db()
    conn = sqlite3.connect(obter_caminho_db())
    cursor = conn.cursor()
    
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(drivers_analisados)
    desatualizados = sum(1 for d in drivers_analisados if d['status'] == 'Desatualizado')
    
    # Salva o cabeçalho da auditoria
    cursor.execute("""
        INSERT INTO historico_auditorias (data_hora, total_dispositivos, desatualizados)
        VALUES (?, ?, ?)
    """, (data_hora_atual, total, desatualizados))
    
    auditoria_id = cursor.lastrowid
    
    # Salva cada driver individualmente vinculado à auditoria
    for d in drivers_analisados:
        cursor.execute("""
            INSERT INTO detalhes_drivers (auditoria_id, nome_dispositivo, categoria, versao_atual, versao_recomendada, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            auditoria_id,
            d['nome'],
            d['categoria'],
            d['versao_instalada'],
            d['versao_sugerida'],
            d['status']
        ))
        
    conn.commit()
    conn.close()