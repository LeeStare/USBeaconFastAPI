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
    "host": "sql12.freesqldatabase.com",
    "user": "sql12804805",
    "password": "8WkBTMX1nD",
    "database": "sql12804805",
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
    id: str
    password: str

@app.post("/check_account")
def check_if_exist_account(data: AccountInfo):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT account, password FROM userdata WHERE account = %s AND password = %s"
        cursor.execute(sql, (data.id, data.password))
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
def check_if_exist_account(id: str):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "SELECT account, password FROM userdata WHERE account = %s AND password = %s"
        cursor.execute(sql, (data.id, data.password))
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
def check_if_exist_account(id: str):
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