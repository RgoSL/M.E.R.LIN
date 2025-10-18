# Essa Classe é a Responsável por Perpetuar as Informações de Configuração Selecionadas

# Import das Bibliotecas Utilizadas
import sqlite3

# --- Cria ou conecta ao banco ---
def conectar():
    return sqlite3.connect("banco_de_dados.db")

# --- Cria tabela se não existir ---
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ajustes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resolucao TEXT,
            idioma TEXT,
            fps TEXT,
            luz_camera TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- Salva os ajustes selecionados ---
def salvar_ajustes(resolucao, idioma, fps, luz_camera):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ajustes")  # remove anteriores (mantém 1 config)
    cursor.execute("""
        INSERT INTO ajustes (resolucao, idioma, fps, luz_camera)
        VALUES (?, ?, ?, ?)
    """, (resolucao, idioma, fps, luz_camera))
    conn.commit()
    conn.close()

# --- Carrega ajustes salvos ---
def carregar_ajustes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT resolucao, idioma, fps, luz_camera FROM ajustes LIMIT 1")
    dados = cursor.fetchone()
    conn.close()
    return dados
