import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import psycopg

connection_db = psycopg.connect("dbname=mac user=postgres password= host=164.90.152.205 port=80")


url = 'https://en.wikipedia.org/wiki/List_of_Egyptian_hieroglyphs'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
tables = soup.find_all('table', {'class': 'wikitable'})

total = 0

with connection_db as conn:
    with conn.cursor() as cursor:

        for table in tables:
            rows = table.find_all('tr')[1:]
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 4:
                    continue

                try:
                    symbol = cells[0].text.strip()

                    gardiner_full = cells[1].text.strip()
                    codes = gardiner_full.split('\n')
                    gardiner = codes[0].strip()
                    unicode_code = codes[1].strip() if len(codes) > 1 else None 

                    description = cells[2].text.strip().replace("'", "''")
                    ideogram = cells[3].text.strip().replace("'", "''")
                    phonogram = cells[4].text.strip().replace("'", "''") if len(cells) > 4 else ''
                    notes = cells[5].text.strip().replace("'", "''") if len(cells) > 5 else ''

                    try:
                        with conn.transaction():
                            cursor.execute('''
                                INSERT INTO hieroglifo (
                                    symbol, gardiner, unicode_code, description, ideogram, phonogram, notes
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ''', (symbol, gardiner, unicode_code, description, ideogram, phonogram, notes))
                            total += 1

                    except psycopg.Error as e:
                        print(f'Erro ao inserir "{gardiner}": {getattr(e, "pgerror", str(e)).strip()}')

                except Exception as e:
                    print(f'Erro de parsing ao processar linha: {e}')

print(f"\nImportação concluída. {total} hieróglifos inseridos com sucesso.")
