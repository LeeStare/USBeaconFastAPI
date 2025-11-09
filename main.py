from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- 允許 Android 或瀏覽器存取 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 建議部署後須更改
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MySQL 連線設定 ---
db_config = {
    "host": "tpbyud.h.filess.io",
    "user": "USBeaconDataBase_fieldtent",
    "password": "6c4168e2d77d343677613c3b67dea32a211ecad7",
    "database": "USBeaconDataBase_fieldtent",
}

@app.get("/")
def home():
    return {"message": "FastAPI is running on Render"}

@app.get("/users")
def get_users():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM userdata LIMIT 5;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 定義前端送來的資料格式
class AccountInfo(BaseModel):
    account: str
    password: str

@app.post("/check_account_password")
def check_account_password(data: AccountInfo):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT account, password FROM userdata WHERE account = %s AND password = %s"
        cursor.execute(sql, (data.account, data.password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return {"exist": True}
        else:
            return {"exist": False}

    except Exception as e:
        return {"error": str(e)}

@app.get("/check_account_exist")
def check_account_exist(account: str):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT account FROM `userdata` WHERE account = '%s'"
        cursor.execute(sql, account)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return {"exist": True}
        else:
            return {"exist": False}

    except Exception as e:
        return {"error": str(e)}

@app.get("/get_user_name")
def get_user_name(account: str):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT user_name FROM `userdata` WHERE account = '%s'"
        cursor.execute(sql, account)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return {"exist": True}
        else:
            return {"exist": False}

    except Exception as e:
        return {"error": str(e)}

@app.get("/get_class_name")
def get_class_name():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT className,flag FROM `class` WHERE flag = '1'";
        cursor.execute(sql)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return {"exist": True}
        else:
            return {"exist": False}

    except Exception as e:
        return {"error": str(e)}
    
class createRequest(BaseModel):
    account: str
    password:str
    user_name: str
    phone_number: str

@app.post("/create_user")
def create_user(data: createRequest):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = """
        INSERT INTO userdata (account, password, user_name, phone_number)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (data.account, data.password, data.user_name, data.phone_number))
        conn.commit()

        cursor.close()
        conn.close()
        return {"success": True, "message": "使用者註冊成功"}
    except Exception as e:
        return {"success": False, "error": str(e)}