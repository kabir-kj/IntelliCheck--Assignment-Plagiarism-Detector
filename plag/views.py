from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Assingment, Students_Assigments
from django.contrib.auth import logout
import random
from django.contrib.auth.decorators import login_required
import datetime
from datetime import timezone 
import sweetify

#test import
import os
from .models import Assingment, Students_Assigments
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from PyPDF2 import PdfReader
import docx2txt
import pdfplumber
import pytesseract
from PIL import Image
import io
import zipfile
#test import


def process_pdf(pdf_path):

    all_content = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text_content = page.extract_text()
            if text_content:
                all_content.append(text_content)
                all_content.append("\n")
            
            if page.images:
                #print("Images found:")
                for image_number, image_dict in enumerate(page.images):
                    image = image_dict['stream']
                    image_bytes = image.get_data()
                    pil_image = Image.open(io.BytesIO(image_bytes))          
                    image_content = pytesseract.image_to_string(pil_image)
                    all_content.append(image_content)
                    all_content.append("\n")
                    
    combined_text_content = ''.join(all_content)            
    return combined_text_content
    

def convert_docx_to_text(docx_path):
    text = docx2txt.process(docx_path)
    return text
'''
def run_plagiarism_checker(files, notes):
    output = []

    for i in range(len(notes) - 1):
        X = notes[i]
        for j in range(i + 1, len(notes)):
            Y = notes[j]
            X_list = word_tokenize(X)
            Y_list = word_tokenize(Y)
            sw = stopwords.words('english')
            l1 = []
            l2 = []
            X_set = {w for w in X_list if not w in sw}
            Y_set = {w for w in Y_list if not w in sw}
            rvector = X_set.union(Y_set)
            for w in rvector:
                if w in X_set:
                    l1.append(1)
                else:
                    l1.append(0)
                if w in Y_set:
                    l2.append(1)
                else:
                    l2.append(0)
            c = 0
            for a in range(len(rvector)):
                c += l1[a] * l2[a]
            cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
            similarity = (files[i] + " and " + files[j] + " similarity: ", cosine)
            #if cosine > 0.30:
            output.append(similarity)

    return output
'''

def index(request):   
    return render(request, "Login_Student.html")   




def index(request):
    
    return render(request, "Login_Student.html")


def Lteacher(request):
    if request.method =='POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, "Teacher_Dashboard.html")
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('Lteacher')

    else:
        return render(request, "Login_Teacher.html")

@login_required   
def Show_Student_assingment(request):
    Student = request.user
    content = {'user_name': Student.first_name}
    return render(request, "Verify_Assigment.html", content)

@login_required 
def Subassignments(request):

    if request.method == 'POST':
        Key = request.POST.get('Akey')
        Assigment = request.FILES.get('myfile')
        student = request.user
        Student_Name = student.first_name
        Student_ID = student.username
        
        file = Assingment.objects.get(key=Key)
        dead = file.deadline
        now = datetime.datetime.now(timezone.utc)

        if now<dead:

            if Assigment:
                Submit_Assigment = Students_Assigments(Sname = Student_Name,  S_iD =  Student_ID, key = Key, document = Assigment)
                Submit_Assigment.save()
            else:
                print('No File')

            content = {'user_name': student.first_name}
            return render(request, "Submit_Student_Assingment.html", content)
        else:
            Student = request.user
            content = {'user_name': Student.first_name}
            sweetify.error(request, 'Due date exceeded! Cannot accept any further submissions')
            return render(request, "Submit_Student_Assingment.html", content)


    else:
        Student = request.user
        content = {'user_name': Student.first_name}
        return render(request, "Submit_Student_Assingment.html", content)

def LStudent(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            context = {'user_name': user.first_name}
            return render(request, "Verify_Assigment.html", context)
        
        else:
            messages.error(request, 'Invalid Credentials')

            return redirect('LStudent')
    else:
        return render(request, "Login_Student.html")

@login_required
def keyverify(request):
    if request.method == 'POST':
        ykey = request.POST.get('Vkey')
        Student = request.user

        assingment = Assingment.objects.get(key = ykey)

        content = {'user_name': Student.first_name, 'teacher_name': assingment.Tname, 'Assingment_name': assingment.Aname, 'Document': assingment.document, 'Deadline': assingment.deadline}

        return render(request, "Show_Assigment.html", content)
    
    else: 
        Student = request.user
        content = {'user_name': Student.first_name}
        return render(request, "Show_Assigment.html", content)
     

def SStudent(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        student_id = request.POST.get('student_ID')
        pass1 = request.POST.get('pass1')
        cpass1 = request.POST.get('Cpass1')
        phone = request.POST.get('phone')

        if pass1 == cpass1:
            new_student = User.objects.create_user(first_name=name, email=email, username=student_id, password=pass1)
            new_student.save()
            print('user created')
        else:
            print('password not match')

        return redirect('LStudent')
    else:
        return render(request, "Signup_Student.html")

def STeacher(request):
    if request.method == 'POST':    
        name = request.POST.get('name')
        email = request.POST.get('email')
        Tid = request.POST.get('Teacher-ID')
        pass1 = request.POST.get('pass1')
        cpass1 = request.POST.get('pass2')
        phone = request.POST.get('phone')

        if pass1 == cpass1:
            new_teacher = User.objects.create_user(first_name=name, email=email, username=Tid, password=pass1)
            new_teacher.save()
            print('user created')
        else:
            print('password not match')
            
        return redirect('Lteacher')
    else:
        return render(request, "Signup_Teacher.html")

@login_required
def Sassingment(request):
    if request.method == 'POST':
        name = request.POST.get('Assingmnet_Name')
        date = request.POST.get('Deadline')
        file_uploads = request.FILES.get('file')
        teacher = request.user  # Assuming the user is a teacher

        def generate_key():
            x = random.randint(100, 9999)

            y = Assingment.objects.filter(key=x)

            if y.exists():
                return generate_key()
            else:
                return x

        Ukey = generate_key()

        if file_uploads:
            assingment = Assingment(Tname=teacher.first_name, T_iD=teacher.username, Aname=name, key=Ukey, deadline=date, document=file_uploads)
            assingment.save()

            context = {'Tname': teacher.first_name, 'E_ID': teacher.username, 'U_Key': Ukey, 'Aname': name, 'Deadline': date}

            return render(request, 'sucess.html', context)
        
        else:
            print("No file")

@login_required
def show_assignment_teacher(request):
    teacher = request.user

    x = teacher.username
    details = Assingment.objects.filter(T_iD = x)

    contents = {'assignments':  details}

    return render(request, "Show_Assingment_Teacher.html", contents)

def view_submissions(request, assingment_key):
    assingment = Students_Assigments.objects.filter(key = assingment_key)

    Students_Assigment_Details = {'assignments':  assingment}

    return render(request, "view_submission.html", Students_Assigment_Details)


def TDashboard(request):
    return render(request, "Teacher_Dashboard.html")

def SDashboard(request):
    return render(request, "Student_Assinment.html")

def Slogout(request):
    auth.logout(request)
    return redirect('LStudent')

def Tlogout(request):
    auth.logout(request)
    return redirect('Lteacher')
