class Student:
    def __init__(self, student_id: str, name: str, grade: str):
        self.id = self.validate_id(student_id)
        self.name = self.validate_name(name)
        self.grade = self.validate_grade(grade)

    @staticmethod
    def validate_id(student_id: str) -> str:
        clean_id = str(student_id).strip()
        if not clean_id:
            raise ValueError("Student ID cannot be empty!")
        return clean_id

    @staticmethod
    def validate_name(name: str) -> str:
        clean_name = str(name).strip()
        if not clean_name:
            raise ValueError("Name cannot be empty!")
        return clean_name

    @staticmethod
    def validate_grade(grade: str) -> str:
        clean_grade = str(grade).strip().upper()
        if not clean_grade:
            raise ValueError("Grade cannot be empty!")
        return clean_grade

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "grade": self.grade}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["id"], data["name"], data["grade"])