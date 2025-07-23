from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

# Create your models here.

class Hospital_reg(models.Model):
    PENDING = 'Pending'
    APPROVE = 'Approve'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVE, 'Approve'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = ResizedImageField(size=[300, 300], upload_to="user_profile/", null=True, blank=True)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    class Meta:
        managed=True
        db_table='hospital_reg'

class Add_patient(models.Model):
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    patient_no = models.CharField(max_length=15, blank=True, null=True)
    patient_phone = models.CharField(max_length=15, blank=True, null=True)
    patient_blood_group = models.CharField(max_length=5, blank=True, null=True)
    patient_dob = models.DateField(blank=True, null=True)
    patient_gender = models.CharField(max_length=50, blank=True, null=True)
    patient_address = models.CharField(max_length=500, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_patient'

class Patient_signup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = ResizedImageField(size=[300, 300], upload_to="patient_profile/", null=True, blank=True)
    patient_name = models.CharField(max_length=150, blank=True, null=True)
    patient_address = models.CharField(max_length=500, blank=True, null=True)
    patient_no = models.CharField(max_length=20, blank=True, null=True)
    patient_email = models.EmailField(max_length=500, blank=True, null=True)
    patient_phone = models.CharField(max_length=15, blank=True, null=True)
    patient_gender = models.CharField(max_length=500, blank=True, null=True)
    patient_dob = models.DateField(blank=True, null=True)
    patient_blood_group = models.CharField(max_length=5, blank=True, null=True)
    class Meta:
        managed=True
        db_table='patient_signup'
        
class Add_appointment(models.Model):
    appointment_date = models.DateField(blank=True, null=True)
    appointment_time = models.TimeField(blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_appointment'

class Doctor_signup(models.Model):
    PENDING = 'Pending'
    APPROVE = 'Approve'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVE, 'Approve'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = ResizedImageField(size=[300, 300], upload_to="doctor_profile/", null=True, blank=True)
    doctor_fullName = models.CharField(max_length=150, blank=True, null=True)
    doctor_phone = models.CharField(max_length=15, blank=True, null=True)
    doctor_email = models.EmailField(max_length=500, blank=True, null=True)
    doctor_gender = models.CharField(max_length=500, blank=True, null=True)
    doctor_reg_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        managed = True
        db_table = 'doctor_signup'

class Doctor_appointment(models.Model):
    appointment_date = models.DateField(blank=True, null=True)
    appointment_time = models.TimeField(blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    patient_no = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        managed=True
        db_table='doctor_appointment'

class Add_patient_prescription(models.Model):
    prescription_date = models.DateField(auto_now_add=True, blank=True, null=True)
    prescription_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    patient_blood_group = models.CharField(max_length=5, blank=True, null=True)
    patient_gender = models.CharField(max_length=10, blank=True, null=True)
    case_history = models.CharField(max_length=1000, blank=True, null=True)
    medication = models.CharField(max_length=1000, blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_patient_prescription'

class Add_patient_diagnosis(models.Model):
    diagnosis_date = models.DateField(blank=True, null=True)
    diagnosis_time = models.TimeField(blank=True, null=True)
    report_type = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to="patient_diagnosis_file/", max_length=100, blank=True, null=True)
    document_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_patient_diagnosis'

class Add_bed_allotment(models.Model):
    bed_number = models.CharField(max_length=100, blank=True, null=True)
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    allotment_time = models.TimeField(blank=True, null=True)
    discharge_time = models.TimeField(blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_bed_allotment'

class Add_report(models.Model):
    report_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    report_date = models.DateField(blank=True, null=True)
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_report'

class Admin_signup(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = ResizedImageField(size=[300, 300], upload_to="admin_profile/", null=True, blank=True)
    admin_name = models.CharField(max_length=150, blank=True, null=True)
    admin_username = models.CharField(max_length=150, blank=True, null=True)
    admin_email = models.EmailField(max_length=500, blank=True, null=True)
    admin_phone = models.CharField(max_length=15, blank=True, null=True)
    class Meta:
        managed=True
        db_table='admin_signup'

# PHARMACY
class Pharmacy_signup(models.Model):
    PENDING = 'Pending'
    APPROVE = 'Approve'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVE, 'Approve'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = ResizedImageField(size=[300, 300], upload_to="pharmacy_profile/", null=True, blank=True)
    pharmacy_name = models.CharField(max_length=150, blank=True, null=True)
    pharmacy_email = models.EmailField(max_length=500, blank=True, null=True)
    pharmacy_phone = models.CharField(max_length=15, blank=True, null=True)
    pharmacy_gender = models.CharField(max_length=15, blank=True, null=True)
    pharmacy_username = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    class Meta:
        managed=True
        db_table='pharmacy_signup'

class Add_medicine_category(models.Model):
    medicine_category = models.CharField(max_length=150, blank=True, null=True)
    medicine_category_description = models.CharField(max_length=1000, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_medicine_category'

class Add_medicine(models.Model):
    medicine_name = models.CharField(max_length=150, blank=True, null=True)
    medicine_category = models.CharField(max_length=150, blank=True, null=True)
    medicine_category_description = models.CharField(max_length=1000, blank=True, null=True)
    medicine_price = models.IntegerField(blank=True, null=True)
    total_quantity = models.IntegerField(blank=True, null=True)
    manufacture_company = models.CharField(max_length=500, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_medicine'

class Add_sales_medicine(models.Model):
    customer_name = models.CharField(max_length=150, blank=True, null=True)
    medicine_name = models.CharField(max_length=150, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    medicine_price = models.CharField(max_length=20, blank=True, null=True)
    sales_total_price = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_sales_medicine'

class Add_to_cart(models.Model):
    product = models.CharField(max_length=150, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    invoice_no = models.IntegerField(blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_to_cart'

class Add_sales(models.Model):
    customer_name = models.CharField(max_length=150, blank=True, null=True)
    customer_phone = models.CharField(max_length=15, blank=True, null=True)
    invoice_no = models.IntegerField(blank=True, null=True)
    amount_paid = models.CharField(max_length=20, blank=True, null=True)
    sales_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_sales'

# ACCOUNT
class Acct_signup(models.Model):
    PENDING = 'Pending'
    APPROVE = 'Approve'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVE, 'Approve'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = ResizedImageField(size=[300, 300], upload_to="acct_profile/", null=True, blank=True)
    acct_name = models.CharField(max_length=150, blank=True, null=True)
    acct_username = models.CharField(max_length=150, blank=True, null=True)
    acct_email = models.EmailField(max_length=500, blank=True, null=True)
    acct_phone = models.CharField(max_length=15, blank=True, null=True)
    acct_gender = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    class Meta:
        managed=True
        db_table='acct_signup'

class Add_invoice(models.Model):
    invoice_title = models.CharField(max_length=150, blank=True, null=True)
    invoice_number = models.CharField(max_length=150, blank=True, null=True)
    patient_name = models.CharField(max_length=150, blank=True, null=True)
    patient_address = models.CharField(max_length=500, blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    pay_status = models.CharField(max_length=15, blank=True, null=True)
    des_invoice = models.CharField(max_length=200, blank=True, null=True)
    amount = models.CharField(max_length=15, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_invoice'

# LABORATORY
class Laboratory_signup(models.Model):
    PENDING = 'Pending'
    APPROVE = 'Approve'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVE, 'Approve'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = ResizedImageField(size=[300, 300], upload_to="laboratory_profile/", null=True, blank=True)
    laboratory_name = models.CharField(max_length=150, blank=True, null=True)
    laboratory_username = models.CharField(max_length=150, blank=True, null=True)
    laboratory_email = models.EmailField(max_length=500, blank=True, null=True)
    laboratory_gender = models.CharField(max_length=15, blank=True, null=True)
    laboratory_phone = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    class Meta:
        managed=True
        db_table='laboratory_signup'

class Add_blood_donor(models.Model):
    donor_name = models.CharField(max_length=150, blank=True, null=True)
    donor_address = models.CharField(max_length=500, blank=True, null=True)
    donor_phone = models.CharField(max_length=15, blank=True, null=True)
    donor_gender = models.CharField(max_length=25, blank=True, null=True)
    donor_age = models.IntegerField(blank=True, null=True)
    donor_blood_group = models.CharField(max_length=6, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_blood_donor'

# ADMIN
class Add_department(models.Model):
    depart_icon = ResizedImageField(size=[300, 300], upload_to="depart_icon/", null=True, blank=True)
    depart_title = models.CharField(max_length=150, blank=True, null=True)
    depart_description = models.CharField(max_length=500, blank=True, null=True)
    class Meta:
        managed=True
        db_table='add_department'