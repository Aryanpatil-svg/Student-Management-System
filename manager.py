import json
import os
from student import Student


class StudentManager:
    def __init__(self):
        self.filename = "students.json"
        self.students = []
        self.load_students()

    def load_students(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                try:
                    data = json.load(file)
                    self.students = [
                        Student(s["student_id"], s["name"], s["grade"])
                        for s in data
                    ]
                except:
                    self.students = []

    def save_students(self):
        with open(self.filename, "w") as file:
            json.dump([s.to_dict() for s in self.students], file, indent=4)

    def add_student(self, student_id, name, grade):
        for student in self.students:
            if student.student_id == student_id:
                print("❌ Student ID already exists!")
                return

        self.students.append(Student(student_id, name, grade))
        self.save_students()
        print("✅ Student Added Successfully!")

    def list_students(self):
        if not self.students:
            print("\nNo Students Found!\n")
            return

        print("\n" + "=" * 55)
        print("{:<15}{:<25}{:<10}".format("ID", "NAME", "GRADE"))
        print("=" * 55)

        for student in self.students:
            print("{:<15}{:<25}{:<10}".format(
                student.student_id,
                student.name,
                student.grade
            ))

        print("=" * 55)

    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                print("\nStudent Found")
                print(f"ID    : {student.student_id}")
                print(f"Name  : {student.name}")
                print(f"Grade : {student.grade}")
                return

        print("❌ Student Not Found!")

    def update_student(self, student_id, new_name, new_grade):
        for student in self.students:
            if student.student_id == student_id:
                student.name = new_name
                student.grade = new_grade
                self.save_students()
                print("✅ Student Updated Successfully!")
                return

        print("❌ Student Not Found!")

    def delete_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                self.save_students()
                print("✅ Student Deleted Successfully!")
                return

        print("❌ Student Not Found!")

    def total_students(self):
        print(f"\n📚 Total Students : {len(self.students)}")