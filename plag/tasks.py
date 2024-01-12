from celery import shared_task
import os
from .models import Assingment, Students_Assigments
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from io import BytesIO
from django.http import HttpResponse
from .models import Contact
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


@shared_task (bind=True)

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

def submit(request):

    
    assingments = Students_Assigments.objects.filter(key = assingment_key)

    files = []
    notes = []

    for assignment in assingments:
        # Assuming the 'document' field contains file content
        if assignment.document.name.endswith('.pdf'):
            text = process_pdf(assignment.document.path)
        elif assignment.document.name.endswith('.docx'):
            text = convert_docx_to_text(assignment.document.path)
        else:
            # Assume TXT file format
            text = open(assignment.document.path, encoding='utf-8').read()

        notes.append(text)
        files.append(assignment.Sname)

    # Run plagiarism checks and get the results
    plagiarism_results = run_plagiarism_checker(files, notes)

    # Pass the results to the template
    context = {'plagiarism_results': plagiarism_results}
 
    return








#test start
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

    stu = Students_Assigments.objects.all()
    tech = User.objects.filter(is_staff = 'True') 
    teach = Assingment.objects.all()
    
    file = []
    skey = []
    mail = []
    tkey = []
    
    for s in stu:
        file.append(s.document.name)
        skey.append(s.key)
    
    for t in tech:
        mail.append(t.email)

    for tq in teach:
        tkey.append(tq.key)

    print(file)
    return render(request, "Login_Student.html")
    
'''

    files = []
    notes = []

    for f in file:
        files.append(f)
            
        if f.endswith('.pdf'):
            text = process_pdf(f)
        #elif filename.endswith('.docx'):
         #   text = convert_docx_to_text(file_path)
        #else:  # Assume TXT file format
         #   text = open(file_path, encoding='utf-8').read()
        notes.append(text)
    checker_output = run_plagiarism_checker(files, notes)  # Pass 'files' to the function
    #Delete the Contact instance after processing
    #contact.delete()
    subject = 'Plagiarism Checker Results'
    message = f'Please find your plagiarism results.\n {checker_output}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [mail]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
 '''   
    

#test end
