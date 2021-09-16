import concurrent.futures
import ipaddress, re
import subprocess
import socket
from django.shortcuts import render, redirect
from .form import *
from .models import *
from django.contrib.auth.decorators import login_required
import json


# Функция авторизации/регистрации


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register_and_login/register.html', {'user_form': user_form})


# Главная страница сайта


@login_required
def home(request):
    s = netmask.objects.all()

    context = {
        'name': s,
    }
    return render(request, 'home.html', context)


# Функция добавление данных в бд


@login_required
def input_data(request):
    error = ''
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            form.save()
            address = str(request.POST['input']) + '/' + str(request.POST['mask'])
            with concurrent.futures.ThreadPoolExecutor(max_workers=512) as executor:
                for ip in ipaddress.ip_network(address):
                    executor.submit(ping, ip=str(ip))

            return redirect('input_data')
        else:
            error = 'форма заполнена не верно'
    form = NameForm
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'input_data.html', data)


# Функция сканирования списка адресов на наличие пинга


def ping(ip):
    output = subprocess.Popen(["/bin/ping", "-c1", "-w1", str(ip)], stdout=subprocess.PIPE).stdout.read()
    if (str(output).lower()[str(output).rfind('received, ') + 10:str(output).rfind(' packet')]) == '0%':
        f = Local_Scanner.objects.filter(ip=str(ip))
        if not f:
            s = Local_Scanner(ip=str(ip), status='G', delay=str(output).lower()[
                                                            str(output).rfind(' time=') + 6:str(output).rfind(
                                                                ' time=') + 10])
            s.save()
        else:
            f.update(status='G')
            f.update(delay=str(output).lower()[str(output).rfind(' time=') + 6:str(output).rfind(' time=') + 11])


# Функция определения имени хоста


def hostName(ip):
    fields = subprocess.Popen(['grep', str(ip), '/proc/net/arp'], stdout=subprocess.PIPE).stdout.read()
    try:
        r = re.search(r'\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}', fields.decode('UTF 8')).group()
        Local_Scanner.objects.filter(ip=str(ip)).update(mac=r)
    except:
        pass
    try:
        Local_Scanner.objects.filter(ip=ip).update(hostname=str(socket.gethostbyaddr(str(ip))[0]))
        print(str(socket.gethostbyaddr(str(ip))[0]))
    except:
        pass


# Функция определения девайса или ОС


def os(ip):
    sudoPassword = 'd12L03xd'
    cmd1 = subprocess.Popen(['echo', sudoPassword], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S', 'nmap', '-p', '22,23,80,7070',
                             '--version-light', '-O', ip], stdin=cmd1.stdout, stdout=subprocess.PIPE)
    output = cmd2.stdout.read()
    if ' type: switch' in str(output):
        Local_Scanner.objects.filter(ip=ip).update(os="Свитч")
    elif ' type: VoIP ' in str(output):
        if ' details: ' in str(output):
            a = str(output).lower()[str(output).rfind(' details: ') + 10:str(output).find('Network Distance:') - 2]
            Local_Scanner.objects.filter(ip=ip).update(os=a)
    elif ' type: router' in str(output):
        # print('\n'+ip + ' router')
        Local_Scanner.objects.filter(ip=ip).update(os='Роутер')
    elif ' type: printer' in str(output):
        # print('\n'+ip + ' printer')
        Local_Scanner.objects.filter(ip=ip).update(os='Принтер')
    elif ' type: general ' in str(output).lower():
        if ' details: ' in str(output):
            a = str(output).lower()[str(output).rfind(' details: ') + 10:str(output).find('Network Distance:') - 2]
            Local_Scanner.objects.filter(ip=ip).update(os=a)
        elif ' Running: ' in str(output):
            a = str(output).lower()[str(output).rfind(
                'Running: ') + 9:str(output).find('OS CPE:') - 2]
            Local_Scanner.objects.filter(ip=ip).update(os=a)
    elif ' type: ' in str(output):
        if ' details: ' in str(output):
            a = str(output).lower()[str(output).rfind('Running: ') + 9:str(output).find('OS CPE:') - 2]
            Local_Scanner.objects.filter(ip=ip).update(os=a)
        else:
            Local_Scanner.objects.filter(ip=ip).update(os='Прочее')
    else:
        Local_Scanner.objects.filter(ip=ip).update(os='Прочее')


# Функция выведения подсетей


@login_required
def list_info(request):
    s = netmask.objects.all()
    dat = {
        'address': s,
    }
    return render(request, 'list_info.html', dat)


# Функция удаления подсети с адресами


@login_required
def addres_delete(request, mainid):
    if request.method == 'POST':
        if 'delete_address' in request.POST:
            if {mainid}:
                print('POST')
                a = netmask.objects.get(pk=mainid)
                for ip in ipaddress.ip_network(a):
                    Local_Scanner.objects.filter(ip=ip).delete()
                a.delete()
            return redirect('home')


# Функция отображения данных определенной маски или адреса


@login_required
def host_info(request, hostid):
    import time
    start_time = time.time()
    ip_list = []
    if request.method == 'POST':
        if 'global' in request.POST:
            add = str(netmask.objects.get(pk=hostid).input) + '/' + str(netmask.objects.get(pk=hostid).mask)
            with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
                for ip in ipaddress.ip_network(add):
                    executor.submit(ping, ip=str(ip))
                    executor.submit(os, ip=str(ip))
                    executor.submit(hostName, ip=str(ip))
                    # print(ip)

    if request.method == 'GET':
        if 'name' in request.GET:
            add = str(netmask.objects.get(pk=hostid).input) + '/' + str(netmask.objects.get(pk=hostid).mask)
            with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
                for ip in ipaddress.ip_network(add):
                    executor.submit(ping, ip=str(ip))

    add = str(netmask.objects.get(pk=hostid).input) + '/' + str(netmask.objects.get(pk=hostid).mask)
    print(add)
    with concurrent.futures.ThreadPoolExecutor(max_workers=255) as executor:
        for ip in ipaddress.ip_network(add):
            ip_list.append(str(ip))
            executor.submit(fastScan, ip=str(ip))
    ip_list.sort(key=ipaddress.IPv4Network)
    for i in Local_Scanner.objects.all():
        if str(i).split('.')[2:3] == add.split('.')[2:3]:
            Local_Scanner.objects.filter(ip=i).update(net=netmask.objects.filter(id=hostid)[0])
    time = time.time() - start_time
    print(time)
    context = {
        'list_ip': ip_list,
        'list': Local_Scanner.objects.all()
    }
    return render(request, 'host_info.html', context)


# Быстрое сканирование по пингу


@login_required
def fastScan(ip):
    s = subprocess.call(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.DEVNULL)
    if s == 0:
        Local_Scanner.objects.filter(ip=ip).update(status='G')
    elif s == 1:
        Local_Scanner.objects.filter(ip=ip).update(status='R')
    else:
        Local_Scanner.objects.filter(ip=ip).update(status='B')


# Функция групировки и постоянного сканирования


def group(request):
    a = []
    if request.method == 'POST':
        if 'inputval' in request.POST:
            z = str(request.POST['inputval'])
            y = str(request.POST['checkboxes_value'])
            print(z)
            print(y)
            # print(z.split('&'))
            # for i in z.split('&'):
            #     res = re.search(r'\d+.\d+.\d+.\d+', i).group()
            #     print(res)
            # if not groupUp.objects.filter(ip=res):
            #     s = groupUp(ip=res, bool=True)
            #     s.save()
            # else:
            #     groupUp.objects.filter(ip=res).update(bool=True)
            # for i in groupUp.objects.all():
            #     if i != groupUp.objects.filter(ip=res):
            #         groupUp.objects.filter(ip=i).delete()
    data = netmask.objects.all()
    list = []
    # for i in data:
    # model_is_confirm =
    #     if str(i).split('.')[2:3] == data.split('.')[2:3]:
    #         list.append(i)
    context = {
        'block_scan': list,
        'block_info': data,
    }
    # return redirect('home')
    return render(request, 'block_scan.html', context)
