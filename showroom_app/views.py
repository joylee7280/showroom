from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from datetime import datetime
from showroom_app.models import student
from django.contrib import auth
from showroom_app.reeman_function import *
from showroom_app.pudu_function import *
from django.views.decorators.csrf import csrf_exempt

device_id = "1709533220727"
group_id = "Z8Qp8N4sjgZyshhuJLmdz"
deviceSecret = "deviceSecret"
region = "ap-southeast-1"
# Create your views here.
def home(request):
    return HttpResponse("Home page")

@csrf_exempt
def index(request):
    pageTitle="子網頁繼承"
    mainTitle="段落標題"
    mainContent="段落內文"
    # artitle1={"aTitle":"文章標題","aContent":"文章1內文"}
    # artitle2={"aTitle":"文章標題","aContent":"文章2內文"}
    # artitles=[artitle1, artitle2]
    return render(request, 'index.html', locals())


@csrf_exempt
def robot(request):
    if request.method == "POST":
        if "get" in request.POST.keys():
            now_state = obtain_status_of_robot(device_id,robot_id)
            now_state = json.loads(now_state)
            return JsonResponse(now_state, safe=False)
        if "order" in request.POST.keys():
            dest = request.POST["dest"]
            if robot_type == "pudu":
                print("pudu")
                # call_robot_from_a_destination_on_map(device_id,robot_id,dest,destList_total)
            elif robot_type == "reeman":
                print("reeman")
                # post_destname(dest)
            if request.POST["order"] == "go":
                if robot_type == "pudu":
                    call_robot_from_a_destination_on_map(device_id,robot_id,dest,destList_total)
                elif robot_type == "reeman":
                    post_destname(dest)
            elif request.POST["order"] == "cancel":
                if robot_type == "pudu":
                    cancel_task_from_a_destination_on_map(device_id,robot_id,dest,destList_total)
                elif robot_type == "reeman":
                    post_cancel_nav(host)
    return render(request, 'robot.html', locals())

@csrf_exempt
def bella(request):
    global name,robot_id,robot_type,dest_list,robot_id,destList_total
    name = "bella"
    robot_id = "08e9f6cf6c56"
    robot_type = "pudu"
    destList_total,dest_list = obtain_robot_destination_on_map(device_id,robot_id)
    return render(request, 'robot.html', globals())

@csrf_exempt
def hola(request):
    global name,robot_id,robot_type,dest_list,robot_id,destList_total
    name = "hola"
    robot_id = "08e9f6cf6eee"
    robot_type = "pudu"
    destList_total,dest_list = obtain_robot_destination_on_map(device_id,robot_id)
    return render(request, 'robot.html', globals())

@csrf_exempt
def pudubot(request):
    global name,robot_id,robot_type,dest_list,robot_id,destList_total
    name = "pudubot2"
    robot_id = "b4edd5756f42"
    robot_type = "pudu"
    destList_total,dest_list = obtain_robot_destination_on_map(device_id,robot_id)
    return render(request, 'robot.html', globals())

@csrf_exempt
def boat(request):
    global name,robot_id,robot_type,dest_list,robot_id,destList_total,host
    robotlist = get_robotlist(get_token())
    print(".............")
    print(type(robotlist))
    name = "boat"
    robot_id = "08e9f6cf6c56"
    robot_type = "reeman"
    host = robotlist['台北辦公室 | 大狗']+".ros.rmbot.cn"
    get_position(host)
    destList_total,dest_list = get_position(host)
    return render(request, 'robot.html', locals())

@csrf_exempt
def dog(request):
    global name,robot_id,robot_type,dest_list,robot_id,destList_total,host
    robotlist = get_robotlist(get_token())
    name = "dog"
    robot_id = "08e9f6cf6c56"
    robot_type = "reeman"
    host = robotlist['台北辦公室 | 大狗']+".ros.rmbot.cn"
    destList_total,dest_list = get_position(host)
    return render(request, 'robot.html', locals())

@csrf_exempt
def hiname(request, username):
    return HttpResponse("Hi "+username)

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
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