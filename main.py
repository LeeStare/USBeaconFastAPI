from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- 允許 Android 或瀏覽器存取 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 建議部署後改成你的App網域
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