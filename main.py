from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PostgreSQL Connection
def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ml_database",
        user="postgres",      # <-- तुमचा PostgreSQL username
        password="admin",     # <-- तुमचा PostgreSQL password
        port="5432"
    )
    return conn


# Create Table
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmers (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        email VARCHAR(100),
        password VARCHAR(100),
        dob VARCHAR(20),
        gender VARCHAR(20),
        address TEXT
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()


create_table()


# Request Model
class RegisterUser(BaseModel):
    fullname: str
    email: str
    password: str
    dob: str
    gender: str
    address: str


# Home API
@app.get("/")
def home():
    return {
        "message": "Smart Agri API Connected With Database"
    }


# Register API
@app.post("/register")
def register(user: RegisterUser):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO farmers
    (fullname, email, password, dob, gender, address)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        user.fullname,
        user.email,
        user.password,
        user.dob,
        user.gender,
        user.address
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Registration Saved Successfully",
        "name": user.fullname
    }


# View All Data
@app.get("/farmers")
def get_farmers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, fullname, email, password, dob, gender, address
        FROM farmers
    """)

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "fullname": row[1],
            "email": row[2],
            "password": row[3],
            "dob": row[4],
            "gender": row[5],
            "address": row[6]
        })

    cursor.close()
    conn.close()

    return data