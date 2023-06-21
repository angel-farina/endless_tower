import sqlite3,os

def create_scores_table():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "scores.db")

    # Crear una conexión a la base de datos
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Crear la tabla si no existe
    c.execute("CREATE TABLE IF NOT EXISTS scores (name TEXT, score INTEGER)")

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

def save_score(name, score):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "scores.db")

    # Conectar a la base de datos y obtener el puntaje actual
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT score FROM scores ORDER BY score DESC LIMIT 1")
    result = c.fetchone()

    if result is None or score > result[0]:
        # Eliminar el puntaje existente si hay alguno
        c.execute("DELETE FROM scores")
        
        # Insertar el nuevo puntaje más grande
        c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, int(score)))

    conn.commit()
    conn.close()

def check_if_table_exists():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "scores.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar si la tabla "scores" existe en la base de datos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scores'")
    table_exists = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return table_exists

def get_highest_score():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "scores.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener el puntaje más alto de la tabla "scores"
    cursor.execute("SELECT MAX(score) FROM scores")
    result = cursor.fetchone()
    highest_score = result[0] if result and result[0] else 0

    cursor.close()
    conn.close()

    return highest_score

def get_highscore_name():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "scores.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener el puntaje más alto de la tabla "scores"
    cursor.execute("SELECT MAX(score) FROM scores")
    result = cursor.fetchone()
    highest_score = result[0] if result and result[0] else 0

    # Obtener el nombre asociado al puntaje más alto
    cursor.execute("SELECT name FROM scores WHERE score=?", (highest_score,))
    result = cursor.fetchone()
    highest_score_name = result[0] if result else "N/A"

    cursor.close()
    conn.close()

    return highest_score_name
