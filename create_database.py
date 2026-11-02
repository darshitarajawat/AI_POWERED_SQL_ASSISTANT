
import sqlite3

# 1. Create/connect to database
connection = sqlite3.connect("school.db")
cursor = connection.cursor()

# 2. Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    age INTEGER,
    marks REAL
)
""")

# 3. Create courses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    department TEXT,
    credits INTEGER
)
""")

# 4. Recreate enrollments table with student_name
# This removes the old enrollments table and its records.
cursor.execute("DROP TABLE IF EXISTS enrollments")

cursor.execute("""
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL,
    course_id INTEGER,
    grade TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
)
""")

# 5. Insert sample students
cursor.executemany("""
INSERT OR IGNORE INTO students
(student_id, name, department, age, marks)
VALUES (?, ?, ?, ?, ?)
""", [
    (1, "Aarav", "AI & Data Science", 21, 88),
    (2, "Priya", "AI and Data Science", 22, 92),
    (3, "Rahul", "Computer Science", 21, 76),
    (4, "Sneha", "Computer Science", 23, 95),
    (5, "Arjun", "AI and Data Science", 22, 81),
    (6, "Nisha", "Computer Science", 23, 85)
    
])

# 6. Insert sample courses
cursor.executemany("""
INSERT OR IGNORE INTO courses
(course_id, course_name, department, credits)
VALUES (?, ?, ?, ?)
""", [
    (1, "Machine Learning", "AI & Data Science", 4),
    (2, "Database Management", "Computer Science", 3),
    (3, "Data Analytics", "AI & Data Science", 3),
    (4, "Python Programming", "Computer Science", 4),
    (5, "Java", "Computer Science", 3)
])

# 7. Insert enrollments with enrollment IDs 101, 102, etc.
cursor.executemany("""
INSERT INTO enrollments
(enrollment_id, student_name, course_id, grade)
VALUES (?, ?, ?, ?)
""", [
    (101, "Aarav", 1, "A"),
    (102, "Priya", 3, "A"),
    (103, "Rahul", 2, "A"),
    (104, "Sneha", 4, "B"),
    (105, "Arjun", 1, "A"),
    (106, "Nisha", 2, "B")
])

# 8. Save and close database
connection.commit()
connection.close()

print("Database created successfully!")
print("Database name: school.db")
print("Tables: students, courses, enrollments")
