from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Smart Agriculture API",
    description="Smart Agri API Connected With PostgreSQL",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# PostgreSQL Connection
# =========================================================

def get_connection():

    # Render PostgreSQL DATABASE_URL
    database_url = os.getenv("DATABASE_URL")

    if database_url:

        # Convert postgres:// to postgresql:// if required
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://",
                "postgresql://",
                1
            )

        return psycopg2.connect(database_url)

    # =====================================================
    # LOCAL POSTGRESQL
    # =====================================================

    return psycopg2.connect(
        host="localhost",
        database="ml_database",
        user="postgres",
        password="admin",
        port=5432
    )


# =========================================================
# CREATE FARMERS TABLE
# =========================================================

def create_table():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL,
                dob VARCHAR(20),
                gender VARCHAR(20),
                address TEXT
            )
        """)

        conn.commit()

        print("Database table 'farmers' is ready.")

    except Exception as e:

        print("Database error:", e)
        raise

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# APPLICATION STARTUP
# =========================================================

@app.on_event("startup")
def startup_event():

    create_table()


# =========================================================
# REQUEST MODEL
# =========================================================

class RegisterUser(BaseModel):

    fullname: str
    email: str
    password: str
    dob: str
    gender: str
    address: str


# =========================================================
# HOME API
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Smart Agri API Connected With PostgreSQL",
        "status": "success"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1")

        cursor.fetchone()

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:

        return {
            "status": "unhealthy",
            "database": "not connected",
            "error": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# REGISTER API
# =========================================================

@app.post("/register")
def register(user: RegisterUser):

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # -------------------------------------------------
        # Check existing email
        # -------------------------------------------------

        cursor.execute(
            "SELECT id FROM farmers WHERE email = %s",
            (user.email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # -------------------------------------------------
        # Insert farmer
        # -------------------------------------------------

        query = """
            INSERT INTO farmers
            (
                fullname,
                email,
                password,
                dob,
                gender,
                address
            )
            VALUES
            (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        cursor.execute(
            query,
            (
                user.fullname,
                user.email,
                user.password,
                user.dob,
                user.gender,
                user.address
            )
        )

        user_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "message": "Registration Saved Successfully",
            "id": user_id,
            "name": user.fullname,
            "email": user.email
        }

    except HTTPException:

        raise

    except Exception as e:

        if conn:
            conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# GET ALL FARMERS
# =========================================================

@app.get("/farmers")
def get_farmers():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                fullname,
                email,
                dob,
                gender,
                address
            FROM farmers
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        data = []

        for row in rows:

            data.append({
                "id": row[0],
                "fullname": row[1],
                "email": row[2],
                "dob": row[3],
                "gender": row[4],
                "address": row[5]
            })

        return data

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# =========================================================
# GET SINGLE FARMER
# =========================================================

@app.get("/farmers/{farmer_id}")
def get_farmer(farmer_id: int):

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                fullname,
                email,
                dob,
                gender,
                address
            FROM farmers
            WHERE id = %s
        """, (farmer_id,))

        row = cursor.fetchone()

        if not row:

            raise HTTPException(
                status_code=404,
                detail="Farmer not found"
            )

        return {
            "id": row[0],
            "fullname": row[1],
            "email": row[2],
            "dob": row[3],
            "gender": row[4],
            "address": row[5]
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()
