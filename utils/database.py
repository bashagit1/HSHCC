import sqlite3
from utils.auth import hash_password, add_user, get_user

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Initialize all tables
    create_users_table(cursor)
    create_residents_table(cursor)
    create_health_table(cursor)
    create_staff_table(cursor)
    create_messages_table(cursor)
    create_meal_plans_table(cursor)
    create_activities_table(cursor)
    create_cognitive_stimulation_table(cursor)
    create_smart_room_table(cursor)
    create_medication_table(cursor)
    create_visitor_table(cursor)
    create_staff_performance_table(cursor)
    create_doctors_table(cursor)
    create_appointments_table(cursor)
    create_doctor_updates_table(cursor)

    
    # Add sample data
    add_sample_users(cursor)
    add_sample_doctors(cursor)

    conn.commit()
    conn.close()

# Table creation functions
def create_users_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

def create_residents_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS residents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        room_number TEXT,
        medical_history TEXT
    )
    """)

def create_health_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        blood_pressure TEXT,
        heart_rate INTEGER,
        sugar_level REAL,
        FOREIGN KEY (resident_id) REFERENCES residents (id)
    )
    """)

def create_staff_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        assigned_residents TEXT,
        contact_info TEXT
    )
    """)

def create_messages_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_name TEXT NOT NULL,
        receiver_name TEXT NOT NULL,
        message TEXT NOT NULL,
        date TEXT NOT NULL,
        resident_id INTEGER NOT NULL,
        FOREIGN KEY (resident_id) REFERENCES residents (id)
    )
    """)

def create_meal_plans_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meal_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        breakfast TEXT,
        lunch TEXT,
        dinner TEXT,
        snacks TEXT,
        FOREIGN KEY (resident_id) REFERENCES residents (id)
    )
    """)

def create_activities_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        activity_name TEXT NOT NULL,
        activity_type TEXT NOT NULL,
        description TEXT,
        time TEXT NOT NULL,
        FOREIGN KEY (resident_id) REFERENCES residents (id)
    )
    """)

def create_cognitive_stimulation_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cognitive_stimulation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        activity_type TEXT NOT NULL,
        time_spent INTEGER NOT NULL,
        description TEXT,
        FOREIGN KEY (resident_id) REFERENCES residents (id)
    )
    """)

def create_smart_room_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS smart_room (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_id INTEGER NOT NULL,
        room_temperature REAL NOT NULL,
        light_status TEXT NOT NULL,
        motion_status TEXT NOT NULL,
        last_updated TEXT NOT NULL,
        FOREIGN KEY (resident_id) REFERENCES residents (id)
    )
    """)

def create_medication_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_id INTEGER NOT NULL,
        medication_name TEXT NOT NULL,
        dosage TEXT NOT NULL,
        frequency TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        reminder_times TEXT NOT NULL,
        FOREIGN KEY (resident_id) REFERENCES residents (id)
    )
    """)

def create_visitor_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_id INTEGER NOT NULL,
        visitor_name TEXT NOT NULL,
        visit_date TEXT NOT NULL,
        purpose TEXT NOT NULL,
        approval_status TEXT NOT NULL,
        FOREIGN KEY (resident_id) REFERENCES residents (id)
    )
    """)

def create_staff_performance_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff_performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id INTEGER NOT NULL,
        task TEXT NOT NULL,
        completion_status TEXT NOT NULL,
        feedback TEXT,
        performance_date TEXT NOT NULL
    )
    """)

def create_doctors_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        contact_info TEXT NOT NULL
    )
    """)

def create_appointments_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (resident_id) REFERENCES residents (id),
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    )
    """)

def create_doctor_updates_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctor_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER,
        resident_id INTEGER,
        appointment_id INTEGER,
        prescribed_medicines TEXT,
        meal_instructions TEXT,
        care_recommendations TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (doctor_id) REFERENCES doctors (id),
        FOREIGN KEY (resident_id) REFERENCES residents (id),
        FOREIGN KEY (appointment_id) REFERENCES appointments (id)
    )
    """)


# Sample data functions
def add_sample_users(cursor):
    # Sample users with the roles correctly defined
    sample_users = [
        ("admin", hash_password("admin123"), "admin"),
        ("caregiver1", hash_password("care123"), "caregiver"),
        ("family1", hash_password("family123"), "family"),
        ("doctor1", hash_password("doctor123"), "doctor")  # Added doctor
    ]
    
    # Insert the sample users into the users table, ignoring duplicates
    cursor.executemany("""
    INSERT OR IGNORE INTO users (username, password, role) 
    VALUES (?, ?, ?)
    """, sample_users)



# Add sample doctors
def add_sample_doctors(cursor):
    sample_doctors = [
        ("Dr. Smith", "Cardiology", "123-456-7890"),
        ("Dr. Johnson", "Neurology", "098-765-4321"),
        ("Dr. Lee", "Geriatrics", "555-555-5555")
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO doctors (name, specialization, contact_info)
    VALUES (?, ?, ?)
    """, sample_doctors)




# Insert a new resident
def add_resident(name, age, room_number, medical_history):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO residents (name, age, room_number, medical_history)
    VALUES (?, ?, ?, ?)
    """, (name, age, room_number, medical_history))
    conn.commit()
    conn.close()

# Fetch all residents
def get_residents():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM residents")
    residents = cursor.fetchall()
    conn.close()
    return residents

# Insert health data
def add_health_record(resident_id, date, blood_pressure, heart_rate, sugar_level):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO health_records (resident_id, date, blood_pressure, heart_rate, sugar_level)
    VALUES (?, ?, ?, ?, ?)
    """, (resident_id, date, blood_pressure, heart_rate, sugar_level))
    conn.commit()
    conn.close()

# Fetch health records for a resident
def get_health_records(resident_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT date, blood_pressure, heart_rate, sugar_level
    FROM health_records
    WHERE resident_id = ?
    ORDER BY date DESC
    """, (resident_id,))
    records = cursor.fetchall()
    conn.close()
    return records


# Insert staff member data
def add_staff(name, role, assigned_residents, contact_info):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO staff (name, role, assigned_residents, contact_info)
    VALUES (?, ?, ?, ?)
    """, (name, role, assigned_residents, contact_info))
    conn.commit()
    conn.close()

# Fetch all staff members
def get_staff():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff")
    staff = cursor.fetchall()
    conn.close()
    return staff


# Insert a message
def add_message(sender_name, receiver_name, message, date, resident_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO messages (sender_name, receiver_name, message, date, resident_id)
    VALUES (?, ?, ?, ?, ?)
    """, (sender_name, receiver_name, message, date, resident_id))
    conn.commit()
    conn.close()

# Fetch messages for a resident
def get_messages_for_resident(resident_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT sender_name, receiver_name, message, date
    FROM messages
    WHERE resident_id = ?
    ORDER BY date DESC
    """, (resident_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages


# Insert a new meal plan
def add_meal_plan(resident_id, date, breakfast, lunch, dinner, snacks):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO meal_plans (resident_id, date, breakfast, lunch, dinner, snacks)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (resident_id, date, breakfast, lunch, dinner, snacks))
    conn.commit()
    conn.close()

# Fetch meal plans for a resident
def get_meal_plans_for_resident(resident_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT date, breakfast, lunch, dinner, snacks
    FROM meal_plans
    WHERE resident_id = ?
    ORDER BY date DESC
    """, (resident_id,))
    meal_plans = cursor.fetchall()
    conn.close()
    return meal_plans


# Insert a new activity plan
def add_activity_plan(resident_id, date, activity_name, activity_type, description, time):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO activities (resident_id, date, activity_name, activity_type, description, time)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (resident_id, date, activity_name, activity_type, description, time))
    conn.commit()
    conn.close()

# Fetch activities for a resident
def get_activities_for_resident(resident_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT date, activity_name, activity_type, description, time
    FROM activities
    WHERE resident_id = ?
    ORDER BY date DESC
    """, (resident_id,))
    activities = cursor.fetchall()
    conn.close()
    return activities


# Insert a new cognitive stimulation activity
def add_cognitive_activity(resident_id, date, activity_type, time_spent, description):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO cognitive_stimulation (resident_id, date, activity_type, time_spent, description)
    VALUES (?, ?, ?, ?, ?)
    """, (resident_id, date, activity_type, time_spent, description))
    conn.commit()
    conn.close()

# Fetch cognitive stimulation activities for a resident
def get_cognitive_activities_for_resident(resident_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT date, activity_type, time_spent, description
    FROM cognitive_stimulation
    WHERE resident_id = ?
    ORDER BY date DESC
    """, (resident_id,))
    activities = cursor.fetchall()
    conn.close()
    return activities



# Insert or update smart room data
def add_smart_room_data(resident_id, room_temperature, light_status, motion_status, last_updated):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO smart_room (resident_id, room_temperature, light_status, motion_status, last_updated)
    VALUES (?, ?, ?, ?, ?)
    """, (resident_id, room_temperature, light_status, motion_status, last_updated))
    conn.commit()
    conn.close()

# Fetch smart room data for a resident
def get_smart_room_data(resident_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT room_temperature, light_status, motion_status, last_updated
    FROM smart_room
    WHERE resident_id = ?
    """, (resident_id,))
    data = cursor.fetchone()
    conn.close()
    return data



# Insert Medication Record
def add_medication(resident_id, medication_name, dosage, frequency, start_date, end_date, reminder_times):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO medications (resident_id, medication_name, dosage, frequency, start_date, end_date, reminder_times)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (resident_id, medication_name, dosage, frequency, start_date, end_date, reminder_times))
    conn.commit()
    conn.close()

# Fetch Medications for a Resident
def get_medications(resident_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, medication_name, dosage, frequency, start_date, end_date, reminder_times
    FROM medications
    WHERE resident_id = ?
    """, (resident_id,))
    medications = cursor.fetchall()
    conn.close()
    return medications

# Mark Medication as Administered
def mark_medication_as_administered(medication_id):
    # Add logic here if needed, such as logging the event
    pass



# Insert Visitor Record
def add_visitor(resident_id, visitor_name, visit_date, purpose, approval_status="Pending"):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO visitors (resident_id, visitor_name, visit_date, purpose, approval_status)
    VALUES (?, ?, ?, ?, ?)
    """, (resident_id, visitor_name, visit_date, purpose, approval_status))
    conn.commit()
    conn.close()

# Fetch Visitors for a Resident
def get_visitors(resident_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, visitor_name, visit_date, purpose, approval_status
    FROM visitors
    WHERE resident_id = ?
    """, (resident_id,))
    visitors = cursor.fetchall()
    conn.close()
    return visitors

# Update Visitor Approval Status
def update_visitor_status(visitor_id, status):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE visitors
    SET approval_status = ?
    WHERE id = ?
    """, (status, visitor_id))
    conn.commit()
    conn.close()


# Insert Staff Performance Record
def add_staff_performance(staff_id, task, completion_status, feedback, performance_date):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO staff_performance (staff_id, task, completion_status, feedback, performance_date)
    VALUES (?, ?, ?, ?, ?)
    """, (staff_id, task, completion_status, feedback, performance_date))
    conn.commit()
    conn.close()

# Fetch Performance Records for Staff
def get_staff_performance(staff_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT task, completion_status, feedback, performance_date
    FROM staff_performance
    WHERE staff_id = ?
    ORDER BY performance_date DESC
    """, (staff_id,))
    records = cursor.fetchall()
    conn.close()
    return records
# Fetch All Staff
def get_all_staff():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, name FROM staff
    """)
    staff = cursor.fetchall()
    conn.close()
    return staff



# Add these calls to initialize the tables in your app startup (inside init_db function)

def get_doctors():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        return cursor.fetchall()

def add_appointment(resident_id, doctor_id, appointment_date, notes):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO appointments (resident_id, doctor_id, appointment_date, notes)
        VALUES (?, ?, ?, ?);
        """, (resident_id, doctor_id, appointment_date, notes))
        conn.commit()


# In utils/database.py


# Function to establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Replace with your database file
    return conn
