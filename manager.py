import json
import os
from typing import Dict, List
from student import Student

class StudentManager:
    def __init__(self, filename: str = "students.json"):
        self.filename = filename
        self.students: Dict[str, Student] = {}
        self.load_students()

    def load_students(self):
        """💾 Automatic Data Loading from JSON"""
        if not os.path.exists(self.filename):
            self.students = {}
            return
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.students = {str(s_id): Student.from_dict(info) for s_id, info in data.items() if isinstance(info, dict)}
                else:
                    self.students = {}
        except (json.JSONDecodeError, KeyError, TypeError):
            self.students = {}

    def save_students(self):
        """💾 Automatic Data Storage using JSON"""
        try:
            with open(self.filename, 'w') as file:
                serialized = {s_id: student.to_dict() for s_id, student in self.students.items()}
                json.dump(serialized, file, indent=4)
        except IOError as e:
            raise IOError(f"File write error: {e}")

    def add_student(self, student_id: str, name: str, grade: str) -> Student:
        """✅ Unique Student ID Validation & Add"""
        clean_id = Student.validate_id(student_id)
        if clean_id in self.students:
            raise ValueError(f"Student with ID '{clean_id}' already exists!")
        
        new_student = Student(clean_id, name, grade)
        self.students[clean_id] = new_student
        self.save_students()
        return new_student

    def update_student(self, student_id: str, name: str, grade: str) -> Student:
        """✏️ Update Student Details"""
        clean_id = Student.validate_id(student_id)
        if clean_id not in self.students:
            raise KeyError(f"Student with ID '{clean_id}' not found!")
        
        updated_student = Student(clean_id, name, grade)
        self.students[clean_id] = updated_student
        self.save_students()
        return updated_student

    def delete_student(self, student_id: str):
        """❌ Delete Student Record"""
        clean_id = Student.validate_id(student_id)
        if clean_id not in self.students:
            raise KeyError(f"Student with ID '{clean_id}' not found!")
        del self.students[clean_id]
        self.save_students()

    def get_all_students(self) -> List[Student]:
        """📋 View All Students"""
        return list(self.students.values())

    def search_student(self, query: str) -> List[Student]:
        """🔍 Search Student by ID or Name"""
        query = query.strip().lower()
        if not query:
            return self.get_all_students()
        
        results = []
        for student in self.students.values():
            if query in student.id.lower() or query in student.name.lower():
                results.append(student)
        return results

    def get_total_count(self) -> int:
        """📊 Display Total Number of Students"""
        return len(self.students)