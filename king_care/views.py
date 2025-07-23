from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from king_care.models import *
from django.db.models import Sum, F

from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import random

# Create your views here.

@login_required(login_url='logout_dash/register/')
def dashboard(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_user_info = Hospital_reg.objects.get(email=user_identity_email)
    count_doctor = Doctor_signup.objects.all().count()
    doctor_timeline = Doctor_signup.objects.all()
    count_appointment = Add_appointment.objects.all().count()
    appointment_timeline = Add_appointment.objects.all()
    get_patient = Add_patient.objects.all().count()
    get_registered_patient = Patient_signup.objects.all().count()
    all = {'get_patient':get_patient, 'get_registered_patient':get_registered_patient, 'doctor_timeline':doctor_timeline, 'appointment_timeline':appointment_timeline, 'get_user_info':get_user_info, 'count_doctor':count_doctor, 'count_appointment':count_appointment}
    return render(request, 'receptionist/index.html', all)

def register(request):
    if request.method == 'POST':
        # Submit to Database
        get_fullName = request.POST.get('get_fullName')
        get_email = request.POST.get('get_email')
        get_phone = request.POST.get('get_phone')
        get_gender = request.POST.get('get_gender')
        get_username = request.POST.get('get_username')
        get_password = request.POST.get('get_password')

        if User.objects.filter(email=get_email).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Email already exists!!!, Please alter')
            return redirect("/dashboard/register/")
        elif User.objects.filter(username=get_username).exists(): # CHECK FOR THE SAME USERNAME
            messages.warning(request, 'Username already exists!!!, Please alter')
            return redirect("/dashboard/register/")
        else: # ELSE SUBMIT TO DATABASE
            if 'fileToUpload' in request.FILES:
                passport = request.FILES['fileToUpload']
            else:
                passport = 'abc.jpg'  
            submit_user = User.objects.create_user(password = get_password, username = get_username, first_name = get_fullName, email = get_email)
            submit_user.save()
            # name	email	gender	phone	dob	student_class	
            submit_others = Hospital_reg.objects.create(user=submit_user, fullName = get_fullName, email = get_email, phone = get_phone, gender = get_gender, profile_picture = passport, status='Pending')
            submit_others.save()
            messages.success(request, get_fullName + " have successfully registered. Your account is pending approval.")
            return redirect('/register/login')

    else:
        return render(request, 'receptionist/pages-register.html')

def login(request):
    if request.method == 'POST':
        get_username = request.POST.get('get_username')
        get_password = request.POST.get('get_password')

        user = auth.authenticate(username=get_username, password=get_password)
        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                messages.success(request, "Admin login Successful")
                return redirect('/admin_dash/')  # Redirect superuser to the dashboard or any desired page
            else:
                receptionist_signup = Hospital_reg.objects.get(user=user)
                if receptionist_signup.status == 'Pending':
                    messages.error(request, "Your account is still pending approval.")
                    return redirect('/register/login')
                else:
                    auth.login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect('/dashboard')  # Redirect regular user to the dashboard or any desired page
        else:
            messages.error(request, "Your login details are wrong")
            return redirect('/register/login')
    else:
        return render(request, 'receptionist/pages-login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, "Loggout Successful")
    return redirect('/logout/logout_dash')

def logout_dash(request):
    return render(request, 'general/logout_dash.html')

@login_required(login_url='logout_dash/register/')
def add_patient(request):
    if request.method == 'POST':
        get_fullName = request.POST.get('get_fullName')
        get_patient_no = request.POST.get('get_patient_no')
        get_phone = request.POST.get('get_phone')
        get_gender = request.POST.get('get_gender')
        get_dob = request.POST.get('get_dob')
        get_blood_group = request.POST.get('get_blood_group')
        get_address = request.POST.get('get_address')

        if Add_patient.objects.filter(patient_phone = get_phone).exists(): # CHECK FOR THE SAME CARD NUMBER
            messages.error(request, 'Phone Number already exists!!!, Please Enter new Phone Number')
            return redirect("/dashboard/patient")
        else:
            submit_add_patient = Add_patient.objects.create(patient_name = get_fullName, patient_no = get_patient_no, patient_phone = get_phone, patient_blood_group = get_blood_group, patient_dob = get_dob, patient_gender = get_gender, patient_address = get_address)
            submit_add_patient.save()
            messages.success(request, get_fullName + " have been registered as a PATIENT")
            return redirect('/dashboard/patient')
    else:
        patient_no = random.randint(10, 1000000000)
        get_patient = Add_patient.objects.all()

        user_identity = request.user
        user_identity_email = user_identity.email
        get_user_info = Hospital_reg.objects.get(email=user_identity_email)
        all = {'get_user_info':get_user_info, 'patient_no':patient_no, 'get_patient':get_patient}
        return render(request, 'receptionist/patient.html', all)
    
def view_patient(request, id):
    get_patients_id = Add_patient.objects.get(id=id)
    get_patient = Add_patient.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_user_info = Hospital_reg.objects.get(email=user_identity_email)
    all = {'get_patient': get_patient, 'get_patients_id':get_patients_id, 'get_user_info':get_user_info}
    return render(request, 'receptionist/patient.html', all)
    
def confirm_delete_patient(request, id):
    get_patient_id = Add_patient.objects.get(id=id)
    get_patients = Add_patient.objects.all()
    get_patient = Add_patient.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_user_info = Hospital_reg.objects.get(email=user_identity_email)
    return render(request, 'receptionist/patient.html', {'get_patients': get_patients, 'get_patient': get_patient, 'get_patient_id':get_patient_id, 'get_user_info':get_user_info})

def delete_patient(request, id):
    get_patient = Add_patient.objects.get(id=id)
    get_patient.delete()
    return redirect("/dashboard/patient")

def appointment(request):
    get_appointment = Add_appointment.objects.all()
    count_appointment = Add_appointment.objects.all().count()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_user_info = Hospital_reg.objects.get(email=user_identity_email)
    all = {'get_user_info':get_user_info,'get_appointment':get_appointment, 'count_appointment':count_appointment}
    return render(request, 'receptionist/appointment.html', all)
  
def payroll(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_user_info = Hospital_reg.objects.get(email=user_identity_email)
    all = {'get_user_info':get_user_info}
    return render(request, 'receptionist/payroll.html', all)

def receptionist_pro(request):
    if request.method == 'POST':
        old_image = request.POST.get('old_image')
        user_id = request.POST.get('user_id')
        get_fullName = request.POST.get('get_fullName')
        get_email = request.POST.get('get_email')
        get_phone = request.POST.get('get_phone')
        get_password = request.POST.get('get_password')
        get_newpassword = request.POST.get('get_newpassword')

        if 'fileToUpload' in request.FILES:
            passport = request.FILES['fileToUpload'] # This is for new image
        else:
            passport = old_image.replace('/media/', '') # Maintain the old image

        user_info = Hospital_reg.objects.get(user_id=user_id)  
        user_info.fullName = get_fullName
        user_info.email = get_email
        user_info.phone = get_phone
        user_info.profile_picture = passport
        user_info.save()
        messages.info(request, " Your profile has been updated successfully")

        
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_user_info = Hospital_reg.objects.get(email=user_identity_email)
        all = {'get_user_info':get_user_info}
        return render(request, 'receptionist/users-profile.html', all)

def receptionist_pro_change_pass(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        get_password = request.POST.get('get_password')
        get_newpassword = request.POST.get('get_newpassword')

        user_identity = User.objects.get(id=user_id)
        user_identity.password = get_password
        user_identity.password = make_password(get_newpassword)
        user_identity.save()
        messages.info(request, " Your Password has been change successfully")
        return redirect('/register/login/')

    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_user_info = Hospital_reg.objects.get(email=user_identity_email)
        all = {'get_user_info':get_user_info}
        return render(request, 'receptionist/users-profile.html', all)

# PATIENT VIEWS
def patient_signup(request):
    if request.method == 'POST':
        # Submit to Database
        get_fullName = request.POST.get('get_fullName')
        get_email = request.POST.get('get_email')
        get_phone = request.POST.get('get_phone')
        get_patient_no = request.POST.get('get_patient_no')
        get_username = request.POST.get('get_username')
        get_address = request.POST.get('get_address')
        get_gender = request.POST.get('get_gender')
        get_dob = request.POST.get('get_dob')
        get_blood_group = request.POST.get('get_blood_group')
        get_password = request.POST.get('get_password')

        if User.objects.filter(username=get_username).exists(): # CHECK FOR THE SAME USERNAME
            messages.warning(request, 'Username already exists!!!, Please alter')
            return redirect("/logout_dash/patient_register/")
        elif User.objects.filter(email=get_email).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Email already exists!!!, Please alter')
            return redirect("/logout_dash/patient_register/")
        elif Patient_signup.objects.filter(patient_no=get_patient_no).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Patient Number already exists!!!, Please alter')
            return redirect("/logout_dash/patient_register/")
        elif Patient_signup.objects.filter(patient_phone=get_phone).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Patient Phone Number already exists!!!, Please alter')
            return redirect("/logout_dash/patient_register/")
        else: # ELSE SUBMIT TO DATABASE
            if 'fileToUpload' in request.FILES:
                passport = request.FILES['fileToUpload']
            else:
                passport = 'abc.jpg'  
            submit_patient_info = User.objects.create_user(password = get_password, username = get_username, first_name = get_fullName, email = get_email)
            mydict = {'get_fullName':get_fullName}
            submit_patient_info.save()
            # name	email	gender	phone	dob	student_class	
            submit_others = Patient_signup.objects.create(user=submit_patient_info, patient_name = get_fullName, patient_no = get_patient_no, patient_email = get_email, patient_phone = get_phone, patient_address = get_address, patient_gender = get_gender, patient_dob = get_dob, patient_blood_group = get_blood_group, profile_picture = passport)
            submit_others.save()
            
            html_template = 'patient/email.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Welcome To King Care Hospital'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [get_email]
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            messages.success(request, get_fullName + " have successfully registered")
            return redirect('/patient_register/patient_login/')
    else:
        patient_no = random.randint(10, 1000000000)
        all = {'patient_no':patient_no}
        return render(request, 'patient/patient-register.html', all)

# GETTING PATIENT INFO FOR PATIENT REGISTRATION
def get_patient_name(request):
    if request.method == 'GET':
        patient_no = request.GET['get_patient_no']
        get_patient_no_id = Add_patient.objects.get(patient_no=patient_no)
        patient_name = get_patient_no_id.patient_name
        return HttpResponse(patient_name)

def get_patient_phone(request):
    if request.method == 'GET':
        patient_no = request.GET['get_patient_no']
        get_patient_no_id = Add_patient.objects.get(patient_no=patient_no)
        patient_phone = get_patient_no_id.patient_phone
        return HttpResponse(patient_phone)
    
def get_patient_blood_group(request):
    if request.method == 'GET':
        patient_no = request.GET['get_patient_no']
        get_patient_no_id = Add_patient.objects.get(patient_no=patient_no)
        patient_blood_group = get_patient_no_id.patient_blood_group
        return HttpResponse(patient_blood_group)
    
def get_patient_dob(request):
    if request.method == 'GET':
        patient_no = request.GET['get_patient_no']
        get_patient_no_id = Add_patient.objects.get(patient_no=patient_no)
        patient_dob = get_patient_no_id.patient_dob
        return HttpResponse(patient_dob)
    
def get_patient_gender(request):
    if request.method == 'GET':
        patient_no = request.GET['get_patient_no']
        get_patient_no_id = Add_patient.objects.get(patient_no=patient_no)
        patient_gender = get_patient_no_id.patient_gender
        return HttpResponse(patient_gender)
    
def get_patient_addresses(request):
    if request.method == 'GET':
        patient_no = request.GET['get_patient_no']
        get_patient_no_id = Add_patient.objects.get(patient_no=patient_no)
        patient_address = get_patient_no_id.patient_address
        return HttpResponse(patient_address)
    
def patient_login(request):
    if request.method == 'POST':
        get_username = request.POST.get('get_username')
        get_password = request.POST.get('get_password')

        user = auth.authenticate(username=get_username, password=get_password)
        if user is not None: # if the user login details is valid then.....
            auth.login(request, user)
            messages.success(request, "Login Successful")
            return redirect('/patient_dash/')
        else:
            messages.error(request, "Your login details is wrong")
            return redirect('/patient_register/patient_login/')
    else:
        return render(request, 'patient/patient-login.html')
    
def patient_dashboard(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_patient_info = Patient_signup.objects.get(patient_email=user_identity_email)
    all = {'get_patient_info':get_patient_info}

    return render(request, 'patient/patient_dash.html', all)

def patient_appointment(request):
    get_appointment = Doctor_appointment.objects.all()
    count_appointment = Doctor_appointment.objects.all().count()
    get_doctor = Doctor_signup.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_patient_info = Patient_signup.objects.get(patient_email=user_identity_email)
    get_patient_no = get_patient_info.patient_no
    # get_patient_no = patient_data.patient_no
    get_patient_nos = Doctor_appointment.objects.filter(patient_no=get_patient_no)
    all = {'get_patient_info':get_patient_info, 'get_patient_no':get_patient_no, 'get_patient_nos':get_patient_nos, 'get_doctor':get_doctor, 'count_appointment':count_appointment, 'get_appointment':get_appointment}
    return render(request, 'patient/appointment.html', all)

def patient_prescription(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_patient_info = Patient_signup.objects.get(patient_email=user_identity_email)
    all = {'get_patient_info':get_patient_info}
    return render(request, 'patient/prescription.html', all)

def patient_admit_history(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_patient_info = Patient_signup.objects.get(patient_email=user_identity_email)
    all = {'get_patient_info':get_patient_info}
    return render(request, 'patient/admit_history.html', all)

def patient_operation_history(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_patient_info = Patient_signup.objects.get(patient_email=user_identity_email)
    all = {'get_patient_info':get_patient_info}
    return render(request, 'patient/operation_history.html', all)

def patient_invoice(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_patient_info = Patient_signup.objects.get(patient_email=user_identity_email)
    all = {'get_patient_info':get_patient_info}
    return render(request, 'patient/patient_invoice.html', all)

def patient_profile(request):
    if request.method == 'POST':
        old_image = request.POST.get('old_image')
        user_id = request.POST.get('user_id')
        get_fullName = request.POST.get('get_fullName')
        get_email = request.POST.get('get_email')
        get_phone = request.POST.get('get_phone')
        get_password = request.POST.get('get_password')

        if User.objects.filter(email=get_email).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Email already exists!!!, Please alter')
            return redirect("/patient_dash/patient_profile/")
        else:
            if 'fileToUpload' in request.FILES:
                passport = request.FILES['fileToUpload'] # This is for new image
            else:
                passport = old_image.replace('/media/', '') # Maintain the old image

            user_identity = User.objects.get(id=user_id)
            user_identity.first_name = get_fullName
            user_identity.email = get_email 
            user_identity.save()

            user_info = Patient_signup.objects.get(user_id=user_id)  
            user_info.patient_name = get_fullName
            user_info.patient_email = get_email
            user_info.patient_phone = get_phone
            user_info.profile_picture = passport
            user_info.save()
            messages.info(request, " Your profile has been updated successfully")
            return redirect("/patient_dash/profile/")
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_patient_info = Patient_signup.objects.get(patient_email=user_identity_email)
        all = {'get_patient_info':get_patient_info}
        return render(request, 'patient/patient-profile.html', all)

def patient_other_info(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        get_address = request.POST.get('get_address')
        get_gender = request.POST.get('get_gender')
        get_dob = request.POST.get('get_dob')
        get_blood_group = request.POST.get('get_blood_group')

        user_info = Patient_signup.objects.get(user_id=user_id)  
        user_info.patient_address = get_address
        user_info.patient_gender = get_gender
        user_info.patient_dob = get_dob 
        user_info.patient_blood_group = get_blood_group 
        user_info.save()
        messages.info(request, " Your profile has been updated successfully")
        return redirect("/patient_dash/profile/")
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_patient_info = Patient_signup.objects.get(patient_email=user_identity_email)
        all = {'get_patient_info':get_patient_info}
        return render(request, 'patient/patient-profile.html', all)

def patient_change_pass(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        get_password = request.POST.get('get_password')
        get_newpassword = request.POST.get('get_newpassword')

        user_identity = User.objects.get(id=user_id)
        user_identity.password = get_password
        user_identity.password = make_password(get_newpassword)
        user_identity.save()
        messages.info(request, " Your Password has been change successfully")
        return redirect('/patient_register/patient_login/')
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_patient_info = Patient_signup.objects.get(patient_email=user_identity_email)
        all = {'get_patient_info':get_patient_info}
        return render(request, 'patient/patient-profile.html', all)

# DOCTOR VIEWS
def doc_signup(request):
    if request.method == 'POST':
        # Submit to Database
        get_doctor_fullName = request.POST.get('get_doctor_fullName')
        get_doctor_email = request.POST.get('get_doctor_email')
        get_doctor_phone = request.POST.get('get_doctor_phone')
        get_doctor_username = request.POST.get('get_doctor_username')
        get_doctor_gender = request.POST.get('get_doctor_gender')
        get_doctor_password = request.POST.get('get_doctor_password')

        if User.objects.filter(email=get_doctor_email).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Email already exists!!!, Please alter')
            return redirect("/logout_dash/doc_signup/")
        elif User.objects.filter(username=get_doctor_username).exists(): # CHECK FOR THE SAME USERNAME
            messages.warning(request, 'Username already exists!!!, Please alter')
            return redirect("/logout_dash/doc_signup/")
        else: # ELSE SUBMIT TO DATABASE
            if 'fileToUpload' in request.FILES:
                passport = request.FILES['fileToUpload']
            else:
                passport = 'abc.jpg'  

            # Create user with pending status
            submit_user = User.objects.create_user(password=get_doctor_password, username=get_doctor_username, first_name=get_doctor_fullName, email=get_doctor_email)
            submit_user.save()
            
            # Set user as pending
            submit_to_pending = Doctor_signup.objects.create(user=submit_user, doctor_fullName=get_doctor_fullName, doctor_email=get_doctor_email, doctor_gender=get_doctor_gender, doctor_phone=get_doctor_phone, profile_picture=passport, status='Pending')
            submit_to_pending.save()
            
            messages.success(request, get_doctor_fullName + " have successfully registered. Your account is pending approval.")
            return redirect('/doc_signup/doc_login/')
    else:
        return render(request, 'doctor/doc_signup.html')
    
def doc_login(request):
    if request.method == 'POST':
        get_doctor_username = request.POST.get('get_doctor_username')
        get_doctor_password = request.POST.get('get_doctor_password')

        user = auth.authenticate(username=get_doctor_username, password=get_doctor_password)
        if user is not None: # if the user login details is valid then.....
            doctor_signup = Doctor_signup.objects.get(user=user)
            if doctor_signup.status == 'Pending':
                messages.error(request, "Your account is still pending approval.")
                return redirect('/doc_signup/doc_login/')
            else:
                auth.login(request, user)
                messages.success(request, "Login Successful")
                return redirect('/doctor_dash/')
        else:
            messages.error(request, "Your login details are wrong")
            return redirect('/doc_signup/doc_login/')
    else:
        return render(request, 'doctor/doc_login.html')
    
def doctor_dash(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    count_appointment = Doctor_appointment.objects.all().count()
    count_patient = Add_patient.objects.all().count()
    count_registered_patient = Patient_signup.objects.all().count()
    all = {'get_doctor_info':get_doctor_info, 'count_patient':count_patient, 'count_appointment':count_appointment, 'count_registered_patient':count_registered_patient}
    return render(request, 'doctor/doctor_dash.html', all)

def doctor_appointment(request):
    if request.method == 'POST':
        get_date = request.POST.get('get_date')
        get_time = request.POST.get('get_time')
        get_doctor_name = request.POST.get('get_doctor_name')
        get_patient_name = request.POST.get('get_patient_name')
        get_patient_no = request.POST.get('get_patient_no')

        submit_appointment = Doctor_appointment.objects.create(appointment_date = get_date, appointment_time = get_time, doctor_name = get_doctor_name, patient_name = get_patient_name, patient_no = get_patient_no)
        submit_appointment.save()
        messages.success(request, get_patient_name + " appointment is been added")
        return redirect('/doctor_dash/appointment')
    else:
        get_appointment = Doctor_appointment.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
        get_patient = Patient_signup.objects.all()
        all = {'get_doctor_info':get_doctor_info, 'get_appointment':get_appointment, 'get_patient':get_patient}
        return render(request, 'doctor/appointment.html', all)
    
def get_patient_no(request):
    if request.method == 'GET':
        patient_name = request.GET['get_patient_name']
        get_patient_name_id = Add_patient.objects.get(patient_name=patient_name)
        patient_no = get_patient_name_id.patient_no
        return HttpResponse(patient_no)
    
def doctor_edit_appointment(request, id):
    if request.method == 'POST':
        get_date = request.POST.get('get_date')
        get_time = request.POST.get('get_time')
        get_doctor_name = request.POST.get('get_doctor_name')
        get_patient_name = request.POST.get('get_patient_name')

        user_identity = Doctor_appointment.objects.get(id=id)
        user_identity.appointment_date = get_date
        user_identity.appointment_time = get_time
        user_identity.doctor_name = get_doctor_name
        user_identity.patient_name = get_patient_name
        user_identity.save()
        messages.info(request, " You have successfully update " + get_patient_name + " appointment")
        return redirect('/doctor_dash/appointment/')
    else:
        get_appointment_id = Doctor_appointment.objects.get(id=id)
        get_appointment = Doctor_appointment.objects.all()
        get_appointment_details = Doctor_appointment.objects.all()
        return render(request, 'doctor/appointment.html', { 'get_appointment': get_appointment, 'get_appointment_details': get_appointment_details, 'get_appointment_id':get_appointment_id})
    
def doctor_confirm_delete_appointment(request, id):
    get_appointments_id = Doctor_appointment.objects.get(id=id)
    get_appointments = Doctor_appointment.objects.all()
    
    get_appointment = Doctor_appointment.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    return render(request, 'doctor/appointment.html', {'get_doctor_info':get_doctor_info, 'get_appointments': get_appointments, 'get_appointment': get_appointment, 'get_appointments_id':get_appointments_id})

def doctor_delete_appointment(request, id):
    get_appointment = Doctor_appointment.objects.get(id=id)
    get_appointment.delete()
    messages.info(request, " You have successfully delete this appointment")
    return redirect("/doctor_dash/appointment/")

def doctor_prescription(request):
    if request.method == 'POST':
        get_doctor_name = request.POST.get('get_doctor_name')
        get_patient_name = request.POST.get('get_patient_name')
        get_patient_blood_group = request.POST.get('get_patient_blood_group')
        get_patient_gender = request.POST.get('get_patient_gender')
        get_case_history = request.POST.get('get_case_history')
        get_medication = request.POST.get('get_medication')
        get_note = request.POST.get('get_note')

        submit_prescription = Add_patient_prescription.objects.create(doctor_name = get_doctor_name, patient_name = get_patient_name, patient_blood_group = get_patient_blood_group, patient_gender = get_patient_gender, case_history = get_case_history, medication = get_medication, note = get_note)
        submit_prescription.save()
        messages.success(request, get_patient_name + " prescription is been added")
        return redirect('/doctor_dash/prescription')
    else:
        get_prescription = Add_patient_prescription.objects.all()
        get_patient = Add_patient.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
        all = {'get_doctor_info':get_doctor_info, 'get_prescription':get_prescription, 'get_patient':get_patient}
        return render(request, 'doctor/prescription.html', all)
    
def get_patient_blood_groups(request):
    if request.method == 'GET':
        patient_name = request.GET['get_patient_name']
        get_patient_name_id = Patient_signup.objects.get(patient_name=patient_name)
        patient_blood_group = get_patient_name_id.patient_blood_group
        return HttpResponse(patient_blood_group)
    
def get_patient_genders(request):
    if request.method == 'GET':
        patient_name = request.GET['get_patient_name']
        get_patient_name_id = Patient_signup.objects.get(patient_name=patient_name)
        patient_gender = get_patient_name_id.patient_gender
        return HttpResponse(patient_gender)
    
def doctor_edit_prescription(request, id):
    if request.method == 'POST':
        get_doctor_name = request.POST.get('get_doctor_name')
        get_patient_name = request.POST.get('get_patient_name')
        get_case_history = request.POST.get('get_case_history')
        get_medication = request.POST.get('get_medication')
        get_note = request.POST.get('get_note')

        user_identity = Add_patient_prescription.objects.get(id=id)
        user_identity.doctor_name = get_doctor_name
        user_identity.patient_name = get_patient_name
        user_identity.case_history = get_case_history
        user_identity.medication = get_medication
        user_identity.note = get_note
        user_identity.save()
        messages.info(request, " You have successfully update " + get_patient_name + " prescription")
        return redirect('/doctor_dash/prescription/')
    else:
        get_prescription_id = Add_patient_prescription.objects.get(id=id)
        get_prescription = Add_patient_prescription.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
        return render(request, 'doctor/prescription.html', {'get_doctor_info':get_doctor_info, 'get_prescription': get_prescription, 'get_prescription_id':get_prescription_id})
    
def doctor_view_prescription(request, id):
    gets_prescription_id = Add_patient_prescription.objects.get(id=id)
    get_prescription = Add_patient_prescription.objects.all()
    get_patient = Add_patient.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    return render(request, 'doctor/prescription.html', {'get_doctor_info':get_doctor_info, 'get_prescription': get_prescription, 'gets_prescription_id':gets_prescription_id})

def doctor_confirm_delete_prescription(request, id):
    get_prescriptions_id = Add_patient_prescription.objects.get(id=id)
    get_prescription = Add_patient_prescription.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    return render(request, 'doctor/prescription.html', {'get_doctor_info':get_doctor_info, 'get_prescription': get_prescription, 'get_prescriptions_id':get_prescriptions_id})

def doctor_delete_prescription(request, id):
    get_prescription = Add_patient_prescription.objects.get(id=id)
    get_prescription.delete()
    messages.info(request, " You have successfully delete this prescription")
    return redirect("/doctor_dash/prescription/")

def doctor_patient(request):
    get_patient = Patient_signup.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    all = {'get_doctor_info':get_doctor_info, 'get_patient':get_patient}
    return render(request, 'doctor/patient.html', all)

def doctor_view_patient_profile(request, id):
    get_patient_profile_id = Patient_signup.objects.get(id=id)
    get_patient_profile = Patient_signup.objects.all()
    get_patient = Patient_signup.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    all = {'get_patient':get_patient, 'get_doctor_info':get_doctor_info, 'get_patient_profile': get_patient_profile, 'get_patient_profile': get_patient_profile, 'get_patient_profile_id':get_patient_profile_id}
    return render(request, 'doctor/patient.html', all)

def doctor_bed_allotment(request):
    if request.method == 'POST':
        get_bed_no = request.POST.get('get_bed_no')
        get_patient_name = request.POST.get('get_patient_name')
        get_allotment_time = request.POST.get('get_allotment_time')
        get_discharge_time = request.POST.get('get_discharge_time')

        submit_bed_allotment = Add_bed_allotment.objects.create(bed_number = get_bed_no, patient_name = get_patient_name, discharge_time = get_discharge_time, allotment_time = get_allotment_time)
        submit_bed_allotment.save()
        messages.success(request, get_patient_name + " bed_allotment is been added")
        return redirect('/doctor_dash/bed_allotment')
    else:
        get_bed_allotment = Add_bed_allotment.objects.all()
        get_patient = Patient_signup.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
        all = {'get_doctor_info':get_doctor_info, 'get_bed_allotment':get_bed_allotment, 'get_patient':get_patient}
        return render(request, 'doctor/allotment.html', all)

def doctor_edit_bed_allotment(request, id):
    if request.method == 'POST':
        get_bed_no = request.POST.get('get_bed_no')
        get_patient_name = request.POST.get('get_patient_name')
        get_allotment_time = request.POST.get('get_allotment_time')
        get_discharge_time = request.POST.get('get_discharge_time')

        user_identity = Add_bed_allotment.objects.get(id=id)
        user_identity.bed_number = get_bed_no
        user_identity.patient_name = get_patient_name
        user_identity.allotment_time = get_allotment_time
        user_identity.discharge_time = get_discharge_time
        user_identity.save()
        messages.info(request, " You have successfully update " + get_patient_name + " Bed Allotment")
        return redirect('/doctor_dash/bed_allotment/')
    else:
        get_bed_allotment_id = Add_bed_allotment.objects.get(id=id)
        get_bed_allotment = Add_bed_allotment.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
        all = {'get_doctor_info':get_doctor_info, 'get_bed_allotment_id': get_bed_allotment_id, 'get_bed_allotment': get_bed_allotment}
        return render(request, 'doctor/allotment.html', all)
    
def doctor_confirm_delete_bed_allotment(request, id):
    get_bed_allotments_id = Add_bed_allotment.objects.get(id=id)
    get_bed_allotments = Add_bed_allotment.objects.all()
    get_bed_allotment_profiles = Add_patient.objects.all()
    return render(request, 'doctor/allotment.html', {'get_bed_allotments': get_bed_allotments, 'get_bed_allotment_profiles': get_bed_allotment_profiles, 'get_bed_allotments_id':get_bed_allotments_id})

def doctor_delete_bed_allotment(request, id):
    get_bed_allotment = Add_bed_allotment.objects.get(id=id)
    get_bed_allotment.delete()
    messages.info(request, " You have successfully delete this bed_allotment")
    return redirect("/doctor_dash/bed_allotment/")

def doctor_blood_bank(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    all = {'get_doctor_info':get_doctor_info}
    return render(request, 'doctor/blood_bank.html', all)

def doctor_report(request):
    if request.method == 'POST':
        get_report_type = request.POST.get('get_report_type')
        get_description = request.POST.get('get_description')
        get_report_date = request.POST.get('get_report_date')
        get_patient_name = request.POST.get('get_patient_name') 

        submit_operation_report = Add_report.objects.create(report_type = get_report_type, description = get_description, report_date = get_report_date, patient_name = get_patient_name)
        submit_operation_report.save()
        messages.success(request, get_patient_name + " operation_report is been added")
        return redirect('/doctor_dash/report')
    else:
        get_operation_report = Add_report.objects.filter(report_type='Operation')
        get_birth_report = Add_report.objects.filter(report_type='Birth')
        get_death_report = Add_report.objects.filter(report_type='Death')
        get_patient = Patient_signup.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
        all = {'get_doctor_info':get_doctor_info, 'get_operation_report':get_operation_report, 'get_patient':get_patient, 'get_birth_report':get_birth_report, 'get_death_report':get_death_report}
        return render(request, 'doctor/report.html', all)

def doctor_edit_report(request, id):
    if request.method == 'POST':
        get_report_type = request.POST.get('get_report_type')
        get_description = request.POST.get('get_description')
        get_report_date = request.POST.get('get_report_date')
        get_patient_name = request.POST.get('get_patient_name')
        get_report_file = request.POST.get('get_report_file')

        user_identity = Add_report.objects.get(id=id)
        user_identity.report_type = get_report_type
        user_identity.description = get_description
        user_identity.report_date = get_report_date
        user_identity.patient_name = get_patient_name
        user_identity.save()
        messages.info(request, " You have successfully update " + get_patient_name + " Report")
        return redirect('/doctor_dash/report/')
    else:
        get_report_id = Add_report.objects.get(id=id)
        get_report = Add_report.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
        all = {'get_doctor_info':get_doctor_info, 'get_report_id': get_report_id, 'get_report': get_report}
        return render(request, 'doctor/report.html', all)
    
def doctor_view_report(request, id):
    get_reports_id = Add_report.objects.get(id=id)
    get_report = Add_report.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    all = {'get_doctor_info': get_doctor_info, 'get_reports_id':get_reports_id, 'get_report': get_report}
    return render(request, 'doctor/report.html', all)

def doctor_confirm_delete_report(request, id):
    get_reports_ids = Add_report.objects.get(id=id)
    get_operation_report = Add_report.objects.filter(report_type='Operation')
    get_birth_report = Add_report.objects.filter(report_type='Birth')
    get_death_report = Add_report.objects.filter(report_type='Death')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    all = {'get_reports_ids':get_reports_ids, 'get_doctor_info':get_doctor_info, 'get_operation_report':get_operation_report, 'get_birth_report':get_birth_report, 'get_death_report':get_death_report}
    return render(request, 'doctor/report.html', all)

def doctor_delete_report(request, id):
    get_report = Add_report.objects.get(id=id)
    get_report.delete()
    messages.info(request, " You have successfully delete this report")
    return redirect("/doctor_dash/report/")

def doctor_payroll(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
    all = {'get_doctor_info':get_doctor_info}
    return render(request, 'doctor/payroll.html', all)

def doctor_pro(request):
    if request.method == 'POST':
        old_image = request.POST.get('old_image')
        user_id = request.POST.get('user_id')
        get_doctor_fullName = request.POST.get('get_doctor_fullName')
        get_doctor_email = request.POST.get('get_doctor_email')
        get_doctor_phone = request.POST.get('get_doctor_phone')

        if User.objects.filter(email=get_doctor_email).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Email already exists!!!, Please alter')
            return redirect("/doctor_dash/doctor_pro/")
        else:
            if 'fileToUpload' in request.FILES:
                passport = request.FILES['fileToUpload'] # This is for new image
            else:
                passport = old_image.replace('/media/', '') # Maintain the old image

            user_identity = User.objects.get(id=user_id)
            user_identity.first_name = get_doctor_fullName
            user_identity.email = get_doctor_email 
            user_identity.save()

            user_info = Doctor_signup.objects.get(user_id=user_id)  
            user_info.doctor_fullName = get_doctor_fullName
            user_info.doctor_email = get_doctor_email
            user_info.doctor_phone = get_doctor_phone
            user_info.profile_picture = passport
            user_info.save()
            messages.info(request, " Your profile has been updated successfully")
            return redirect("/doctor_dash/doctor_pro/")
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
        all = {'get_doctor_info':get_doctor_info}
        return render(request, 'doctor/doctor-profile.html', all)

def doctor_pro_change_pass(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        get_password = request.POST.get('get_password')
        get_newpassword = request.POST.get('get_newpassword')

        user_identity = User.objects.get(id=user_id)
        user_identity.password = get_password
        user_identity.password = make_password(get_newpassword)
        user_identity.save()
        messages.info(request, " Your Password has been change successfully")
        return redirect('/doc_signup/doc_login/')
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_doctor_info = Doctor_signup.objects.get(doctor_email=user_identity_email)
        all = {'get_doctor_info':get_doctor_info}
        return render(request, 'doctor/doctor-profile.html', all)

# PHARMACY PAGE
def pharmacy_signup(request):
    if request.method == 'POST':
        # Submit to Database
        get_name = request.POST.get('get_name')
        get_username = request.POST.get('get_username')
        get_email = request.POST.get('get_email')
        get_phone = request.POST.get('get_phone')
        get_gender = request.POST.get('get_gender')
        get_password = request.POST.get('get_password')

        if User.objects.filter(email=get_email).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Email already exists!!!, Please alter')
            return redirect("/logout_dash/pharmacy_signup/")
        elif User.objects.filter(username=get_username).exists(): # CHECK FOR THE SAME USERNAME
            messages.warning(request, 'Username already exists!!!, Please alter')
            return redirect("/logout_dash/pharmacy_signup/")
        else: # ELSE SUBMIT TO DATABASE
            if 'fileToUpload' in request.FILES:
                passport = request.FILES['fileToUpload']
            else:
                passport = 'abc.jpg'  
            submit_user = User.objects.create_user(password = get_password, username = get_username, first_name = get_name, email = get_email)
            submit_user.save()
            # name	email	gender	phone	dob	student_class	
            submit_others = Pharmacy_signup.objects.create(user=submit_user, pharmacy_name = get_name, pharmacy_username = get_username, pharmacy_email = get_email, pharmacy_phone = get_phone, pharmacy_gender = get_gender, profile_picture = passport, status='Pending')
            submit_others.save()
            messages.success(request, get_name + " have successfully registered. Your account is pending approval.")
            return redirect('/pharmacy_signup/pharmacy_login/')
    else:
            return render(request, 'pharmacy/pharmacy-register.html')

def pharmacy_login(request):
    if request.method == 'POST':
        get_username = request.POST.get('get_username')
        get_password = request.POST.get('get_password')

        user = auth.authenticate(username=get_username, password=get_password)
        if user is not None: # if the user login details is valid then.....
            pharmacy_signup = Pharmacy_signup.objects.get(user=user)
            if pharmacy_signup.status == 'Pending':
                messages.error(request, "Your account is still pending approval.")
                return redirect('/pharmacy_signup/pharmacy_login/')
            else:
                auth.login(request, user)
                messages.success(request, "Login Successful")
                return redirect('/pharmacy_dash/')
        else:
            messages.error(request, "Your login details is wrong")
            return redirect('/pharmacy_signup/pharmacy_login/')
    else:
        return render(request, 'pharmacy/pharmacy-login.html')

def pharmacy_dash(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)

    all = {'get_pharmacy_info':get_pharmacy_info}
    return render(request, 'pharmacy/pharmacy_dash.html', all)

def pharmacy_medicine_category(request):
    if request.method == 'POST':
        get_medicine_category = request.POST.get('get_medicine_category')
        get_description = request.POST.get('get_description')

        if Add_medicine_category.objects.filter(medicine_category = get_medicine_category).exists(): # CHECK FOR THE SAME MEDICINE CATEGORY
            messages.error(request, 'Medicine Category already exists!!!, Please Enter new Medicine Category')
            return redirect("/pharmacy_dash/medicine_category/")
        else:
            submit_add_medicine_category = Add_medicine_category.objects.create(medicine_category = get_medicine_category, medicine_category_description = get_description)
            submit_add_medicine_category.save()
            messages.success(request, get_medicine_category + " have been registered as a medicine_category")
            return redirect('/pharmacy_dash/medicine_category/')
    else:
        get_medicine_category = Add_medicine_category.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
        all = {'get_pharmacy_info':get_pharmacy_info, 'get_medicine_category':get_medicine_category}
        return render(request, 'pharmacy/medicine_category.html', all)
    
def pharmacy_edit_medicine_category(request, id):
    if request.method == 'POST':
        get_medicine_category = request.POST.get('get_medicine_category')
        get_description = request.POST.get('get_description')

        user_identity = Add_medicine_category.objects.get(id=id)
        user_identity.medicine_category = get_medicine_category
        user_identity.medicine_category_description = get_description
        user_identity.save()
        messages.info(request, " Medicine Category have successfully Updated")
        return redirect('/pharmacy_dash/medicine_category/')
    else:
        get_medicine_category_id = Add_medicine_category.objects.get(id=id)
        get_medicine_category = Add_medicine_category.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
        all = {'get_pharmacy_info':get_pharmacy_info, 'get_medicine_category_id': get_medicine_category_id, 'get_medicine_category': get_medicine_category}
        return render(request, 'pharmacy/medicine_category.html', all)
    
def pharmacy_confirm_delete_medicine_category(request, id):
    get_medicine_categorys_id = Add_medicine_category.objects.get(id=id)
    get_medicine_category = Add_medicine_category.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
    all = {'get_medicine_category': get_medicine_category, 'get_medicine_categorys_id':get_medicine_categorys_id, 'get_pharmacy_info':get_pharmacy_info}
    return render(request, 'pharmacy/medicine_category.html', all)

def pharmacy_delete_medicine_category(request, id):
    get_medicine_category = Add_medicine_category.objects.get(id=id)
    get_medicine_category.delete()
    messages.info(request, " You have successfully delete this Medicine Category")
    return redirect("/pharmacy_dash/medicine_category/")

def pharmacy_manage_medicine(request):
    if request.method == 'POST':
        get_medicine_name = request.POST.get('get_medicine_name')
        get_medicine_category = request.POST.get('get_medicine_category')
        get_description = request.POST.get('get_description')
        get_medicine_price = request.POST.get('get_medicine_price')
        get_total_quantity = request.POST.get('get_total_quantity')
        get_manufacture_company = request.POST.get('get_manufacture_company')

        if Add_medicine.objects.filter(medicine_name = get_medicine_name).exists(): # CHECK FOR THE SAME MEDICINE NAME
            messages.error(request, 'Medicine Name already exists!!!, Please Enter new Medicine Name')
            return redirect("/pharmacy_dash/manage_medicine/")
        else:
            submit_add_medicine = Add_medicine.objects.create(medicine_name = get_medicine_name, medicine_category = get_medicine_category, medicine_category_description = get_description, medicine_price = get_medicine_price, total_quantity = get_total_quantity, manufacture_company = get_manufacture_company)
            submit_add_medicine.save()
            messages.success(request, get_medicine_name + " have been registered as a medicine name")
            return redirect('/pharmacy_dash/manage_medicine/')
    else:
        get_medicine_category = Add_medicine_category.objects.all()
        get_manage_medicine = Add_medicine.objects.all()
        get_sold_medicine = Add_sales_medicine.objects.all().count()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
        all = {'get_pharmacy_info':get_pharmacy_info, 'get_medicine_category':get_medicine_category, 'get_manage_medicine':get_manage_medicine, 'get_sold_medicine':get_sold_medicine}
        return render(request, 'pharmacy/manage_medicine.html', all)
    
def pharmacy_confirm_delete_product_medicine(request, id):
    get_product_medicine_id = Add_medicine.objects.get(id=id)
    get_medicine = Add_medicine.objects.all()
    get_manage_medicine = Add_medicine.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
    all = {'get_medicine': get_medicine, 'get_manage_medicine':get_manage_medicine, 'get_product_medicine_id':get_product_medicine_id, 'get_pharmacy_info':get_pharmacy_info}
    return render(request, 'pharmacy/manage_medicine.html', all)

def pharmacy_delete_product_medicine(request, id):
    get_medicine = Add_medicine.objects.get(id=id)
    get_medicine.delete()
    messages.info(request, " You have successfully delete this Medicine")
    return redirect("/pharmacy_dash/manage_medicine/")
    
def get_info(request):
    if request.method == 'GET':
        medicine_category = request.GET['get_medicine_category']
        get_medicine_category_id = Add_medicine_category.objects.get(medicine_category=medicine_category)
        medicine_category_description = get_medicine_category_id.medicine_category_description
        return HttpResponse(medicine_category_description)
    
def pharmacy_medicine_sales(request):
    get_sales = Add_sales.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)

    all = {'get_pharmacy_info':get_pharmacy_info, 'get_sales':get_sales}
    return render(request, 'pharmacy/medicine_sales.html', all)

def pharmacy_add_medicine_sales(request):
    invoice_no = random.randint(10, 100000)
    get_manage_medicine = Add_medicine.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)

    all = {'get_pharmacy_info':get_pharmacy_info, 'get_manage_medicine':get_manage_medicine, 'invoice_no':invoice_no}
    return render(request, 'pharmacy/add_medicine_sales.html', all)

def add_to_cart(request):
    if request.method == 'POST':
        get_medicine_name = request.POST.get('get_medicine_name')
        get_quantity = int(request.POST.get('get_quantity'))
        get_invoice_no = request.POST.get('get_invoice_no')
        
        product = Add_medicine.objects.get(medicine_name=get_medicine_name)
        if product.total_quantity < get_quantity:
            messages.error(request, 'Insufficient quantity available.')
        else:
            get_price = product.medicine_price
            amount = get_quantity * get_price

            # Create a new item in the cart
            submit_add_to_cart = Add_to_cart.objects.create(
                product=get_medicine_name,
                quantity=get_quantity,
                price=get_price,
                invoice_no=get_invoice_no,
                amount=amount
            )
            submit_add_to_cart.save()

            messages.success(request, f"{get_quantity} units of {get_medicine_name} added to cart successfully.")

    # Get necessary data for rendering the page
    get_manage_medicine = Add_medicine.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
    filter_invoice_no = Add_to_cart.objects.filter(invoice_no=get_invoice_no)
    sum_total = Add_to_cart.objects.filter(invoice_no=get_invoice_no).aggregate(total_amount=Sum('amount'))
    sales_amount = sum_total.get('total_amount', 0)

    all_data = {
        'get_pharmacy_info': get_pharmacy_info,
        'get_manage_medicine': get_manage_medicine,
        'invoice_no': get_invoice_no,
        'filter_invoice_no': filter_invoice_no,
        'sales_amount': sales_amount
    }
    return render(request, 'pharmacy/add_medicine_sales.html', all_data)

def add_sales(request):
    if request.method == 'POST':
        get_customer_name = request.POST.get('get_customer_name')
        get_customer_phone = request.POST.get('get_customer_phone')
        get_amount_paid = request.POST.get('get_amount_paid')
        get_invoice_no = request.POST.get('get_invoice_no')

        # Create a new entry in Add_sales model
        submit_add_sales = Add_sales.objects.create(
            customer_name=get_customer_name,
            customer_phone=get_customer_phone,
            amount_paid=get_amount_paid,
            invoice_no=get_invoice_no
        )
        submit_add_sales.save()

        # Update the total quantity sold in Add_medicine model
        cart_items = Add_to_cart.objects.filter(invoice_no=get_invoice_no)
        for item in cart_items:
            Add_medicine.objects.filter(medicine_name=item.product).update(total_quantity=F('total_quantity') - item.quantity)

        return redirect("/medicine_sales/add_medicine_sales/")

# def edit_sales(request, id):
#     get_customer_cart = Add_sales.objects.get(id = id)
#     inv = get_customer_cart.invoice_no
#     name = get_customer_cart.customer_name
#     phone = get_customer_cart.customer_phone
    

#     get_manage_medicine = Add_medicine.objects.all()

#     filter_invoice_no = Add_to_cart.objects.filter(invoice_no = inv)

#     sum_total = Add_to_cart.objects.filter(invoice_no = inv).aggregate(total_amount = Sum('amount'))
#     sales_amount = sum_total['total_amount']

#     user_identity = request.user
#     user_identity_email = user_identity.email
#     get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)

#     all = {'get_pharmacy_info':get_pharmacy_info, 'get_customer_cart':get_customer_cart, 'get_manage_medicine':get_manage_medicine, 'invoice_no':inv, 'name':name, 'phone':phone, 'filter_invoice_no':filter_invoice_no, 'sales_amount':sales_amount}
#     return render(request, 'pharmacy/add_medicine_sales.html', all)
def edit_sales(request, id):
    if request.method == 'POST':
        # Get the sale object to be edited
        get_customer_cart = Add_sales.objects.get(id=id)
        
        # Update the sale object with the new data
        get_customer_cart.customer_name = request.POST.get('get_customer_name')
        get_customer_cart.customer_phone = request.POST.get('get_customer_phone')
        get_customer_cart.save()

        # Redirect to the page showing the updated sale
        return redirect('/pharmacy_dash/medicine_sales/')  # Replace '/path_to_sale_detail_page/' with the appropriate URL
        
    else:
        # Handle GET request
        get_customer_cart = Add_sales.objects.get(id=id)
        inv = get_customer_cart.invoice_no
        name = get_customer_cart.customer_name
        phone = get_customer_cart.customer_phone
        
        get_manage_medicine = Add_medicine.objects.all()
        filter_invoice_no = Add_to_cart.objects.filter(invoice_no=inv)
        sum_total = Add_to_cart.objects.filter(invoice_no=inv).aggregate(total_amount=Sum('amount'))
        sales_amount = sum_total['total_amount']
        
        user_identity = request.user
        user_identity_email = user_identity.email
        get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
        
        context = {
            'get_pharmacy_info': get_pharmacy_info,
            'get_customer_cart': get_customer_cart,
            'get_manage_medicine': get_manage_medicine,
            'invoice_no': inv,
            'name': name,
            'phone': phone,
            'filter_invoice_no': filter_invoice_no,
            'sales_amount': sales_amount
        }
        
        return render(request, 'pharmacy/add_medicine_sales.html', context)
    
def pharmacy_confirm_delete_sale(request, id):
    get_sale_id = Add_sales.objects.get(id=id)
    get_sales = Add_sales.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
    all = {'get_pharmacy_info':get_pharmacy_info, 'get_sale_id':get_sale_id, 'get_sales':get_sales}
    return render(request, 'pharmacy/medicine_sales.html', all)

def pharmacy_delete_sale(request, id):
    get_sale = Add_sales.objects.get(id=id)
    get_sale.delete()
    messages.info(request, " You have successfully delete Sale")
    return render(request, 'pharmacy/add_medicine_sales.html')

def pharmacy_confirm_delete_medicine(request, id):
    get_medicine_id = Add_to_cart.objects.get(id=id)
    get_invoice_no = get_medicine_id.invoice_no
    get_medicine = Add_to_cart.objects.all()
    filter_invoice_no = Add_to_cart.objects.filter(invoice_no = get_invoice_no)
    get_manage_medicine = Add_medicine.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
    all = {'get_medicine_id': get_medicine_id, 'get_manage_medicine':get_manage_medicine, 'get_medicine':get_medicine, 'filter_invoice_no':filter_invoice_no, 'get_pharmacy_info':get_pharmacy_info}
    return render(request, 'pharmacy/add_medicine_sales.html', all)

def pharmacy_delete_medicine(request, id):
    get_medicine = Add_to_cart.objects.get(id=id)
    get_invoice_no = get_medicine.invoice_no
    get_medicine.delete()
    messages.info(request, " You have successfully delete Product From Cart")
    filter_invoice_no = Add_to_cart.objects.filter(invoice_no = get_invoice_no)
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
    filter_invoice_no = Add_to_cart.objects.filter(invoice_no = get_invoice_no)
    sum_total = Add_to_cart.objects.all().aggregate(total_amount = Sum('amount'))
    sales_amount = sum_total['total_amount']

    all = {'get_pharmacy_info':get_pharmacy_info, 'invoice_no':get_invoice_no, 'filter_invoice_no':filter_invoice_no, 'sales_amount':sales_amount}
    return render(request, 'pharmacy/add_medicine_sales.html', all)
    # return redirect("/medicine_sales/add_medicine_sales/")

def get_price(request):
    if request.method == 'GET':
        medicine_name = request.GET['get_medicine_name']
        get_medicine_name_id = Add_medicine.objects.get(medicine_name=medicine_name)
        medicine_price = get_medicine_name_id.medicine_price
        return HttpResponse(medicine_price)
    
def pharmacy_payroll(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
    all = {'get_pharmacy_info':get_pharmacy_info}
    return render(request, 'pharmacy/payroll.html', all)

def pharmacy_pro(request):
    if request.method == 'POST':
        old_image = request.POST.get('old_image')
        user_id = request.POST.get('user_id')
        get_name = request.POST.get('get_name')
        get_email = request.POST.get('get_email')
        get_phone = request.POST.get('get_phone')
        get_password = request.POST.get('get_password')
        get_newpassword = request.POST.get('get_newpassword')
        
        if 'fileToUpload' in request.FILES:
            passport = request.FILES['fileToUpload'] # This is for new image
        else:
            passport = old_image.replace('/media/', '') # Maintain the old image

        user_identity = User.objects.get(id=user_id)
        user_identity.first_name = get_name
        user_identity.email = get_email 
        user_identity.save()

        user_info = Pharmacy_signup.objects.get(user_id=user_id)  
        user_info.pharmacy_name = get_name
        user_info.pharmacy_email = get_email
        user_info.pharmacy_phone = get_phone
        user_info.profile_picture = passport
        user_info.save()
        messages.info(request, " Your profile has been updated successfully")
        return redirect("/pharmacy_dash/pharmacy_pro/")
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
        all = {'get_pharmacy_info':get_pharmacy_info}
        return render(request, 'pharmacy/pharmacy-profile.html', all)

def pharmacy_pro_change_pass(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        get_password = request.POST.get('get_password')
        get_newpassword = request.POST.get('get_newpassword')

        user_identity = User.objects.get(id=user_id)
        user_identity.password = get_password
        user_identity.password = make_password(get_newpassword)
        user_identity.save()
        messages.info(request, " Your Password has been change successfully")
        return redirect('/pharmacy_signup/pharmacy_login/')
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_pharmacy_info = Pharmacy_signup.objects.get(pharmacy_email=user_identity_email)
        all = {'get_pharmacy_info':get_pharmacy_info}
        return render(request, 'pharmacy/pharmacy-profile.html', all)
    
# ACCOUNT
def acct_signup(request):
    if request.method == 'POST':
        # Submit to Database
        get_acct_name = request.POST.get('get_acct_name')
        get_acct_username = request.POST.get('get_acct_username')
        get_acct_email = request.POST.get('get_acct_email')
        get_acct_phone = request.POST.get('get_acct_phone')
        get_acct_gender = request.POST.get('get_acct_gender')
        get_acct_password = request.POST.get('get_acct_password')

        if User.objects.filter(email=get_acct_email).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Email already exists!!!, Please alter')
            return redirect("/logout_dash/acct_signup/")
        elif User.objects.filter(username=get_acct_username).exists(): # CHECK FOR THE SAME USERNAME
            messages.warning(request, 'Username already exists!!!, Please alter')
            return redirect("/logout_dash/acct_signup/")
        else: # ELSE SUBMIT TO DATABASE
            if 'fileToUpload' in request.FILES:
                passport = request.FILES['fileToUpload']
            else:
                passport = 'abc.jpg'  
            submit_user = User.objects.create_user(password = get_acct_password, username = get_acct_username, first_name = get_acct_name, email = get_acct_email)
            submit_user.save()
            # name	email	gender	phone	dob	student_class	
            submit_others = Acct_signup.objects.create(user=submit_user, acct_name = get_acct_name, acct_username = get_acct_username, acct_email = get_acct_email, acct_phone = get_acct_phone, acct_gender = get_acct_gender, profile_picture = passport, status='Pending')
            submit_others.save()
            messages.success(request, get_acct_name + " have successfully registered. Your account is pending approval.")
            return redirect('/acct_signup/acct_login/')
    else:
        return render(request, 'account/acct-register.html')
    
def acct_login(request):
    if request.method == 'POST':
        get_acct_username = request.POST.get('get_acct_username')
        get_acct_password = request.POST.get('get_acct_password')

        user = auth.authenticate(username=get_acct_username, password=get_acct_password)
        if user is not None: # if the user login details is valid then.....
            accountant_signup = Acct_signup.objects.get(user=user)
            if accountant_signup.status == 'Pending':
                messages.error(request, "Your account is still pending approval.")
                return redirect('/acct_signup/acct_login/')
            else:
                auth.login(request, user)
                messages.success(request, "Login Successful")
                return redirect('/acct_dash/')
        else:
            messages.error(request, "Your login details is wrong")
            return redirect('/acct_signup/acct_login/')
    else:
        return render(request, 'account/acct-login.html')

def acct_dash(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_acct_info = Acct_signup.objects.get(acct_email=user_identity_email)

    count_patient = Add_patient.objects.all().count()

    all = {'get_acct_info':get_acct_info, 'count_patient':count_patient}
    return render(request, 'account/acct_dash.html', all)
    
def acct_add_invoice(request):
    if request.method == 'POST':
        get_invoice_title = request.POST.get('get_invoice_title')
        get_invoice_number = request.POST.get('get_invoice_number')
        get_patient_name = request.POST.get('get_patient_name')
        get_patient_address = request.POST.get('get_patient_address')
        get_creation_date = request.POST.get('get_creation_date')
        get_due_date = request.POST.get('get_due_date')
        get_payment_status = request.POST.get('get_payment_status')
        get_invoice_entry = request.POST.get('get_invoice_entry')
        get_amount = request.POST.get('get_amount')

        if Add_invoice.objects.filter(invoice_title = get_invoice_title).exists(): # CHECK FOR THE SAME MEDICINE NAME
            messages.error(request, 'Medicine Name already exists!!!, Please Enter new Medicine Name')
            return redirect("/acct_dash/add_invoice/")
        else:
            submit_add_invoice = Add_invoice.objects.create(invoice_title = get_invoice_title, invoice_number = get_invoice_number, patient_name = get_patient_name, patient_address = get_patient_address, creation_date = get_creation_date, due_date = get_due_date, pay_status = get_payment_status, des_invoice = get_invoice_entry, amount = get_amount)
            submit_add_invoice.save()
            messages.success(request, get_invoice_title + " have been registered as a Invoice")
            return redirect('/acct_dash/add_invoice/')
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_acct_info = Acct_signup.objects.get(acct_email=user_identity_email)
        get_patient = Patient_signup.objects.all()
        all = {'get_acct_info':get_acct_info, 'get_patient':get_patient}
        return render(request, 'account/add_invoice.html', all)
    
def get_patient_address(request):
    if request.method == 'GET':
        patient_name = request.GET['get_patient_name']
        get_patient_name_id = Add_patient.objects.get(patient_name=patient_name)
        patient_address = get_patient_name_id.patient_address
        return HttpResponse(patient_address)
    
def acct_manage_invoice(request):
    get_manage_invoice = Add_invoice.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_acct_info = Acct_signup.objects.get(acct_email=user_identity_email)

    all = {'get_acct_info':get_acct_info, 'get_manage_invoice':get_manage_invoice}
    return render(request, 'account/manage_invoice.html', all)

def acct_edit_invoice(request, id):
    if request.method == 'POST':
        get_invoice_title = request.POST.get('get_invoice_title')
        get_invoice_number = request.POST.get('get_invoice_number')
        get_patient_name = request.POST.get('get_patient_name')
        get_patient_address = request.POST.get('get_patient_address')
        get_creation_date = request.POST.get('get_creation_date')
        get_due_date = request.POST.get('get_due_date')
        get_payment_status = request.POST.get('get_payment_status')
        get_invoice_entry = request.POST.get('get_invoice_entry')
        get_amount = request.POST.get('get_amount')

        user_identity = Add_invoice.objects.get(id=id)
        user_identity.invoice_title = get_invoice_title
        user_identity.invoice_number = get_invoice_number
        user_identity.patient_name = get_patient_name
        user_identity.patient_address = get_patient_address
        user_identity.creation_date = get_creation_date
        user_identity.due_date = get_due_date
        user_identity.pay_status = get_payment_status
        user_identity.des_invoice = get_invoice_entry
        user_identity.amount = get_amount
        user_identity.save()
        messages.info(request, " You have successfully update " + get_patient_name + " Invoice")
        return redirect('/acct_dash/manage_invoice/')
    else:
        get_manage_invoice = Add_invoice.objects.all()
        get_invoice_id = Add_invoice.objects.get(id=id)
        get_invoice = Add_invoice.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_acct_info = Acct_signup.objects.get(acct_email=user_identity_email)
        all = {'get_acct_info':get_acct_info, 'get_invoice_id': get_invoice_id, 'get_invoice':get_invoice, 'get_manage_invoice':get_manage_invoice}
        return render(request, 'account/manage_invoice.html', all)
    
def acct_view_invoice(request, id):
    get_invoices_id = Add_invoice.objects.get(id=id)
    get_manage_invoice = Add_invoice.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_acct_info = Acct_signup.objects.get(acct_email=user_identity_email)
    all = {'get_invoices_id': get_invoices_id, 'get_manage_invoice': get_manage_invoice, 'get_acct_info':get_acct_info}
    return render(request, 'account/manage_invoice.html', all)

def acct_confirm_delete_invoice(request, id):
    get_invoice_ids = Add_invoice.objects.get(id=id)
    get_manage_invoice = Add_invoice.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_acct_info = Acct_signup.objects.get(acct_email=user_identity_email)
    all = {'get_invoice_ids': get_invoice_ids, 'get_manage_invoice': get_manage_invoice, 'get_acct_info':get_acct_info}
    return render(request, 'account/manage_invoice.html', all)

def acct_delete_invoice(request, id):
    get_invoice_ids = Add_invoice.objects.get(id=id)
    get_invoice_ids.delete()
    return redirect("/acct_dash/manage_invoice/")

def acct_payroll(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_acct_info = Acct_signup.objects.get(acct_email=user_identity_email)

    all = {'get_acct_info':get_acct_info}
    return render(request, 'account/payroll.html', all)

def acct_pro(request):
    if request.method == 'POST':
        old_image = request.POST.get('old_image')
        user_id = request.POST.get('user_id')
        get_acct_name = request.POST.get('get_acct_name')
        get_acct_email = request.POST.get('get_acct_email')
        get_acct_phone = request.POST.get('get_acct_phone')
        get_acct_password = request.POST.get('get_acct_password')
        
        if 'fileToUpload' in request.FILES:
            passport = request.FILES['fileToUpload'] # This is for new image
        else:
            passport = old_image.replace('/media/', '') # Maintain the old image

        user_identity = User.objects.get(id=user_id)
        user_identity.first_name = get_acct_name
        user_identity.email = get_acct_email 
        user_identity.save()

        user_info = Acct_signup.objects.get(user_id=user_id)  
        user_info.acct_name = get_acct_name
        user_info.acct_email = get_acct_email
        user_info.acct_phone = get_acct_phone
        user_info.profile_picture = passport
        user_info.save()
        messages.info(request, " Your profile has been updated successfully")
        return redirect("/acct_dash/acct_pro/")
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_acct_info = Acct_signup.objects.get(acct_email=user_identity_email)
        all = {'get_acct_info':get_acct_info}
        return render(request, 'account/acct-profile.html', all)

def acct_pro_change_pass(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        get_acct_password = request.POST.get('get_acct_password')
        get_newpassword = request.POST.get('get_newpassword')

        user_identity = User.objects.get(id=user_id)
        user_identity.password = get_acct_password
        user_identity.password = make_password(get_newpassword)
        user_identity.save()
        messages.info(request, " Your Password has been change successfully")
        return redirect('/acct_signup/acct_login/')
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_acct_info = Acct_signup.objects.get(acct_email=user_identity_email)
        all = {'get_acct_info':get_acct_info}
        return render(request, 'account/acct-profile.html', all)

def laboratory_signup(request):
    if request.method == 'POST':
        # Submit to Database
        get_name = request.POST.get('get_name')
        get_username = request.POST.get('get_username')
        get_email = request.POST.get('get_email')
        get_gender = request.POST.get('get_gender')
        get_phone = request.POST.get('get_phone')
        get_password = request.POST.get('get_password')

        if User.objects.filter(email=get_email).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Email already exists!!!, Please alter')
            return redirect("/logout_dash_signup/")
        elif User.objects.filter(username=get_username).exists(): # CHECK FOR THE SAME USERNAME
            messages.warning(request, 'Username already exists!!!, Please alter')
            return redirect("/logout_dash/lab_signup/")
        else: # ELSE SUBMIT TO DATABASE
            if 'fileToUpload' in request.FILES:
                passport = request.FILES['fileToUpload']
            else:
                passport = 'abc.jpg'  
            submit_user = User.objects.create_user(password = get_password, username = get_username, first_name = get_name, email = get_email)
            submit_user.save()
            # name	email	gender	phone	dob	student_class	
            submit_others = Laboratory_signup.objects.create(user=submit_user, laboratory_name = get_name, laboratory_username = get_username, laboratory_email = get_email, laboratory_phone = get_phone, laboratory_gender = get_gender, profile_picture = passport, status='Pending')
            submit_others.save()
            messages.success(request, get_name + " have successfully registered. Your account is pending approval.")
            return redirect('/laboratory_signup/laboratory_login/')
    else:
        return render(request, 'laboratory/lab_signup.html')
    
def laboratory_login(request):
    if request.method == 'POST':
        get_username = request.POST.get('get_username')
        get_password = request.POST.get('get_password')

        user = auth.authenticate(username=get_username, password=get_password)
        if user is not None: # if the user login details is valid then.....
            laboratory_signup = Laboratory_signup.objects.get(user=user)
            if laboratory_signup.status == 'Pending':
                messages.error(request, "Your account is still pending approval.")
                return redirect('/laboratory_signup/laboratory_login/')
            else:
                auth.login(request, user)
                messages.success(request, "Login Successful")
                return redirect('/laboratory_dash/')
        else:
            messages.error(request, "Your login details is wrong")
            return redirect('/laboratory_signup/laboratory_login/')
    else:
        return render(request, 'laboratory/lab_login.html')

def laboratory_dash(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_lab_info = Laboratory_signup.objects.get(laboratory_email=user_identity_email)

    count_patient = Add_patient.objects.all().count()
    count_doctor = Doctor_signup.objects.all().count()

    all = {'get_lab_info':get_lab_info, 'count_patient':count_patient, 'count_doctor':count_doctor}
    return render(request, 'laboratory/lab_dash.html', all)

def laboratory_blood_bank(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_lab_info = Laboratory_signup.objects.get(laboratory_email=user_identity_email)
    all = {'get_lab_info':get_lab_info}
    return render(request, 'laboratory/blood_bank.html', all)

def laboratory_blood_donor(request):
    if request.method == 'POST':
        get_donor_name = request.POST.get('get_donor_name')
        get_address = request.POST.get('get_address')
        get_phone = request.POST.get('get_phone')
        get_gender = request.POST.get('get_gender')
        get_age = request.POST.get('get_age')
        get_blood_group = request.POST.get('get_blood_group')

        submit_blood_donor = Add_blood_donor.objects.create(donor_name = get_donor_name, donor_address = get_address, donor_phone = get_phone, donor_gender = get_gender, donor_age = get_age, donor_blood_group = get_blood_group)
        submit_blood_donor.save()
        messages.success(request, get_donor_name + " Blood Donor is been added")
        return redirect('/laboratory_dash/blood_donor/')
    else:
        get_donor = Add_blood_donor.objects.all()
        user_identity = request.user
        user_identity_email = user_identity.email
        get_lab_info = Laboratory_signup.objects.get(laboratory_email=user_identity_email)
        all = {'get_lab_info':get_lab_info, 'get_donor':get_donor}
        return render(request, 'laboratory/lab_blood_donor.html', all)

def laboratory_edit_blood_donor(request, id):
    if request.method == 'POST':
        get_donor_name = request.POST.get('get_donor_name')
        get_address = request.POST.get('get_address')
        get_phone = request.POST.get('get_phone')
        get_gender = request.POST.get('get_gender')
        get_age = request.POST.get('get_age')
        get_blood_group = request.POST.get('get_blood_group')

        user_identity = Add_blood_donor.objects.get(id=id)
        user_identity.donor_name = get_donor_name
        user_identity.donor_address = get_address
        user_identity.donor_phone = get_phone
        user_identity.donor_gender = get_gender
        user_identity.donor_age = get_age
        user_identity.donor_blood_group = get_blood_group
        user_identity.save()
        messages.info(request, " You have successfully update " + get_donor_name + " Blood Donor")
        return redirect('/laboratory_dash/blood_donor/')
    else:
        get_donor = Add_blood_donor.objects.all()
        get_donor_id = Add_blood_donor.objects.get(id=id)
        user_identity = request.user
        user_identity_email = user_identity.email
        get_lab_info = Laboratory_signup.objects.get(laboratory_email=user_identity_email)
        all = {'get_lab_info':get_lab_info, 'get_donor_id': get_donor_id, 'get_donor':get_donor}
        return render(request, 'laboratory/lab_blood_donor.html', all)
    
def laboratory_confirm_delete_donor(request, id):
    get_donors_id = Add_blood_donor.objects.get(id=id)
    get_donor = Add_blood_donor.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_lab_info = Laboratory_signup.objects.get(laboratory_email=user_identity_email)
    all = {'get_donor': get_donor, 'get_donors_id':get_donors_id, 'get_lab_info':get_lab_info}
    return render(request, 'laboratory/lab_blood_donor.html', all)

def laboratory_delete_donor(request, id):
    get_donor = Add_blood_donor.objects.get(id=id)
    get_donor.delete()
    return redirect("/laboratory_dash/blood_donor/")

def laboratory_payroll(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_lab_info = Laboratory_signup.objects.get(laboratory_email=user_identity_email)

    all = {'get_lab_info':get_lab_info}
    return render(request, 'laboratory/payroll.html', all)

def laboratory_pro(request):
    if request.method == 'POST':
        old_image = request.POST.get('old_image')
        user_id = request.POST.get('user_id')
        get_name = request.POST.get('get_name')
        get_email = request.POST.get('get_email')
        get_phone = request.POST.get('get_phone')
        get_password = request.POST.get('get_password')
        
        if 'fileToUpload' in request.FILES:
            passport = request.FILES['fileToUpload'] # This is for new image
        else:
            passport = old_image.replace('/media/', '') # Maintain the old image

        user_identity = User.objects.get(id=user_id)
        user_identity.first_name = get_name
        user_identity.email = get_email 
        user_identity.save()

        user_info = Laboratory_signup.objects.get(user_id=user_id)  
        user_info.laboratory_name = get_name
        user_info.laboratory_email = get_email
        user_info.laboratory_phone = get_phone
        user_info.profile_picture = passport
        user_info.save()
        messages.info(request, " Your profile has been updated successfully")
        return redirect("/laboratory_dash/laboratory_pro")
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_lab_info = Laboratory_signup.objects.get(laboratory_email=user_identity_email)
        all = {'get_lab_info':get_lab_info}
        return render(request, 'laboratory/laboratory-profile.html', all)

def laboratory_pro_change_pass(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        get_password = request.POST.get('get_password')
        get_newpassword = request.POST.get('get_newpassword')

        user_identity = User.objects.get(id=user_id)
        user_identity.password = get_password
        user_identity.password = make_password(get_newpassword)
        user_identity.save()
        messages.info(request, " Your Password has been change successfully")
        return redirect('/laboratory_signup/laboratory_login/')
    else:
        user_identity = request.user
        user_identity_email = user_identity.email
        get_lab_info = Laboratory_signup.objects.get(laboratory_email=user_identity_email)
        all = {'get_lab_info':get_lab_info}
        return render(request, 'laboratory/laboratory-profile.html', all)

# ADMIN VIEWS
def admin_signup(request):
    if request.method == 'POST':
        # Submit to Database
        get_admin_name = request.POST.get('get_admin_name')
        get_admin_username = request.POST.get('get_admin_username')
        get_admin_email = request.POST.get('get_admin_email')
        get_admin_phone = request.POST.get('get_admin_phone')
        get_admin_password = request.POST.get('get_admin_password')

        if User.objects.filter(email=get_admin_email).exists(): # CHECK FOR THE SAME EMAIL
            messages.warning(request, 'Email already exists!!!, Please alter')
            return redirect("/logout_dash/thisisonlyfortheadminanditissecret/")
        elif User.objects.filter(username=get_admin_username).exists(): # CHECK FOR THE SAME USERNAME
            messages.warning(request, 'Username already exists!!!, Please alter')
            return redirect("/logout_dash/thisisonlyfortheadminanditissecret/")
        elif User.objects.filter(is_superuser="1").exists(): # CHECK FOR THE SAME USERNAME
            messages.warning(request, 'Admin already exists!!!, Can`t create another Admin')
            return redirect("/logout_dash/thisisonlyfortheadminanditissecret/")
        else: # ELSE SUBMIT TO DATABASE
            if 'fileToUpload' in request.FILES:
                passport = request.FILES['fileToUpload']
            else:
                passport = 'abc.jpg'  
            submit_user = User.objects.create_user(password = get_admin_password, username = get_admin_username, first_name = get_admin_name, email = get_admin_email, is_superuser="1")
            submit_user.save()
            # name	email	gender	phone	dob	student_class	
            submit_others = Admin_signup.objects.create(admin=submit_user, admin_name = get_admin_name, admin_username = get_admin_username, admin_email = get_admin_email, admin_phone = get_admin_phone, profile_picture = passport)
            submit_others.save()
            messages.success(request, get_admin_name + " have successfully registered")
            return redirect('/register/login/')
    else:
        return render(request, 'admin/admin_signup.html')

def admin_dash(request):
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    count_unreg_patient = Add_patient.objects.all().count()
    count_reg_patient = Patient_signup.objects.all().count()
    count_approve_doctor = Doctor_signup.objects.filter(status='Active').count()
    count_pending_doctor = Doctor_signup.objects.filter(status='Pending').count()
    count_approve_pharmacy = Pharmacy_signup.objects.filter(status='Active').count()
    count_pending_pharmacy = Pharmacy_signup.objects.filter(status='Pending').count()
    count_approve_laboratory = Laboratory_signup.objects.filter(status='Active').count()
    count_pending_laboratory = Laboratory_signup.objects.filter(status='Pending').count()
    count_approve_accountant = Acct_signup.objects.filter(status='Active').count()
    count_pending_accountant = Acct_signup.objects.filter(status='Pending').count()
    count_approve_nurse = Acct_signup.objects.filter(status='Active').count()
    count_pending_nurse = Acct_signup.objects.filter(status='Pending').count()
    count_payment = Add_invoice.objects.all().count()
    count_medicine = Add_medicine.objects.all().count()
    count_appointment = Doctor_appointment.objects.all().count()

    all = {'get_admin_info':get_admin_info, 'count_unreg_patient':count_unreg_patient, 'count_reg_patient':count_reg_patient, 'count_payment':count_payment, 'count_medicine':count_medicine, 'count_appointment':count_appointment, 'count_approve_doctor':count_approve_doctor, 'count_pending_doctor':count_pending_doctor, 'count_approve_pharmacy':count_approve_pharmacy, 'count_pending_pharmacy':count_pending_pharmacy, 'count_approve_laboratory':count_approve_laboratory, 'count_pending_laboratory':count_pending_laboratory, 'count_approve_accountant':count_approve_accountant, 'count_pending_accountant':count_pending_accountant, 'count_approve_nurse':count_approve_nurse, 'count_pending_nurse':count_pending_nurse,}
    return render(request, 'admin/admin_dash.html', all)

def admin_department(request):
    if request.method == 'POST':
        get_depart_title = request.POST.get('get_depart_title')
        get_depart_description = request.POST.get('get_depart_description')

        if 'fileToUpload' in request.FILES:
            passport = request.FILES['fileToUpload']
        else:
            passport = 'abc.jpg'
        submit_department = Add_department.objects.create(depart_title = get_depart_title, depart_description = get_depart_description, depart_icon = passport)
        submit_department.save()
        messages.success(request, get_depart_title + " have successfully registered")
        return redirect('/admin_dash/department/')
    else:
        get_department = Add_department.objects.all()

        user_identity = request.user
        user_identity_email = user_identity.email
        get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

        all = {'get_admin_info':get_admin_info, 'get_department':get_department}
        return render(request, 'admin/admin_department.html', all)

def admin_edit_department(request, id):
    if request.method == 'POST':
        old_image = request.POST.get('old_image')
        get_depart_title = request.POST.get('get_depart_title')
        get_depart_description = request.POST.get('get_depart_description')

        if 'fileToUpload' in request.FILES:
            passport = request.FILES['fileToUpload'] # This is for new image
        else:
            passport = old_image.replace('/media/', '') # Maintain the old image

        user_identity = Add_department.objects.get(id=id)
        user_identity.depart_icon = passport
        user_identity.depart_title = get_depart_title
        user_identity.depart_description = get_depart_description
        user_identity.save()
        messages.success(request, get_depart_title + " have successfully registered")
        return redirect('/admin_dash/department/')
    else:
        get_department = Add_department.objects.all()
        get_department_id = Add_department.objects.get(id=id)
        user_identity = request.user
        user_identity_email = user_identity.email
        get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
        all = {'get_admin_info':get_admin_info, 'get_department_id': get_department_id, 'get_department':get_department}
        return render(request, 'admin/admin_department.html', all)
    
def admin_confirm_delete_department(request, id):
    get_departments_id = Add_department.objects.get(id=id)
    get_department = Add_department.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all = {'get_department': get_department, 'get_departments_id':get_departments_id, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_department.html', all)

def admin_delete_department(request, id):
    get_department = Add_department.objects.get(id=id)
    get_department.delete()
    return redirect("/admin_dash/department/")

# All Doctor
def admin_all_doctor(request):
    get_doctor = Doctor_signup.objects.filter(status='Active')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all2 = {'get_doctor':get_doctor, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_approved_doctor.html', all2)

def admin_view_pending_doctor(request, id):
    get_doctor_id = Doctor_signup.objects.get(id=id)
    pending_doctor = Doctor_signup.objects.filter(status='Pending')

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'pending_doctor': pending_doctor, 'get_doctor_id':get_doctor_id}
    return render(request, 'admin/admin_all_pending_doctor.html', all)

def admin_all_pending_doctor(request):
    pending_doctor = Doctor_signup.objects.filter(status='Pending')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all = {'pending_doctor':pending_doctor, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_pending_doctor.html', all)

def admin_approve_doctor(request, user_id):
    if request.method == 'POST':
        # Retrieve the DoctorSignup instance
        doctor_account = Doctor_signup.objects.get(pk=user_id)
        
        # Update status to 'Active'
        doctor_account.status = 'Approve'
        doctor_account.save()
        
        # Redirect back to pending accounts page or any other appropriate page
        return redirect('/admin_dash/pending_doctor/')
    else:
        # Handle GET request if needed
        return render(request, 'admin/admin_all_pending_doctor.html')
    
def admin_view_doctor(request, id):
    get_doctor_id = Doctor_signup.objects.get(id=id)
    get_doctor = Doctor_signup.objects.filter(status='Active')

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_doctor': get_doctor, 'get_doctor_id':get_doctor_id}
    return render(request, 'admin/admin_all_approved_doctor.html', all)

def admin_confirm_delete_doctor(request, id):
    get_doctor = Doctor_signup.objects.all()
    get_doctors_id = Doctor_signup.objects.get(id=id)
    get_doctors = Doctor_signup.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_doctors': get_doctors, 'get_doctor': get_doctor, 'get_doctors_id':get_doctors_id}
    return render(request, 'admin/admin_all_approved_doctor.html', all)

def admin_delete_doctor(request, id):
    get_staff = Doctor_signup.objects.get(id=id)
    delete_from_auth_user = User.objects.get(id=get_staff.user_id)
    get_staff.delete()
    delete_from_auth_user.delete()
    return redirect("/admin_dash/doctor")

# All Patient
def admin_all_patient(request):
    get_patient = Patient_signup.objects.all()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all2 = { 'get_admin_info':get_admin_info, 'get_patient':get_patient}
    return render(request, 'admin/admin_all_patient.html', all2)
    
def admin_view_patient(request, id):
    get_patient_id = Patient_signup.objects.get(id=id)
    get_patient = Patient_signup.objects.all()
    return render(request, 'admin/admin_all_patient.html', {'get_patient': get_patient, 'get_patient_id':get_patient_id})

def admin_confirm_delete_patient(request, id):
    get_patients_id = Patient_signup.objects.get(id=id)
    get_patient = Patient_signup.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_patient': get_patient, 'get_patients_id':get_patients_id}
    return render(request, 'admin/admin_all_patient.html', all)

def admin_delete_patient(request, id):
    get_staff = Patient_signup.objects.get(id=id)
    del_from_auth_user = User.objects.get(id=get_staff.user_id)
    get_staff.delete()
    del_from_auth_user.delete()
    return redirect("/admin_dash/patient")

# All Pharmacist
def admin_all_pharmacist(request):
    get_pharmacist = Pharmacy_signup.objects.filter(status='Active')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all2 = {'get_pharmacist':get_pharmacist, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_pharmacist.html', all2)

def admin_view_pending_pharmacist(request, id):
    get_pharmacist_id = Pharmacy_signup.objects.get(id=id)
    pending_pharmacist = Pharmacy_signup.objects.filter(status='Pending')

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'pending_pharmacist': pending_pharmacist, 'get_pharmacist_id':get_pharmacist_id}
    return render(request, 'admin/admin_all_pending_pharmacist.html', all)

def admin_all_pending_pharmacist(request):
    pending_pharmacist = Pharmacy_signup.objects.filter(status='Pending')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all = {'pending_pharmacist':pending_pharmacist, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_pending_pharmacist.html', all)

def admin_approve_pharmacist(request, user_id):
    if request.method == 'POST':
        # Retrieve the PharmacistSignup instance
        pharmacist_account = Pharmacy_signup.objects.get(pk=user_id)
        
        # Update status to 'Active'
        pharmacist_account.status = 'Approve'
        pharmacist_account.save()
        
        # Redirect back to pending accounts page or any other appropriate page
        return redirect('/admin_dash/pending_pharmacist/')
    else:
        # Handle GET request if needed
        return render(request, 'admin/admin_all_pending_pharmacist.html')
    
def admin_view_pharmacist(request, id):
    get_pharmacist_id = Pharmacy_signup.objects.get(id=id)
    get_pharmacist = Pharmacy_signup.objects.filter(status='Active')

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_pharmacist': get_pharmacist, 'get_pharmacist_id':get_pharmacist_id}
    return render(request, 'admin/admin_all_pharmacist.html', all)

def admin_confirm_delete_pharmacist(request, id):
    get_pharmacist = Pharmacy_signup.objects.all()
    get_pharmacists_id = Pharmacy_signup.objects.get(id=id)

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_pharmacist': get_pharmacist, 'get_pharmacists_id':get_pharmacists_id}
    return render(request, 'admin/admin_all_pharmacist.html', all)

def admin_delete_pharmacist(request, id):
    get_staff = Pharmacy_signup.objects.get(id=id)
    get_staff.delete()
    del_from_auth_user = User.objects.get(id=get_staff.user_id)
    del_from_auth_user.delete()
    return redirect("/admin_dash/pharmacist")

# All Laboratory
def admin_all_laboratorist(request):
    get_laboratorist = Laboratory_signup.objects.filter(status='Active')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all2 = {'get_laboratorist':get_laboratorist, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_laboratorist.html', all2)

def admin_view_pending_laboratorist(request, id):
    get_laboratorist_id = Laboratory_signup.objects.get(id=id)
    pending_laboratorist = Laboratory_signup.objects.filter(status='Pending')

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'pending_laboratorist': pending_laboratorist, 'get_laboratorist_id':get_laboratorist_id}
    return render(request, 'admin/admin_all_pending_laboratorist.html', all)

def admin_all_pending_laboratorist(request):
    pending_laboratorist = Laboratory_signup.objects.filter(status='Pending')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all = {'pending_laboratorist':pending_laboratorist, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_pending_laboratorist.html', all)

def admin_approve_laboratorist(request, user_id):
    if request.method == 'POST':
        # Retrieve the laboratoristSignup instance
        laboratorist_account = Laboratory_signup.objects.get(pk=user_id)
        
        # Update status to 'Active'
        laboratorist_account.status = 'Approve'
        laboratorist_account.save()
        
        # Redirect back to pending accounts page or any other appropriate page
        return redirect('/admin_dash/pending_laboratorist/')
    else:
        # Handle GET request if needed
        return render(request, 'admin/admin_all_pending_laboratorist.html')
    
def admin_view_laboratorist(request, id):
    get_laboratorist_id = Laboratory_signup.objects.get(id=id)
    get_laboratorist = Laboratory_signup.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_laboratorist': get_laboratorist, 'get_laboratorist_id':get_laboratorist_id}
    return render(request, 'admin/admin_all_laboratorist.html', all)

def admin_confirm_delete_laboratorist(request, id):
    get_laboratorist = Laboratory_signup.objects.all()
    get_laboratorists_id = Laboratory_signup.objects.get(id=id)

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_laboratorist': get_laboratorist, 'get_laboratorists_id':get_laboratorists_id}
    return render(request, 'admin/admin_all_laboratorist.html', all)

def admin_delete_laboratorist(request, id):
    get_staff = Laboratory_signup.objects.get(id=id)
    get_staff.delete()
    del_from_auth_user = User.objects.get(id=get_staff.user_id)
    del_from_auth_user.delete()
    return redirect("/admin_dash/laboratorist")

# All Accountant
def admin_all_accountant(request):
    get_accountant = Acct_signup.objects.filter(status='Active')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all2 = {'get_accountant':get_accountant, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_accountant.html', all2)

def admin_view_pending_accountant(request, id):
    get_accountant_id = Acct_signup.objects.get(id=id)
    pending_accountant = Acct_signup.objects.filter(status='Pending')

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'pending_accountant': pending_accountant, 'get_accountant_id':get_accountant_id}
    return render(request, 'admin/admin_all_pending_accountant.html', all)

def admin_all_pending_accountant(request):
    pending_accountant = Acct_signup.objects.filter(status='Pending')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all = {'pending_accountant':pending_accountant, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_pending_accountant.html', all)

def admin_approve_accountant(request, user_id):
    if request.method == 'POST':
        # Retrieve the accountantSignup instance
        accountant_account = Acct_signup.objects.get(pk=user_id)
        
        # Update status to 'Active'
        accountant_account.status = 'Approve'
        accountant_account.save()
        
        # Redirect back to pending accounts page or any other appropriate page
        return redirect('/admin_dash/pending_accountant/')
    else:
        # Handle GET request if needed
        return render(request, 'admin/admin_all_pending_accountant.html')
    
def admin_view_accountant(request, id):
    get_accountant_id = Acct_signup.objects.get(id=id)
    get_accountant = Acct_signup.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_accountant': get_accountant, 'get_accountant_id':get_accountant_id}
    return render(request, 'admin/admin_all_accountant.html', all)

def admin_confirm_delete_accountant(request, id):
    get_accountant = Acct_signup.objects.all()
    get_accountants_id = Acct_signup.objects.get(id=id)

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_accountant': get_accountant, 'get_accountants_id':get_accountants_id}
    return render(request, 'admin/admin_all_accountant.html', all)

def admin_delete_accountant(request, id):
    get_staff = Acct_signup.objects.get(id=id)
    get_staff.delete()
    del_from_auth_user = User.objects.get(id=get_staff.user_id)
    del_from_auth_user.delete()
    return redirect("/admin_dash/accountant")

# All Receptionist
def admin_all_receptionist(request):
    get_receptionist = Hospital_reg.objects.filter(status='Active')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all2 = {'get_receptionist':get_receptionist, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_receptionist.html', all2)

def admin_view_pending_receptionist(request, id):
    get_receptionist_id = Hospital_reg.objects.get(id=id)
    pending_receptionist = Hospital_reg.objects.filter(status='Pending')

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'pending_receptionist': pending_receptionist, 'get_receptionist_id':get_receptionist_id}
    return render(request, 'admin/admin_all_pending_receptionist.html', all)

def admin_all_pending_receptionist(request):
    pending_receptionist = Hospital_reg.objects.filter(status='Pending')
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all = {'pending_receptionist':pending_receptionist, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_pending_receptionist.html', all)

def admin_approve_receptionist(request, user_id):
    if request.method == 'POST':
        # Retrieve the receptionistSignup instance
        receptionist_account = Hospital_reg.objects.get(pk=user_id)
        
        # Update status to 'Active'
        receptionist_account.status = 'Approve'
        receptionist_account.save()
        
        # Redirect back to pending accounts page or any other appropriate page
        return redirect('/admin_dash/pending_receptionist/')
    else:
        # Handle GET request if needed
        return render(request, 'admin/admin_all_pending_receptionist.html')
    
def admin_view_receptionist(request, id):
    get_receptionist_id = Hospital_reg.objects.get(id=id)
    get_receptionist = Hospital_reg.objects.all()

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_receptionist': get_receptionist, 'get_receptionist_id':get_receptionist_id}
    return render(request, 'admin/admin_all_receptionist.html', all)

def admin_confirm_delete_receptionist(request, id):
    get_receptionist = Hospital_reg.objects.all()
    get_receptionists_id = Hospital_reg.objects.get(id=id)

    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)

    all = {'get_admin_info':get_admin_info, 'get_receptionist': get_receptionist, 'get_receptionists_id':get_receptionists_id}
    return render(request, 'admin/admin_all_receptionist.html', all)

def admin_delete_receptionist(request, id):
    get_staff = Hospital_reg.objects.get(id=id)
    get_staff.delete()
    del_from_auth_user = User.objects.get(id=get_staff.user_id)
    del_from_auth_user.delete()
    return redirect("/admin_dash/receptionist")

# All Appointment
def admin_all_appointment(request):
    get_appointment = Doctor_appointment.objects.all()
    count_appointment = Doctor_appointment.objects.all().count()
    user_identity = request.user
    user_identity_email = user_identity.email
    get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
    all = {'get_appointment':get_appointment, 'count_appointment':count_appointment, 'get_admin_info':get_admin_info}
    return render(request, 'admin/admin_all_appointment.html', all)
    
def admin_view_appointment(request, id):
    get_appointment_id = Add_appointment.objects.get(id=id)
    get_appointment = Add_appointment.objects.all()
    get_appointment_details = Add_appointment.objects.all()
    return render(request, 'admin/admin_all_appointment.html', {'get_appointment': get_appointment, 'get_appointment_details': get_appointment_details, 'get_appointment_id':get_appointment_id})

def admin_confirm_delete_appointment(request, id):
    get_appointments_id = Add_appointment.objects.get(id=id)
    get_appointments = Add_appointment.objects.all()
    get_appointment_profiles = Add_appointment.objects.all()
    return render(request, 'admin/admin_all_appointment.html', {'get_appointments': get_appointments, 'get_appointment_profiles': get_appointment_profiles, 'get_appointments_id':get_appointments_id})

def admin_delete_appointment(request, id):
    get_staff = Add_appointment.objects.get(id=id)
    get_staff.delete()
    return redirect("/admin_dash/admin_all_appointment")

# PHARMACY
# def admin_all_appointment(request):
#     get_appointment = Doctor_appointment.filter(status='Active')
#     user_identity = request.user
#     user_identity_email = user_identity.email
#     get_admin_info = Admin_signup.objects.get(admin_email=user_identity_email)
#     all = {'get_appointment':get_appointment, 'get_admin_info':get_admin_info}
#     return render(request, 'admin/admin_all_appointment.html', all)


# def get_prices(request):
#     if request.method == 'GET':
#         product_name = request.GET['get_product_name']
#         get_product_id = Add_medicine_category.objects.get(product_name=product_name)
#         product_price = get_product_id.product_price
#         return HttpResponse(product_price)