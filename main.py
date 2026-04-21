# import json
# def load_data():
#     try:
#         with open("student.json","r") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {}
    
# def save_data(student):
#     with open("Student.json","w") as file:
#         json.dump(student,file,indent=4)
    
# def add_students(student):
#     ch=''
#     while ch!='exit':
#         ch=input("Do you want to add student details?")
#         if ch in['yes','ok','ya']:
#             st_id=input("Enter student ID")
#             if st_id in student.keys():
#                 print(f"Student ID {st_id} already exist!")
#             else:
#                 st_name=input("Enter student name")
#                 no_sub=int(input("Enter number of subjects"))
#                 st_marks=int(input("Enter student total marks"))
#                 percent=int((st_marks*100)/(no_sub*100))
#                 grade=grade_check(percent)
#                 #combined in function
#                 # if percent>=80:
#                 #     grade="Distinction"
#                 # elif percent>=70:
#                 #     grade="First Class"
#                 # elif percent>=60:
#                 #     grade="second Class"
#                 # elif percent>35:
#                 #     grade="Pass"
#                 # else:
#                 #     grade="Fail"
                
#                 student[st_id]={
#                     "name":st_name,
#                     "no_sub":no_sub,
#                     "Total_marks":st_marks,
#                     "Percentage":percent,
#                     "Grade":grade
#                 }
#                 save_data(student)
#                 print(f"Student ID:{st_id}\nStudent Name:{student[st_id]['name']} \n Grade: {student[st_id]['Grade']}\n{percent}added successfully!")
#     return student

# def grade_check(percent):
#     if percent>=80:
#         grade="Distinction"
#     elif percent>=70:
#         grade="First Class"
#     elif percent>=60:
#         grade="second Class"
#     elif percent>35:
#         grade="Pass"
#     else:
#         grade="Fail"
#     return grade

# def display_students(student):
    
#     for st_id, details in student.items():
#         print(f"Student ID: {st_id}\nName: {details['name']}\nTotal Marks: {details['Total_marks']}\nPercentage: {details['Percentage']}\nGrade: {details['Grade']}")
#     print(student)

# def search_student(student):
#     st_id=input("Enter ID to search student details")
#     if st_id in student.keys():
#         print(f"Student ID: {st_id}\nStudent Name: {student[st_id]['name']}\nTotal Marks:{student[st_id]['Total_marks']}")
#     else:
#         print(f"Student ID {st_id} not there in our database!")

# def update_student(student):
#     id=input("Enter student ID you want to update")
#     if id in student.keys():
#         name=input("Enter new name")
#         sub=int(input("Enter no of subjects"))
#         total_marks=int(input("Enter updated total marks"))
#         percent=int((total_marks*100)/(100*sub))
#         grade=grade_check(percent)
#         student[id]={"name":name,
#                     "no_sub":sub,
#                     "Total_marks":total_marks,
#                     "Percentage":percent,
#                     "Grade":grade}
#         save_data(student)
#         print(f"Name:{name}\nNo of subjects:{sub}\nTotal Marks:{total_marks}\nPercent:{percent}\nGrade:{grade}\n Updated successfully for Student ID '{id}'")
        
#     else:
#         print(f"Student ID '{id}'not present in our database!")

# if __name__=="__main__":
#     student={}
#     load_data()
#     add_students(student)
#     print(student.keys())
#     display_students(student)
#     search_student(student)
#     update_student(student)


import sqlite3 as sql
conn=sql.connect('student.db')
c=conn.cursor()
emp_1=Students('Abhi',101,5)
emp_2=Students('Abhi',102,6)
c.execute("Insert into employees values(?,?,?)",(emp_1.Name,emp_1.ID,emp_1.subjects))
conn.commit()

# # c.execute("""CREATE Table student(Name text,
#           ID integer primary key,
#           Subjects integer)""")
# c.execute("Insert Into student values('Abhi',101,5)")
c.execute("select *from student where name='Abhi'")
print(c.fetchall())
conn.commit()
conn.close()