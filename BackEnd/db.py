import psycopg

conn = psycopg.connect("dbname=mac user=postgres password= host=164.90.152.205 port=80")

def get_hieroglyph(code):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT symbol, gardiner, unicode_code, description, ideogram, phonogram, notes
            FROM hieroglyph 
            WHERE gardiner = %s
        """, (code,))
        
        row = cur.fetchone()
        if not row:
            return None

        symbol = row[0]
        gardiner = row[1]
        unicode_code = row[2]
        description = row[3]
        ideogram = row[4]
        phonogram = row[5]
        notes = row[6]

        cur.execute("""
            SELECT image_url, description 
            FROM hieroglyph_images 
            WHERE gardiner = %s
        """, (gardiner,))
        
        images = cur.fetchall()

        images_list = [
            {"image_url": img[0], "description": img[1]}
            for img in images
        ]

        return {
            "symbol": symbol,
            "gardiner_code": gardiner,
            "unicode_code": unicode_code,
            "description": description,
            "ideogram": ideogram,
            "phonogram": phonogram,
            "notes": notes,
            "images": images_list
        }
