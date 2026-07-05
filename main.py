from manager import StudentManager

manager = StudentManager()

while True:

    print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Total Students")
    print("7. Exit")

    choice = input("\nEnter Choice : ")

    if choice == "1":

        student_id = input("Enter Student ID : ")
        name = input("Enter Name : ")
        grade = input("Enter Grade : ")

        manager.add_student(student_id, name, grade)

    elif choice == "2":

        manager.list_students()

    elif choice == "3":

        student_id = input("Enter Student ID : ")
        manager.search_student(student_id)

    elif choice == "4":

        student_id = input("Enter Student ID : ")
        name = input("Enter New Name : ")
        grade = input("Enter New Grade : ")

        manager.update_student(student_id, name, grade)

    elif choice == "5":

        student_id = input("Enter Student ID : ")
        manager.delete_student(student_id)

    elif choice == "6":

        manager.total_students()

    elif choice == "7":

        print("\nThank You For Using Student Management System ❤️")
        break

    else:

        print("❌ Invalid Choice!")