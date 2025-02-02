import sqlite3

def check_tables():
    conn = sqlite3.connect('ursula.db')
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables in database:")
    for table in tables:
        print(f"\nTable: {table[0]}")
        try:
            cursor.execute(f"SELECT * FROM {table[0]} LIMIT 1;")
            columns = [description[0] for description in cursor.description]
            print(f"Columns: {', '.join(columns)}")
            
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cursor.fetchone()[0]
            print(f"Row count: {count}")
        except Exception as e:
            print(f"Error reading table: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_tables() 