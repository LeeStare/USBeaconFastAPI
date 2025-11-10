from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
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
    

class FlagRequest(BaseModel):
    user: str

@app.post("/class/setFlagZero")
def set_flag_zero(data: FlagRequest):
    try:
        if data.user != "410777000":
            return {"success": False, "message": "沒有權限執行"}
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "UPDATE class SET flag = '0'"
        cursor.execute(sql)
        cursor.commit()

        cursor.close()
        conn.close()

        return {"success": True, "message": "所有課程 flag 已設為0"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
@app.get("/get_all_class_name")
def get_all_class_name():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT className FROM class")
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        class_list = [r[0] for r in result]
        return {"class_names": class_list}
    except Exception as e:
        return {"error": str(e)}
    
class ClassData(BaseModel):
    className: str
    classroom: str
    day: str
    time: str
    quantity: int
    flag: int

@app.post("/class_create")
def class_create(data: ClassData):
    try:
        # 連線資料庫
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 使用 parameterized query 避免 SQL injection
        sql = """
            INSERT INTO class (className, classroom, day, time, quantity, flag)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (data.className, data.classroom, data.day, data.time, data.quantity, data.flag))
        conn.commit()

        cursor.close()
        conn.close()

        return {
            "success": True,
            "message": f"課程 {data.className} 已成功新增"
        }

    except Error as e:
        return {
            "success": False,
            "message": f"資料庫錯誤: {str(e)}"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"其他錯誤: {str(e)}"
        }