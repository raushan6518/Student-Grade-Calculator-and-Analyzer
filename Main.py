"""
Student Grade Calculator and Analyzer
Author: Raushan Kumar
VIT Email: raushan.25mei10023@vithhopal.ac.in
Course: Introduction to Problem Solving & Programming
"""

import json
import os
from datetime import datetime

# Grade point mapping according to VIT grading system
GRADE_POINTS = {
    'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'E': 5, 'F': 0, 'I': 0
}

class GradeCalculator:
    def __init__(self):
        self.student_data = {}
        self.load_data()
    
    def load_data(self):
        """Load student data from file if exists"""
        try:
            with open('student_data.json', 'r') as file:
                self.student_data = json.load(file)
        except FileNotFoundError:
            self.student_data = {}
    
    def save_data(self):
        """Save student data to file"""
        with open('student_data.json', 'w') as file:
            json.dump(self.student_data, file, indent=4)
    
    def calculate_grade_point(self, marks):
        """Calculate grade point based on marks"""
        if marks >= 90:
            return 'S', 10
        elif marks >= 80:
            return 'A', 9
        elif marks >= 70:
            return 'B', 8
        elif marks >= 60:
            return 'C', 7
        elif marks >= 50:
            return 'D', 6
        elif marks >= 40:
            return 'E', 5
        else:
            return 'F', 0
    
    def add_semester_grades(self):
        """Add courses and grades for a semester"""
        print("\n" + "="*50)
        print("ADD SEMESTER GRADES")
        print("="*50)
        
        student_id = input("Enter Student ID: ")
        semester = input("Enter Semester (e.g., '1-2025'): ")
        
        if student_id not in self.student_data:
            self.student_data[student_id] = {
                'name': input("Enter Student Name: "),
                'semesters': {}
            }
        
        self.student_data[student_id]['semesters'][semester] = {}
        courses = {}
        
        print(f"\nEntering courses for Semester {semester}")
        print("Enter 'done' when finished adding courses")
        
        while True:
            course_code = input("\nEnter Course Code: ")
            if course_code.lower() == 'done':
                break
            
            course_name = input("Enter Course Name: ")
            credits = float(input("Enter Credits: "))
            marks = float(input("Enter Marks Obtained: "))
            
            grade, grade_point = self.calculate_grade_point(marks)
            
            courses[course_code] = {
                'course_name': course_name,
                'credits': credits,
                'marks': marks,
                'grade': grade,
                'grade_point': grade_point
            }
            
            print(f"Grade assigned: {grade} (Grade Point: {grade_point})")
        
        self.student_data[student_id]['semesters'][semester] = courses
        self.save_data()
        print(f"\nGrades for Semester {semester} saved successfully!")
    
    def calculate_sgpa(self):
        """Calculate SGPA for a specific semester"""
        print("\n" + "="*50)
        print("CALCULATE SGPA")
        print("="*50)
        
        student_id = input("Enter Student ID: ")
        semester = input("Enter Semester: ")
        
        if student_id not in self.student_data or semester not in self.student_data[student_id]['semesters']:
            print("No data found for the given Student ID and Semester!")
            return
        
        courses = self.student_data[student_id]['semesters'][semester]
        total_credits = 0
        total_grade_points = 0
        
        print(f"\nSemester: {semester}")
        print("-" * 80)
        print(f"{'Course Code':<12} {'Course Name':<25} {'Credits':<8} {'Marks':<6} {'Grade':<6} {'Grade Point':<10}")
        print("-" * 80)
        
        for course_code, details in courses.items():
            credits = details['credits']
            grade_point = details['grade_point']
            
            total_credits += credits
            total_grade_points += credits * grade_point
            
            print(f"{course_code:<12} {details['course_name']:<25} {credits:<8} {details['marks']:<6} {details['grade']:<6} {grade_point:<10}")
        
        if total_credits > 0:
            sgpa = total_grade_points / total_credits
            print("-" * 80)
            print(f"SGPA for Semester {semester}: {sgpa:.2f}")
        else:
            print("No courses found!")
    
    def calculate_cgpa(self):
        """Calculate CGPA across all semesters"""
        print("\n" + "="*50)
        print("CALCULATE CGPA")
        print("="*50)
        
        student_id = input("Enter Student ID: ")
        
        if student_id not in self.student_data:
            print("Student not found!")
            return
        
        total_credits_all = 0
        total_grade_points_all = 0
        
        print(f"\nCGPA Calculation for {self.student_data[student_id]['name']}")
        print("=" * 60)
        
        for semester, courses in self.student_data[student_id]['semesters'].items():
            semester_credits = 0
            semester_grade_points = 0
            
            for course_code, details in courses.items():
                credits = details['credits']
                grade_point = details['grade_point']
                
                semester_credits += credits
                semester_grade_points += credits * grade_point
            
            if semester_credits > 0:
                sgpa = semester_grade_points / semester_credits
                total_credits_all += semester_credits
                total_grade_points_all += semester_grade_points
                
                print(f"Semester {semester}: SGPA = {sgpa:.2f}, Credits = {semester_credits}")
        
        if total_credits_all > 0:
            cgpa = total_grade_points_all / total_credits_all
            print("=" * 60)
            print(f"Overall CGPA: {cgpa:.2f}")
            print(f"Total Credits Completed: {total_credits_all}")
        else:
            print("No course data available!")
    
    def future_grade_predictor(self):
        """Predict required grades to achieve target CGPA"""
        print("\n" + "="*50)
        print("FUTURE GRADE PREDICTOR")
        print("="*50)
        
        student_id = input("Enter Student ID: ")
        
        if student_id not in self.student_data:
            print("Student not found!")
            return
        
        # Calculate current CGPA
        total_credits = 0
        total_grade_points = 0
        
        for semester, courses in self.student_data[student_id]['semesters'].items():
            for course_code, details in courses.items():
                total_credits += details['credits']
                total_grade_points += details['credits'] * details['grade_point']
        
        if total_credits == 0:
            print("No course data available!")
            return
        
        current_cgpa = total_grade_points / total_credits
        print(f"Current CGPA: {current_cgpa:.2f}")
        print(f"Total Credits Completed: {total_credits}")
        
        target_cgpa = float(input("\nEnter Target CGPA: "))
        future_credits = float(input("Enter Total Credits for Future Semesters: "))
        
        required_grade_points = (target_cgpa * (total_credits + future_credits) - total_grade_points) / future_credits
        
        print(f"\nTo achieve a CGPA of {target_cgpa:.2f}:")
        print(f"You need an average grade point of {required_grade_points:.2f} in your future {future_credits} credits")
        
        # Show what grades are needed
        print("\nThis corresponds to the following average grades:")
        if required_grade_points >= 9.5:
            print("Consistent 'S' grades required")
        elif required_grade_points >= 8.5:
            print("Mostly 'A' grades with some 'S' grades")
        elif required_grade_points >= 7.5:
            print("Mostly 'B' grades with some 'A' grades")
        else:
            print("Achievable with consistent 'C' grades or better")
    
    def display_student_report(self):
        """Display comprehensive student report"""
        print("\n" + "="*50)
        print("STUDENT ACADEMIC REPORT")
        print("="*50)
        
        student_id = input("Enter Student ID: ")
        
        if student_id not in self.student_data:
            print("Student not found!")
            return
        
        student = self.student_data[student_id]
        print(f"\nStudent Name: {student['name']}")
        print(f"Student ID: {student_id}")
        print(f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "="*80)
        
        total_credits_all = 0
        total_grade_points_all = 0
        
        for semester, courses in sorted(student['semesters'].items()):
            print(f"\nSemester: {semester}")
            print("-" * 80)
            print(f"{'Course Code':<12} {'Course Name':<25} {'Credits':<8} {'Marks':<6} {'Grade':<6} {'Grade Point':<10}")
            print("-" * 80)
            
            semester_credits = 0
            semester_grade_points = 0
            
            for course_code, details in courses.items():
                credits = details['credits']
                grade_point = details['grade_point']
                
                semester_credits += credits
                semester_grade_points += credits * grade_point
                total_credits_all += credits
                total_grade_points_all += credits * grade_point
                
                print(f"{course_code:<12} {details['course_name']:<25} {credits:<8} {details['marks']:<6} {details['grade']:<6} {grade_point:<10}")
            
            if semester_credits > 0:
                sgpa = semester_grade_points / semester_credits
                print("-" * 80)
                print(f"Semester SGPA: {sgpa:.2f} | Total Credits: {semester_credits}")
        
        if total_credits_all > 0:
            cgpa = total_grade_points_all / total_credits_all
            print("\n" + "="*80)
            print(f"OVERALL ACADEMIC SUMMARY")
            print(f"Final CGPA: {cgpa:.2f}")
            print(f"Total Credits Completed: {total_credits_all}")
            print("="*80)
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("STUDENT GRADE CALCULATOR AND ANALYZER")
        print("="*50)
        print("1. Add Semester Grades")
        print("2. Calculate SGPA")
        print("3. Calculate CGPA")
        print("4. Future Grade Predictor")
        print("5. Display Student Report")
        print("6. Exit")
        print("="*50)
    
    def run(self):
        """Main program loop"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self.add_semester_grades()
            elif choice == '2':
                self.calculate_sgpa()
            elif choice == '3':
                self.calculate_cgpa()
            elif choice == '4':
                self.future_grade_predictor()
            elif choice == '5':
                self.display_student_report()
            elif choice == '6':
                print("Thank you for using Student Grade Calculator!")
                break
            else:
                print("Invalid choice! Please enter a number between 1-6.")

# Run the application
if __name__ == "__main__":
    calculator = GradeCalculator()
    calculator.run()
