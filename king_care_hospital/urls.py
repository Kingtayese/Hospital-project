"""
URL configuration for king_care_hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from king_care import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('dashboard/', views.dashboard), # Load dashboard page

    path('logout_dash/register/', views.register),

    path('register/login/', views.login),

    path('logout/logout_dash/', views.logout_dash),
    
    path('', views.logout_dash),

    path('dashboard/patient/', views.add_patient),
    
    path('patient/view_patient/<int:id>', views.view_patient),

    # path('patient/doctor_view_patient_medic/<int:id>', views.doctor_view_patient_medic),

    path('patient/confirm_delete_patient/<int:id>', views.confirm_delete_patient),

    path('confirm_delete_patient/delete_patient/<int:id>', views.delete_patient),
    
    path("get-doctors-availability/", views.get_doctors_with_availability, name="get_doctors_with_availability"),

    path('dashboard/appointment/', views.appointment, name='appointment'),
    
    path('appointment/edit/<int:id>/', views.appointment_edit, name='appointment_edit'),
    
    path('appointments/confirm_delete/<int:id>/', views.appointment_confirm_delete, name='appointment_confirm_delete'),
    
    path('appointments/delete/<int:id>/', views.appointment_delete, name='appointment_delete'),

    path('dashboard/payroll_list/', views.payroll),

    path('dashboard/receptionist_pro/', views.receptionist_pro),

    path('dashboard/receptionist_pro_change_pass/', views.receptionist_pro_change_pass),

    # PATIENT PAGES
    path('logout_dash/patient_register/', views.patient_signup),
    
    path('patient_register/patient_login/', views.patient_login),

    path('patient_dash/', views.patient_dashboard),

    path('patient_dash/appointment_list/', views.patient_appointment),
    
    path('get_patient_no/', views.get_patient_no),

    path('patient_dash/prescription/', views.patient_prescription),

    path('patient_dash/admit_history/', views.patient_admit_history),

    path('patient_dash/operation_history/', views.patient_operation_history),

    path('patient_dash/invoice/', views.patient_invoice),

    path('patient_dash/profile/', views.patient_profile),

    path('patient_dash/other_info/', views.patient_other_info),

    path('patient_dash/change_password/', views.patient_change_pass),

    # URL FOR GETTING PATIENT INFO
    path('get_patient_name/', views.get_patient_name),

    path('get_patient_phone/', views.get_patient_phone),
    
    path('get_patient_blood_group/', views.get_patient_blood_group),
    
    path('get_patient_dob/', views.get_patient_dob),
    
    path('get_patient_gender/', views.get_patient_gender),
    
    path('get_patient_addresses/', views.get_patient_addresses),

    # DOCTOR PAGES
    path('logout_dash/doc_signup/', views.doc_signup),

    path('doc_signup/doc_login/', views.doc_login),

    path('doctor_dash/', views.doctor_dash),

    path('doctor_dash/appointment/', views.doctor_appointment),

    path('appointment/edit_appointment/<int:id>', views.doctor_edit_appointment),

    path('appointment/confirm_delete_appointment/<int:id>', views.doctor_confirm_delete_appointment),
    
    path('confirm_delete_appointment/delete_appointment/<int:id>', views.doctor_delete_appointment),

    path('doctor_dash/prescription/', views.doctor_prescription),
    
    path('get_patient_blood_groups/', views.get_patient_blood_groups),
    
    path('get_patient_genders/', views.get_patient_genders),

    path('prescription/edit_prescription/<int:id>', views.doctor_edit_prescription),

    path('prescription/view_prescription/<int:id>', views.doctor_view_prescription),

    path('prescription/confirm_delete_prescription/<int:id>', views.doctor_confirm_delete_prescription),
    
    path('confirm_delete_prescription/delete_prescription/<int:id>', views.doctor_delete_prescription),

    path('doctor_dash/patient/', views.doctor_patient),

    path('doctor_dash/view_patient_profile/<int:id>', views.doctor_view_patient_profile),

    path('doctor_dash/bed_allotment/', views.doctor_bed_allotment),

    path('bed_allotment/edit_bed_allotment/<int:id>', views.doctor_edit_bed_allotment),

    path('bed_allotment/confirm_delete_bed_allotment/<int:id>', views.doctor_confirm_delete_bed_allotment),

    path('confirm_delete_bed_allotment/delete_bed_allotment/<int:id>', views.doctor_delete_bed_allotment),

    path('doctor_dash/blood_bank/', views.doctor_blood_bank),

    path('doctor_dash/report/', views.doctor_report),

    path('report/edit_report/<int:id>', views.doctor_edit_report),

    path('report/view_report/<int:id>', views.doctor_view_report),

    path('report/confirm_delete_report/<int:id>', views.doctor_confirm_delete_report),

    path('confirm_delete_report/delete_report/<int:id>', views.doctor_delete_report),

    path('doctor_dash/payroll_list/', views.doctor_payroll),

    path('doctor_dash/doctor_pro', views.doctor_pro),

    path('doctor_dash/doctor_pro_change_pass', views.doctor_pro_change_pass),

    # PHARMACY
    path('logout_dash/pharmacy_signup/', views.pharmacy_signup),

    path('pharmacy_signup/pharmacy_login/', views.pharmacy_login),

    path('pharmacy_dash/', views.pharmacy_dash),

    path('pharmacy_dash/medicine_category/', views.pharmacy_medicine_category),

    path('medicine_category/edit_medicine_category/<int:id>', views.pharmacy_edit_medicine_category),

    path('medicine_category/confirm_delete_medicine_category/<int:id>', views.pharmacy_confirm_delete_medicine_category),

    path('confirm_delete_medicine_category/delete_medicine_category/<int:id>', views.pharmacy_delete_medicine_category),
    
    path('product_medicine/confirm_delete_product_medicine/<int:id>', views.pharmacy_confirm_delete_product_medicine),

    path('confirm_delete_product_medicine/delete_product_medicine/<int:id>', views.pharmacy_delete_product_medicine),

    path('get_info/', views.get_info),

    path('pharmacy_dash/manage_medicine/', views.pharmacy_manage_medicine),

    path('pharmacy_dash/medicine_sales/', views.pharmacy_medicine_sales),

    path('medicine_sales/add_medicine_sales/', views.pharmacy_add_medicine_sales),

    path('get_price/', views.get_price),

    path('add_to_cart', views.add_to_cart),

    path('add_sales', views.add_sales),

    path('edit_sales/<int:id>', views.edit_sales),
    
    path('medicine_sales/confirm_delete_sale/<int:id>', views.pharmacy_confirm_delete_sale),

    path('confirm_delete_sale/delete_sale/<int:id>', views.pharmacy_delete_sale),

    path('confirm_delete_medicine/<int:id>', views.pharmacy_confirm_delete_medicine),

    path('delete_medicine/<int:id>', views.pharmacy_delete_medicine),

    path('pharmacy_dash/payroll_list/', views.pharmacy_payroll),

    path('pharmacy_dash/pharmacy_pro', views.pharmacy_pro),

    path('pharmacy_dash/pharmacy_pro_change_pass', views.pharmacy_pro_change_pass),

    # ACCOUNT
    path('logout_dash/acct_signup/', views.acct_signup),

    path('acct_signup/acct_login/', views.acct_login),

    path('acct_dash/', views.acct_dash),

    path('acct_dash/add_invoice/', views.acct_add_invoice),

    path('get_patient_address/', views.get_patient_address),

    path('acct_dash/manage_invoice/', views.acct_manage_invoice),

    path('manage_invoice/edit_invoice/<int:id>', views.acct_edit_invoice),

    path('manage_invoice/view_invoice/<int:id>', views.acct_view_invoice),

    path('manage_invoice/confirm_delete_invoice/<int:id>', views.acct_confirm_delete_invoice),

    path('confirm_delete_invoice/delete_invoice/<int:id>', views.acct_delete_invoice),

    path('acct_dash/payroll_list/', views.acct_payroll),

    path('acct_dash/acct_pro', views.acct_pro),

    path('acct_dash/acct_pro_change_pass', views.acct_pro_change_pass),

    # LABORATORY
    path('logout_dash/laboratory_signup/', views.laboratory_signup),

    path('laboratory_signup/laboratory_login/', views.laboratory_login),

    path('laboratory_dash/', views.laboratory_dash),

    path('laboratory_dash/blood_bank/', views.laboratory_blood_bank),

    path('laboratory_dash/blood_donor/', views.laboratory_blood_donor),

    path('blood_donor/edit_donor/<int:id>', views.laboratory_edit_blood_donor),

    path('blood_donor/confirm_delete_donor/<int:id>', views.laboratory_confirm_delete_donor),

    path('confirm_delete_donor/delete_donor/<int:id>', views.laboratory_delete_donor),

    path('laboratory_dash/payroll_list/', views.laboratory_payroll),

    path('laboratory_dash/laboratory_pro', views.laboratory_pro),

    path('laboratory_dash/laboratory_pro_change_pass', views.laboratory_pro_change_pass),




    # ADMIN PAGES
    path('logout_dash/thisisonlyfortheadminanditissecret/', views.admin_signup),

    path('admin_dash/', views.admin_dash),

    # path('admin_dash/department/', views.admin_department),

    # path('department/edit_department/<int:id>', views.admin_edit_department),

    # path('department/confirm_delete_department/<int:id>', views.admin_confirm_delete_department),

    # path('confirm_delete_department/delete_department/<int:id>', views.admin_delete_department),

# All Doctor
    path('admin_dash/doctor/', views.admin_all_doctor),
    
    path('admin_dash/pending_doctor/', views.admin_all_pending_doctor),
    
    path('pending_doctor/approved_doctor/<int:user_id>', views.admin_approve_doctor),

    path('pending_doctor/view_pending_doctor/<int:id>', views.admin_view_pending_doctor),
    
    path('doctor/view_doctor/<int:id>', views.admin_view_doctor),

    path('doctor/confirm_delete_doctor/<int:id>', views.admin_confirm_delete_doctor),

    path('confirm_delete_doctor/delete_doctor/<int:id>', views.admin_delete_doctor),

# All Patient
    path('admin_dash/patient/', views.admin_all_patient),

    path('patients/view_patient/<int:id>', views.admin_view_patient),

    path('patients/confirm_delete_patient/<int:id>', views.admin_confirm_delete_patient),

    path('confirm_delete_patient/delete_patients/<int:id>', views.admin_delete_patient),

# All Pharmacist
    path('admin_dash/pharmacist/', views.admin_all_pharmacist),
    
    path('admin_dash/pending_pharmacist/', views.admin_all_pending_pharmacist),
    
    path('pending_pharmacist/approved_pharmacist/<int:user_id>', views.admin_approve_pharmacist),
    
    path('pending_pharmacist/view_pending_pharmacist/<int:id>', views.admin_view_pending_pharmacist),

    path('pharmacist/view_pharmacist/<int:id>', views.admin_view_pharmacist),

    path('pharmacist/confirm_delete_pharmacist/<int:id>', views.admin_confirm_delete_pharmacist),

    path('confirm_delete_pharmacist/delete_pharmacist/<int:id>', views.admin_delete_pharmacist),

# All Laboratorist
    path('admin_dash/laboratorist/', views.admin_all_laboratorist),
    
    path('admin_dash/pending_laboratorist/', views.admin_all_pending_laboratorist),
    
    path('pending_laboratorist/approved_laboratorist/<int:user_id>', views.admin_approve_laboratorist),
    
    path('pending_laboratorist/view_pending_laboratorist/<int:id>', views.admin_view_pending_laboratorist),

    path('laboratorist/view_laboratorist/<int:id>', views.admin_view_laboratorist),

    path('laboratorist/confirm_delete_laboratorist/<int:id>', views.admin_confirm_delete_laboratorist),

    path('confirm_delete_laboratorist/delete_laboratorist/<int:id>', views.admin_delete_laboratorist),

# All Accountant
    path('admin_dash/accountant/', views.admin_all_accountant),
    
    path('admin_dash/pending_accountant/', views.admin_all_pending_accountant),
    
    path('pending_accountant/approved_accountant/<int:user_id>', views.admin_approve_accountant),
    
    path('pending_accountant/view_pending_accountant/<int:id>', views.admin_view_pending_accountant),

    path('accountant/view_accountant/<int:id>', views.admin_view_accountant),

    path('accountant/confirm_delete_accountant/<int:id>', views.admin_confirm_delete_accountant),

    path('confirm_delete_accountant/delete_accountant/<int:id>', views.admin_delete_accountant),

# All Receptionist
    path('admin_dash/receptionist/', views.admin_all_receptionist),
    
    path('admin_dash/pending_receptionist/', views.admin_all_pending_receptionist),
    
    path('pending_receptionist/approved_receptionist/<int:user_id>', views.admin_approve_receptionist),
    
    path('pending_receptionist/view_pending_receptionist/<int:id>', views.admin_view_pending_receptionist),

    path('receptionist/view_receptionist/<int:id>', views.admin_view_receptionist),

    path('receptionist/confirm_delete_receptionist/<int:id>', views.admin_confirm_delete_receptionist),

    path('confirm_delete_receptionist/delete_receptionist/<int:id>', views.admin_delete_receptionist),

# All Appointment
    path('admin_dash/appointment/', views.admin_all_appointment),

    path('admin_all_appointment/admin_view_appointment/<int:id>', views.admin_view_appointment),

    path('admin_all_appointment/confirm_delete_appointment/<int:id>', views.admin_confirm_delete_appointment),

    path('confirm_delete_appointment/delete_appointment/<int:id>', views.admin_delete_appointment),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
