from flask import *
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mhv78601;PWD=i5mcF9bpp1sZvL1B",'','')

print(conn)


app=Flask(__name__)

@app.route('/')
def home():
    return render_template("homepage.html")


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

# Registration page routing

@app.route('/register1',methods=['GET'])
def register1():
    x = [x for x in request.args.values()]
    print(x)
    NAME=x[0]
    EMAIL=x[1]
    PASSWORD=x[2]
    sql = "SELECT * FROM register WHERE EMAIL =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,EMAIL)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return render_template('login.html', pred="You are already a member, please login using your details")
    else:
        insert_sql = "INSERT INTO  REGISTER VALUES (?, ?, ?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, NAME)
        ibm_db.bind_param(prep_stmt, 2, EMAIL)
        ibm_db.bind_param(prep_stmt, 3, PASSWORD)
        ibm_db.execute(prep_stmt)
        return render_template('login.html', pred="Registration Successful, please login using your details")
       

   
@app.route('/login1',methods=['GET'])
def login1():
    NAME = request.args.get('uname')
    EMAIL = request.args.get('em')
    sql = "SELECT * FROM REGISTER WHERE NAME =? AND EMAIL=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,NAME)
    ibm_db.bind_param(stmt,2,EMAIL)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print (account)
    print(NAME,EMAIL)
    if account:
        return render_template('login.html', pred="Login successful")
    else:
        return render_template('login.html', pred="Login unsuccessful. Incorrect username/password !") 


if __name__=="__main__":
    app.run(debug=True,port=8080)
