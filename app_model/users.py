
def add_user(conn, name, hash, role):
    cur = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?) '''
    param = (name, hash, role)
    cur.execute(sql, param)
    conn.commit()
  


def migrate_users(conn):
    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        user_name, user_hash = user.strip().split(",")
        add_user(conn, user_name, user_hash, 'user')



#read data from users
def get_all_users(conn):
    cur = conn.cursor()
    sql = '''SELECT * FROM users'''
    cur.execute(sql)
    users = cur.fetchall()
    conn.close()
    return(users)


#read just one user based on username
def get_user(conn, name):
    cur = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ?'''
    param = (name,)
    cur.execute(sql, param)
    user = cur.fetchone()
    conn.close()
    return(user)


def update_user(conn, new_role, user_name):
    cur = conn.cursor()
    sql = 'UPDATE users SET role = ? WHERE username = ?'
    param = (new_role, user_name)
    cur.execute(sql, param)
    conn.commit()
    
def delete_user(conn, user_name):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    param = (user_name,)
    cur.execute(sql, param)
    conn.commit()