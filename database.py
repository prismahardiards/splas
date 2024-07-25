import sqlite3
import pandas as pd

def setup_database():
    file_path = r'C:\Users\PRISMA\Documents\statistics-generator\statistics-generator\question-bank\dataset.xlsx'
    db_path = r'C:\Users\PRISMA\Documents\statistics-generator\statistics-generator\db\questions.db'

    df = pd.read_excel(file_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS elements (
        id INTEGER PRIMARY KEY,
        element TEXT NOT NULL,
        question TEXT NOT NULL
    )
    ''')

    cursor.execute('SELECT id, element, question FROM elements')
    existing_data = cursor.fetchall()

    existing_df = pd.DataFrame(existing_data, columns=['id', 'element', 'question'])

    for index, row in df.iterrows():
        element = row['Elements']
        question = row['Question']
        
        matching_row = existing_df[(existing_df['element'] == element) & (existing_df['question'] == question)]
        
        if not matching_row.empty:
            cursor.execute('''
                UPDATE elements
                SET question = ?
                WHERE id = ?
            ''', (question, matching_row.iloc[0]['id']))
        else:
            cursor.execute('INSERT INTO elements (element, question) VALUES (?, ?)', (element, question))

    conn.commit()
    conn.close()