# Cleanup
def close(conn, cursor):
    conn.commit()
    print('Done.')
    cursor.close()
    conn.close()
    print('Connection closed.')
