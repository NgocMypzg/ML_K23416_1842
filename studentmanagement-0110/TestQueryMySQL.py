import mysql.connector

server = "localhost"
port = 3306
database = "studentmanagement"
username = "root"
password = "3141592653589793Mk."

conn = mysql.connector.connect(
    host=server,
    port=port,
    database=database,
    user=username,
    password=password
)

# Truy vấn toàn bộ sinh viên
cursor = conn.cursor()

sql = "SELECT * FROM student"
cursor.execute(sql)

dataset = cursor.fetchall()
align = '{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format("ID", "Code", "Name", "Age"))
for item in dataset:
    id = item[0]
    code = item[1]
    name = item[2]
    age = item[3]
    avatar = item[4]
    intro = item[5]
    print(align.format(id, code, name, age))
cursor.close()
print("-"*100)
# Truy vấn các sinh viên có độ tuổi từ 22 đến 26
curser = conn.cursor()
sql = "SELECT * FROM student WHERE Age>=22 AND Age<=26"
curser.execute(sql)

dataset = curser.fetchall()
align = '{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format("ID", "Code", "Name", "Age"))
for item in dataset:
    id = item[0]
    code = item[1]
    name = item[2]
    age = item[3]
    avatar = item[4]
    intro = item[5]
    print(align.format(id, code, name, age))
cursor.close()
print("-"*100)
# Truy vấn toàn bộ sinh viên và sắp xếp theo tuổi tăng dân
curser = conn.cursor()
sql = "SELECT * FROM student ORDER BY Age DESC"
curser.execute(sql)

dataset = curser.fetchall()
align = '{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format("ID", "Code", "Name", "Age"))
for item in dataset:
    id = item[0]
    code = item[1]
    name = item[2]
    age = item[3]
    avatar = item[4]
    intro = item[5]
    print(align.format(id, code, name, age))
curser.close()
print("-"*100)
# Truy vấn các sinh viên có độ tuổi từ 22 tới 26 và sắp xếp theo tuổi giảm dần
cursor = conn.cursor()
sql="SELECT * FROM student " \
    "where Age>=22 and Age<=26 " \
    "order by Age desc "
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()
print("-"*100)
# Truy vấn chi tiết thông tin sinh viên khi biết id
cursor = conn.cursor()
sql="SELECT * FROM student " \
    "where ID=1 "

cursor.execute(sql)

dataset=cursor.fetchone()
if dataset!=None:
    id,code,name,age,avatar,intro=dataset
    print("Id=",id)
    print("code=",code)
    print("name=",name)
    print("age=",age)

cursor.close()
print("-"*100)
# Truy vấn dạng phân trang student
cursor = conn.cursor()
sql="SELECT * FROM student LIMIT 3 OFFSET 3"
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format("ID", "Code", "Name", "Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))
cursor.close()
print("-"*100)
# Hoàn thiện
print("Pagging !!!")
cursor = conn.cursor()
sql="SELECT count(*) FROM student"
cursor.execute(sql)
dataset = cursor.fetchone()
rowcount = dataset[0]

limit = 3
step = 3
for offset in range (0, rowcount, step):
    sql = f"SELECT * FROM student LIMIT {limit} OFFSET {offset}"
    cursor.execute(sql)

    dataset = cursor.fetchall()
    align='{0:<3} {1:<6} {2:<15} {3:<10}'
    print(align.format("ID", "Code", "Name", "Age"))
    for item in dataset:
        id=item[0]
        code=item[1]
        name=item[2]
        age=item[3]
        avatar=item[4]
        intro=item[5]
        print(align.format(id,code,name,age))
cursor.close()
print("-"*100)
# Thêm mới 1 student
cursor = conn.cursor()
sql="INSERT INTO student(Code, Name, Age) VALUES(%s, %s, %s)"
val = ("k237", "Trần Văn C", 47)

cursor.execute(sql, val)
conn.commit()
print(cursor.rowcount, " records inserted.")

cursor.close()
print("-"*100)
# Thêm mới nhều student
cursor = conn.cursor()

sql="insert into student (code,name,age) values (%s,%s,%s)"

val=[
    ("sv08","Trần Quyết Chiến",19),
    ("sv09","Hồ Thắng",22),
    ("sv10","Hoàng Hà",25),
     ]

cursor.executemany(sql,val)

conn.commit()

print(cursor.rowcount," record inserted")

cursor.close()
print("-"*100)
# Cập nhật tên sinh viên code = 'sv09' thành tên mới
cursor = conn.cursor()
sql="update student set name='Hoàng Lão Tà' where Code='sv09'"
cursor.execute(sql)

conn.commit()

print(cursor.rowcount," record(s) affected")
print("-"*100)
# Cập nhật tên sinh viên 09
cursor = conn.cursor()
sql="update student set name=%s where Code=%s"
val=('Hoàng Lão Tà','sv09')

cursor.execute(sql,val)

conn.commit()

print(cursor.rowcount," record(s) affected")
# Xoá student id = 14
conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
cursor = conn.cursor()
sql="DELETE from student where ID=14"
cursor.execute(sql)

conn.commit()

print(cursor.rowcount," record(s) affected")
print("-"*100)
# Xoá student có id = 13 với sql injection
cursor = conn.cursor()
sql = "DELETE from student where ID=%s"
val = (13,)

cursor.execute(sql, val)

conn.commit()

print(cursor.rowcount," record(s) affected")
