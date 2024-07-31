from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from datetime import datetime
from showroom_app.models import student
from django.contrib import auth
from showroom_app.reeman_function import *
from showroom_app.pudu_function import *

device_id = "1709533220727"
group_id = "Z8Qp8N4sjgZyshhuJLmdz"
deviceSecret = "deviceSecret"
region = "ap-southeast-1"
# Create your views here.
def home(request):
    return HttpResponse("Home page")

def index(request):
    pageTitle="子網頁繼承"
    mainTitle="段落標題"
    mainContent="段落內文"
    # artitle1={"aTitle":"文章標題","aContent":"文章1內文"}
    # artitle2={"aTitle":"文章標題","aContent":"文章2內文"}
    # artitles=[artitle1, artitle2]
    return render(request, 'index.html', locals())

robot_name = ""
robot_state = ""
robot_power = ""
robot_chargestate = ""
robot_movestate = "移動"


def robot(request):
    # global name,state,power,chargeState,moveState
    name = robot_name
    state = robot_state
    power = robot_power
    chargeState = robot_chargestate
    moveState = robot_movestate
    return render(request, 'robot.html', locals())

def bella(request):
    # global name,state,power,chargeState,moveState
    name = "bella"
    robot_id = "08e9f6cf6c56"
    now_state = obtain_status_of_robot(device_id,robot_id)
    state = now_state['data']['robotState']
    power = now_state['data']['robotPower']
    chargeStage = now_state['data']['chargeStage']
    moveState = now_state['data']['moveState']
    return render(request,'robot.html', locals())

def hola(request):
    # global name,state,power,chargeState,moveState
    name = "拉拉"
    state = robot_state
    power = robot_power
    chargeState = robot_chargestate
    moveState = robot_movestate
    return render(request, 'robot.html', locals())

def pudubot(request):
    # global name,state,power,chargeState,moveState
    name = "歡樂送"
    state = robot_state
    power = robot_power
    chargeState = robot_chargestate
    moveState = robot_movestate
    return render(request, 'robot.html', locals())

def boat(request):
    # global name,state,power,chargeState,moveState
    name = "飛船"
    state = robot_state
    power = robot_power
    chargeState = robot_chargestate
    moveState = robot_movestate
    return render(request, 'robot.html', locals())

def dog(request):
    # global name,state,power,chargeState,moveState
    name = "大狗"
    state = robot_state
    power = robot_power
    chargeState = robot_chargestate
    moveState = robot_movestate
    return render(request, 'robot.html', locals())


def hiname(request, username):
    return HttpResponse("Hi "+username)

def getOneByName(request, username):
    title = "顯示一筆資料"
    # unit = get_object_or_404(student, cName=username)
    try:
        unit = student.objects.get(cName=username)
    except student.DoesNotExist:
        raise Http404("查無此學生")
    except:
        raise Http404("讀取錯誤")
    return render(request, 'listone.html', locals() )

def getAll(request):
    title = "顯示全部資料"
    # students = get_list_or_404(student)
    try:
        students = student.objects.all()
    except student.DoesNotExist:
        raise Http404("查無學生資料")
    except:
        raise Http404("讀取錯誤")
    return render(request, 'listall.html', locals() )

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        uName = request.POST.get('uName') # login.html 傳來的變數
        uPass = request.POST.get('uPass') # login.html 傳來的變數
        # 直接判斷帳密有效性
        # if uName=='Peter' and uPass=='591026':
        #     return HttpResponse("已登入")
        # else:
        #     return redirect('/login/')
        
        # 以 Django 內建的管理者帳密判斷有效性
        user = auth.authenticate(username=uName, password=uPass)
        if user is not None:
            auth.login(request, user)
            return HttpResponse("已登入")
        else:
            return redirect('/login/')