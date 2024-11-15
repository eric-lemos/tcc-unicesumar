from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time, date
from django.db.models.functions import TruncMonth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone 
from .models import *
import locale
import json
import pytz

status = [
    "Agendado", "Ausente", "Cancelado", "Finalizado", "Pendente"
]

states = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

specializations = [
    "Cardiologia", "Cirurgia Geral", "Cirurgia Vascular", "Cirurgia Torácica", 
    "Dermatologia", "Ginecologia", "Infectologia", "Neurologia", "Pediatria", 
    "Oncologia", "Ortopedia", "Psiquiatria", "Radiologia", "Urologia"
]

def notfound(request): 
    return render(request, 'app/dashboard/404.html')

def create_fake_user(usertype, *args):
    last_user_id = int(User.objects.latest('id').id)
    cpf = str(last_user_id + 1).zfill(11)
    crm = str(last_user_id + 1).zfill(6)

    for arg in args:

        user = User.objects.create_user(
            first_name=arg['first_name'], 
            last_name=arg['last_name'], 
            email=arg['email'], 
            username=cpf,
            password='1'
        )

        profile = Profile.objects.create(
            pk=user.pk,
            user=user,
            cpf=cpf,
            genrer=arg['genrer'],
            usertype=usertype
        )

        if usertype == 'doctor':
            return Doctor.objects.create(
                pk=user.pk,
                profile=profile,
                crm=crm,
                crm_state=arg['crm_state'],
                specialization=arg['specialization']
            )

        elif usertype == 'manager':
            return Manager.objects.create(
                pk=user.pk,
                profile=profile
            )
        
        elif usertype == 'patient':
            return Patient.objects.create(
                pk=user.pk,
                profile=profile
            )

def create_fake_data():
    # Patients
    create_fake_user('patient', {
        "first_name": "Amélia", "last_name": "Sabino", "email": "amelia@paciente.com", "genrer": "Feminino"
    })
    create_fake_user('patient', {
        "first_name": "Eduardo", "last_name": "Lemos", "email": "eduardo@paciente.com", "genrer": "Masculino"
    })
    create_fake_user('patient', {
        "first_name": "Eliane", "last_name": "Mathias", "email": "eliane@paciente.com", "genrer": "Feminino"
    })
    create_fake_user('patient', {
        "first_name": "Eric", "last_name": "Cardoso", "email": "eric@paciente.com", "genrer": "Masculino"
    })
    create_fake_user('patient', {
        "first_name": "Fernando", "last_name": "Machado", "email": "fernando@paciente.com", "genrer": "Feminino"
    })
    create_fake_user('patient', {
        "first_name": "Gabriel", "last_name": "Bernardino", "email": "gabriel@paciente.com", "genrer": "Masculino"
    })
    create_fake_user('patient', {
        "first_name": "Leandro", "last_name": "Pereira", "email": "leandro@paciente.com", "genrer": "Masculino"
    })
    create_fake_user('patient', {
        "first_name": "Lucas", "last_name": "Antonioli", "email": "lucas@paciente.com", "genrer": "Masculino"
    })
    create_fake_user('patient', {
        "first_name": "Marco", "last_name": "Aurélio", "email": "marco@paciente.com", "genrer": "Masculino"
    })
    create_fake_user('patient', {
        "first_name": "Verônica", "last_name": "Ventura", "email": "veronica@paciente.com", "genrer": "Feminino"
    })
    create_fake_user('patient', {
        "first_name": "Vicente", "last_name": "Leite", "email": "vicente@paciente.com", "genrer": "Masculino"
    })

    # Doctors
    create_fake_user('doctor', {
        "first_name": "Aretusa", "last_name": "Kruchinski", "email": "aretusa@med.com", "genrer": "Feminino", 
        "crm_state": "RS", "specialization": "Cirurgia Torácica"
    })
    create_fake_user('doctor', {
        "first_name": "Camilla", "last_name": "Victer", "email": "camilla@med.com", "genrer": "Feminino", 
        "crm_state": "SC", "specialization": "Pediatria"
    })
    create_fake_user('doctor', {
        "first_name": "Evelyn", "last_name": "Leite", "email": "evelyn@med.com", "genrer": "Feminino", 
        "crm_state": "SC", "specialization": "Cirurgia Vascular"
    })
    create_fake_user('doctor', {
        "first_name": "Gracy", "last_name": "Pereira", "email": "gracy@med.com", "genrer": "Feminino", 
        "crm_state": "PR", "specialization": "Infectologia"
    })
    create_fake_user('doctor', {
        "first_name": "Guilherme", "last_name": "Leal", "email": "guilherme@med.com", "genrer": "Masculino", 
        "crm_state": "PR", "specialization": "Ortopedia"
    })
    create_fake_user('doctor', {
        "first_name": "Marília", "last_name": "Ribas", "email": "marilia@med.com", "genrer": "Feminino", 
        "crm_state": "SC", "specialization": "Cirurgia Vascular"
    })
    create_fake_user('doctor', {
        "first_name": "Patricia", "last_name": "Moraes", "email": "patricia@med.com", "genrer": "Feminino", 
        "crm_state": "SC", "specialization": "Cirurgia Vascular"
    })

    # Managers
    create_fake_user('manager', {
        "first_name": "Isadora", "last_name": "Santos", "email": "isadora@gestor.com", "genrer": "Feminino"
    })
    create_fake_user('manager', {
        "first_name": "Thiago", "last_name": "Silva", "email": "thiago@gestor.com", "genrer": "Masculino"
    })

# Login
def redirect_login(request):
    return redirect('/login/')

def login(request):
    errors = None

    if request.method == "POST":
        posted_username = request.POST["username"]
        password = request.POST["password"]
        remember = request.POST.get("remember", False)

        try:
            user = User.objects.get(email=posted_username)
            username = user.username
        except User.DoesNotExist:
            username = posted_username
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if remember: request.session.set_expiry(timedelta(days=30))
            else: request.session.set_expiry(0)
            return redirect("dashboard")
        else:
            errors = "Login inválido! Por favor, verifique seu usuário e/ou senha."
    
    else:
        if not Profile.objects.filter(cpf='1').exists():
            user = User.objects.create_user(first_name='Super', last_name='Admin', email='admin@website.com', username='1', password='1')
            profile = Profile.objects.create(pk=user.pk, user=user, cpf='1', genrer='')
            Manager.objects.create(pk=user.pk, profile=profile)
            create_fake_data()

    return render(request, 'app/login/auth.html', {'errors': errors})

def logout(request):
    auth_logout(request)
    return redirect("/login/")

def register(request):
    errors = []
    form_data = []

    if request.method == "POST":
        form_data = request.POST
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        cpf = request.POST['cpf']
        genrer = request.POST['genrer']
        password = request.POST['password']
        rpassword = request.POST['rpassword']

        if Profile.objects.filter(cpf=cpf).exists(): errors.append('Este CPF já foi cadastrado.')
        if password != rpassword: errors.append('As senhas informadas não são iguais.')

        if not errors:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=cpf, password=password)
            profile = Profile.objects.create(user=user, cpf=cpf, genrer=genrer, usertype="patient")
            Patient.objects.create(profile=profile)
            return redirect('/login')
        
    return render(request, 'app/login/register.html', {'form_data': form_data, 'errors': errors})

def forgot_password(request):
    return render(request, 'app/login/forgot.html', {})

# Profile
@login_required(login_url='/login/')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if profile.usertype == 'doctor':
        doctor = Doctor.objects.get(profile=profile)
        context = {
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name,
            "email": profile.user.email,
            "cpf": profile.cpf,
            "specialization": doctor.specialization,
            "crm_state": doctor.crm_state,
            "crm": doctor.crm,
        }
    else:
        context = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "cpf": profile.cpf,
        }
    return render(request, 'app/dashboard/profile.html', {"context": context})


# Dashboard
@login_required(login_url='/login/')
def dashboard(request):
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    
    if request.user.profile.usertype == 'doctor':
        doctor = get_object_or_404(Doctor, pk=request.user.pk)
        confirmedAppointments = Calendar.objects.filter(status='Agendado', doctor=doctor).count()
        canceledAppointments = Calendar.objects.filter(status='Cancelado', doctor=doctor).count()
        pendingAppointments = Calendar.objects.filter(status='Pendente', doctor=doctor).count()
        doneAppointments = Calendar.objects.filter(status='Finalizado', doctor=doctor).count()
        awayAppointments = Calendar.objects.filter(status='Ausente', doctor=doctor).count()
        totalAppointments = Calendar.objects.filter(doctor=doctor).count()
        barChart = (
            Calendar.objects.filter(begin_date__year=date.today().year, doctor=doctor)
            .annotate(month=TruncMonth('begin_date'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )
    elif request.user.profile.usertype == 'patient':
        patient = get_object_or_404(Patient, pk=request.user.pk)
        confirmedAppointments = Calendar.objects.filter(status='Agendado', patient=patient).count()
        canceledAppointments = Calendar.objects.filter(status='Cancelado', patient=patient).count()
        pendingAppointments = Calendar.objects.filter(status='Pendente', patient=patient).count()
        doneAppointments = Calendar.objects.filter(status='Finalizado', patient=patient).count()
        awayAppointments = Calendar.objects.filter(status='Ausente', patient=patient).count()
        totalAppointments = Calendar.objects.filter(patient=patient).count()
        barChart = (
            Calendar.objects.filter(begin_date__year=date.today().year, patient=patient)
            .annotate(month=TruncMonth('begin_date'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )
    else:
        confirmedAppointments = Calendar.objects.filter(status='Agendado').count()
        canceledAppointments = Calendar.objects.filter(status='Cancelado').count()
        pendingAppointments = Calendar.objects.filter(status='Pendente').count()
        doneAppointments = Calendar.objects.filter(status='Finalizado').count()
        awayAppointments = Calendar.objects.filter(status='Ausente').count()
        totalAppointments = Calendar.objects.count()
        barChart = (
            Calendar.objects.filter(begin_date__year=date.today().year)
            .annotate(month=TruncMonth('begin_date'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )

    barChart_list = [{'month': result['month'].strftime('%B').capitalize(), 'total': result['total']} for result in barChart]
    barChart_json = json.dumps(barChart_list, default=str)

    return render(request, 'app/dashboard/index.html', {
        "confirmedAppointments": confirmedAppointments,
        "canceledAppointments": canceledAppointments,
        "pendingAppointments": pendingAppointments,
        "totalAppointments": totalAppointments,
        "doneAppointments": doneAppointments,
        "awayAppointments": awayAppointments,
        "barChart": barChart_json
    })


# Calendar
def gen_protocol():
    now = datetime.now()
    ms = int(now.strftime("%f")) // 1000
    return now.strftime("%Y%m%d%H%M%S") + f"{ms}"

@login_required(login_url='/login/')

def calendar(request):
    if request.user.profile.usertype == 'doctor':
        doctor = get_object_or_404(Doctor, pk=request.user.pk)
        appointments = Calendar.objects.all().filter(status__in=['Agendado', 'Pendente'], doctor=doctor)
        patients, doctors = None, None

    elif request.user.profile.usertype == 'patient':
        patient = get_object_or_404(Patient, pk=request.user.pk)
        appointments = Calendar.objects.all().filter(status__in=['Agendado', 'Pendente'], patient=patient)
        doctors = Doctor.objects.all()
        patients = None

    else:
        appointments = Calendar.objects.all().filter(status__in=['Agendado', 'Pendente'])
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()

    specializations = Doctor.objects.values('specialization').distinct()

    return render(request, 'app/dashboard/calendar.html', {
        'appointments': appointments,
        'doctors': doctors,
        'patients': patients,
        'specializations': specializations
    })

@login_required(login_url='/login/')
def add_calendar(request):
    errors = []
    form_data = []

    if request.method == "POST":
        form_data = request.POST
        user_tz = pytz.timezone('America/Sao_Paulo')
        specialization = request.POST['specialization_select']
        doctor = get_object_or_404(Doctor, id=request.POST['doctor_select'])
        patient = get_object_or_404(Patient, id=request.POST['patient_select'])
        begin_date = user_tz.localize(timezone.datetime.strptime(request.POST['begin_date'], '%Y-%m-%dT%H:%M'))
        end_date = user_tz.localize(timezone.datetime.strptime(request.POST['end_date'], '%Y-%m-%dT%H:%M'))

        appointments = Calendar.objects.filter(doctor=doctor, begin_date=begin_date, end_date=end_date, status="Agendado")
        if appointments.exists(): errors.append('Este horário já está agendado para outro paciente.')
        if (end_date - begin_date) != timedelta(minutes=30): errors.append('O agendamento deve ter duração de 30 minutos.')
        if begin_date.weekday() >= 5 or end_date.weekday() >= 5: errors.append('Agendamentos só são permitidos de segunda à sexta-feira.')
        if not (time(8, 0) <= begin_date.time() <= time(18, 0)): errors.append('A hora inicial deve estar entre 08:00 e 18:00.')
        if not (time(8, 0) <= end_date.time() <= time(18, 0)): errors.append('A hora final deve estar entre 08:00 e 18:00.')
        if begin_date < timezone.now(): errors.append('A hora inicial deve ser em um momento futuro.')
        if end_date < timezone.now(): errors.append('A hora final deve ser em um momento futuro.')
        if begin_date >= end_date: errors.append('A hora inicial deve ser antes da hora final.')
        
        if errors: return JsonResponse({"form_data": form_data, "errors": errors})
        else:
            Calendar.objects.create(protocol=gen_protocol(), doctor=doctor, patient=patient, specialization=specialization, begin_date=begin_date, end_date=end_date, status="Pendente", moderator=None).save()
            return JsonResponse({})

@login_required(login_url='/login/')    
def get_calendar(request, pk):
    if request.method == 'GET':
        appointments = get_object_or_404(Calendar, pk=pk)
        return JsonResponse({"appointments": appointments.to_dict()})

@login_required(login_url='/login/')
def edit_calendar(request, pk):
    errors = []

    if request.method == "POST":
        user_tz = pytz.timezone('America/Sao_Paulo')
        calendar = get_object_or_404(Calendar, pk=pk)

        calendar.specialization = request.POST['specialization_select_edit']
        calendar.doctor = get_object_or_404(Doctor, id=request.POST['doctor_select_edit'])
        calendar.patient = get_object_or_404(Patient, id=request.POST['patient_select_edit'])
        calendar.begin_date = user_tz.localize(timezone.datetime.strptime(request.POST['begin_date_edit'], '%Y-%m-%dT%H:%M'))
        calendar.end_date = user_tz.localize(timezone.datetime.strptime(request.POST['end_date_edit'], '%Y-%m-%dT%H:%M'))

        appointments = Calendar.objects.filter(doctor=calendar.doctor, begin_date=calendar.begin_date, end_date=calendar.end_date, status="Agendado")
        if appointments.exists(): errors.append('Este horário já está agendado para outro paciente.')
        if (calendar.end_date - calendar.begin_date) != timedelta(minutes=30): errors.append('O agendamento deve ter duração de 30 minutos.')
        if calendar.begin_date.weekday() >= 5 or calendar.end_date.weekday() >= 5: errors.append('Agendamentos só são permitidos de segunda à sexta-feira.')
        if not (time(8, 0) <= calendar.begin_date.time() <= time(18, 0)): errors.append('A hora inicial deve estar entre 08:00 e 18:00.')
        if not (time(8, 0) <= calendar.end_date.time() <= time(18, 0)): errors.append('A hora final deve estar entre 08:00 e 18:00.')
        if calendar.begin_date < timezone.now(): errors.append('A hora inicial deve ser em um momento futuro.')
        if calendar.end_date < timezone.now(): errors.append('A hora final deve ser em um momento futuro.')
        if calendar.begin_date >= calendar.end_date: errors.append('A hora inicial deve ser antes da hora final.')
        
        if errors: return JsonResponse({"errors": errors})
        else:
            calendar.save()
            return JsonResponse({})

@login_required(login_url='/login/')
def approve_calendar(request, pk):
    appointment = get_object_or_404(Calendar, id=pk)
    appointment.moderator = get_object_or_404(Manager, id=request.POST['moderator'])
    appointment.status = 'Agendado'
    appointment.save()
    return redirect('calendar')

@login_required(login_url='/login/')
def cancel_calendar(request, pk):
    appointment = get_object_or_404(Calendar, id=pk)
    appointment.status = 'Cancelado'
    appointment.save()
    return redirect('calendar')

@login_required(login_url='/login/')
def away_calendar(request, pk):
    appointment = get_object_or_404(Calendar, id=pk)
    appointment.status = 'Ausente'
    appointment.save()
    return redirect('calendar')

@login_required(login_url='/login/')
def done_calendar(request, pk):
    appointment = get_object_or_404(Calendar, id=pk)
    appointment.status = 'Finalizado'
    appointment.save()
    return redirect('calendar')


# Managers
@login_required(login_url='/login/')
def managers(request):
    managers = Manager.objects.all()
    return render(request, 'app/dashboard/managers.html', {'managers': managers})

@login_required(login_url='/login/')
def add_manager(request):
    errors = []
    form_data = []

    if request.method == "POST":
        form_data = request.POST
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        rpassword = request.POST['rpassword']
        genrer = request.POST['genrer']
        email = request.POST['email']
        cpf = request.POST['cpf']
        
        if Profile.objects.filter(cpf=cpf).exists(): errors.append('Este CPF já foi cadastrado.')
        if password != rpassword: errors.append('As senhas informadas não são iguais.')
        
        if errors:
            return JsonResponse({"form_data": form_data, "errors": errors})
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=cpf, password=password)
            profile = Profile.objects.create(pk=user.pk, user=user, cpf=cpf, genrer=genrer, usertype="manager")
            Manager.objects.create(pk=user.pk, profile=profile)
            return JsonResponse({})
        
@login_required(login_url='/login/')
def get_manager(request, pk):
    if request.method == 'GET':
        manager = get_object_or_404(Manager, pk=pk)
        return JsonResponse({"manager": manager.to_dict()})

@login_required(login_url='/login/')
def edit_manager(request, pk):
    errors = []

    if request.method == 'POST':
        manager = get_object_or_404(Manager, pk=pk)
        if request.method == "POST":
            manager.profile.user.first_name = request.POST['first_name']
            manager.profile.user.last_name = request.POST['last_name']
            manager.profile.user.email = request.POST['email']
            manager.profile.genrer = request.POST['genrer']

            if manager.profile.cpf != request.POST['cpf'] and Profile.objects.filter(cpf=request.POST['cpf']).exists():
                errors.append('Este CPF já foi cadastrado.')
            else:
                manager.profile.cpf = request.POST['cpf']
                manager.profile.user.username = request.POST['cpf']

            if request.POST['password']:
                if request.POST['password'] == request.POST['rpassword']:
                    manager.profile.user.set_password(request.POST['password'])
                else:
                    errors.append('As senhas informadas não são iguais.')

            if errors: return JsonResponse({"errors": errors})
            else: 
                manager.profile.user.save()
                manager.profile.save()
                manager.save()
                return JsonResponse({})

@login_required(login_url='/login/')
def del_manager(request, pk):
    manager = get_object_or_404(Manager, pk=pk)
    manager.profile.user.delete()
    manager.profile.delete()
    manager.delete()

    if not Profile.objects.filter(pk=pk).exists():
        return JsonResponse({'was_deleted': True})
    else: JsonResponse({'was_deleted': False})


# Doctors
@login_required(login_url='/login/')
def doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'app/dashboard/doctors.html', {'doctors': doctors, "states": states, "specializations": specializations})

@login_required(login_url='/login/')
def add_doctor(request):
    errors = []
    form_data = []

    if request.method == "POST":
        form_data = request.POST
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        rpassword = request.POST['rpassword']
        genrer = request.POST['genrer']
        email = request.POST['email']
        cpf = request.POST['cpf']
        crm = request.POST['crm']
        crm_state = request.POST['crm_state']
        specialization = request.POST['specialization']
        
        if Profile.objects.filter(cpf=cpf).exists(): errors.append('Este CPF já foi cadastrado.')
        if password != rpassword: errors.append('As senhas informadas não são iguais.')
        
        if errors:
            return JsonResponse({"states": states, "specializations": specializations, "form_data": form_data, "errors": errors})
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=cpf, password=password)
            profile = Profile.objects.create(pk=user.pk, user=user, cpf=cpf, genrer=genrer, usertype="doctor")
            Doctor.objects.create(pk=user.pk, profile=profile, crm=crm, crm_state=crm_state, specialization=specialization)
            return JsonResponse({})

@login_required(login_url='/login/')
def get_doctor(request, pk):
    if request.method == 'GET':
        doctor = get_object_or_404(Doctor, pk=pk)
        return JsonResponse({"doctor": doctor.to_dict()})

@login_required(login_url='/login/')
def edit_doctor(request, pk):
    errors = []

    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, pk=pk)
        if request.method == "POST":
            doctor.profile.user.first_name = request.POST['first_name']
            doctor.profile.user.last_name = request.POST['last_name' ] 
            doctor.profile.user.email = request.POST['email']
            doctor.profile.genrer = request.POST['genrer']
            doctor.crm = request.POST['crm']
            doctor.crm_state = request.POST['crm_state']
            doctor.specialization = request.POST['specialization']

            if doctor.profile.cpf != request.POST['cpf'] and Profile.objects.filter(cpf=request.POST['cpf']).exists():
                errors.append('Este CPF já foi cadastrado.')
            else:
                doctor.profile.cpf = request.POST['cpf']
                doctor.profile.user.username = request.POST['cpf']

            if request.POST['password']:
                if request.POST['password'] == request.POST['rpassword']:
                    doctor.profile.user.set_password(request.POST['password'])
                else:
                    errors.append('As senhas informadas não são iguais.')

            if errors: return JsonResponse({"errors": errors})
            else: 
                doctor.profile.user.save()
                doctor.profile.save()
                doctor.save()
                return JsonResponse({})
            
@login_required(login_url='/login/')
def del_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.profile.user.delete()
    doctor.profile.delete()
    doctor.delete()

    if not Profile.objects.filter(pk=pk).exists():
        return JsonResponse({'was_deleted': True})
    else: JsonResponse({'was_deleted': False})


# Patients
@login_required(login_url='/login/')
def patients(request):
    patients = Patient.objects.all()
    return render(request, 'app/dashboard/patients.html', {'patients': patients})

@login_required(login_url='/login/')
def add_patient(request):
    errors = []
    form_data = []

    if request.method == "POST":
        form_data = request.POST
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        rpassword = request.POST['rpassword']
        genrer = request.POST['genrer']
        email = request.POST['email']
        cpf = request.POST['cpf']
        
        if Profile.objects.filter(cpf=cpf).exists(): errors.append('Este CPF já foi cadastrado.')
        if password != rpassword: errors.append('As senhas informadas não são iguais.')
        
        if errors:
            return JsonResponse({"form_data": form_data, "errors": errors})
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=cpf, password=password)
            profile = Profile.objects.create(pk=user.pk, user=user, cpf=cpf, genrer=genrer, usertype="patient")
            Patient.objects.create(pk=user.pk, profile=profile)
            return JsonResponse({})
        
@login_required(login_url='/login/')
def get_patient(request, pk):
    if request.method == 'GET':
        patient = get_object_or_404(Patient, pk=pk)
        return JsonResponse({"patient": patient.to_dict()})

@login_required(login_url='/login/')
def edit_patient(request, pk):
    errors = []
    print(request.POST)
    if request.method == 'POST':
        patient = get_object_or_404(Patient, pk=pk)
        if request.method == "POST":
            patient.profile.user.first_name = request.POST['first_name']
            patient.profile.user.last_name = request.POST['last_name']
            patient.profile.user.email = request.POST['email']
            patient.profile.genrer = request.POST['genrer']

            if patient.profile.cpf != request.POST['cpf'] and Profile.objects.filter(cpf=request.POST['cpf']).exists():
                errors.append('Este CPF já foi cadastrado.')
            else:
                patient.profile.cpf = request.POST['cpf']
                patient.profile.user.username = request.POST['cpf']

            if request.POST['password']:
                if request.POST['password'] == request.POST['rpassword']:
                    patient.profile.user.set_password(request.POST['password'])
                else:
                    errors.append('As senhas informadas não são iguais.')

            if errors: return JsonResponse({"errors": errors})
            else: 
                patient.profile.user.save()
                patient.profile.save()
                patient.save()
                return JsonResponse({})

@login_required(login_url='/login/')
def del_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.profile.user.delete()
    patient.profile.delete()
    patient.delete()

    if not Profile.objects.filter(pk=pk).exists():
        return JsonResponse({'was_deleted': True})
    else: JsonResponse({'was_deleted': False})


# History
@login_required(login_url='/login/')
def history(request):
    if request.user.profile.usertype == 'doctor':
        doctor = get_object_or_404(Doctor, pk=request.user.pk)
        appointments = Calendar.objects.all().filter(status__in=['Ausente', 'Cancelado', 'Finalizado'], doctor=doctor)

    elif request.user.profile.usertype == 'patient':
        patient = get_object_or_404(Patient, pk=request.user.pk)
        appointments = Calendar.objects.all().filter(status__in=['Ausente', 'Cancelado', 'Finalizado'], patient=patient)

    else:
        appointments = Calendar.objects.all().filter(status__in=['Ausente', 'Cancelado', 'Finalizado'])

    return render(request, 'app/dashboard/history.html', {'appointments': appointments})