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
def check_if_exist_account(data: AccountInfo):
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
def check_if_exist_account():
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