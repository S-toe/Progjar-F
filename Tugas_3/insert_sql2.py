import sqlite3, os, sys, time

start = time.time()         # start runtime

CREATE = True             

if CREATE:
    try:
        os.remove("data.db")
    except:
        pass

db = sqlite3.connect("data.db")         # koneksi database data.db
cur = db.cursor()                       # u/ menjalankan query

if CREATE:
    counter = 0
    for ln in open("ExportSQL2.sql"):       # u/ setiap line di dr opened file (ExportSQL2.sql) berisi query create table & insert data
        ln = ln.strip()                     # membuang white space (depan-belakang)
        cur.execute(ln)                     # menjalankan line query yg didapatkan
        
        if counter % 1000 == 0:                     # print ke layar
            db.commit()
            sys.stdout.write(str(counter)+"..")
            sys.stdout.flush()
        counter += 1
    db.commit()

# u/ jalankan query count
cur = db.cursor()                                  
cur.execute("select count(*) from mockdata;")
print("\ncount(*) = ", cur.fetchone()[0])

# coba jalankan query lain (tampilkan FirstNameLastName, JobTitle dg ID < 5)
cur = db.cursor()
rows=cur.execute("select FirstNameLastName, JobTitle from mockdata where ID < 5")

# iterator u/ lbh dr 1 (tdk bisa print rows)
#for row in rows.fetchall():
#    for i in range(len(row)):
#        print(i, row[i])

for row in rows.fetchall():        
    print(row)

#close db
db.close()      

# print runtime
print("waktu: = ", time.time()-start)    