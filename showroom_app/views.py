from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from datetime import datetime
from showroom_app.models import pudu_robot,reeman_robot
from django.contrib import auth
from showroom_app.reeman_function import *
from showroom_app.pudu_function import *
from django.views.decorators.csrf import csrf_exempt

device_id = "1709533220727"
group_id = "Z8Qp8N4sjgZyshhuJLmdz"
deviceSecret = "deviceSecret"
region = "ap-southeast-1"
# Create your views here.

@csrf_exempt
def index(request):
    global name,robot_id,robot_type,host
    pudu_robot_list = pudu_robot.objects.all()
    reeman_robot_list = reeman_robot.objects.all()
    print(pudu_robot_list)
    print(reeman_robot_list)
    if request.method == "POST":
        # 哪個機器人
        if "type" in request.POST.keys():
            if request.POST["type"] == "pudu":
                robot_type = request.POST["type"]
                name = request.POST["robot"]
                robot_id = pudu_robot.objects.get(name=name).robotid
            elif request.POST["type"] == "reeman":
                robot_type = request.POST["type"]
                name = request.POST["robot"]
                robotlist = get_robotlist(get_token())
                host = robotlist[reeman_robot.objects.get(name=name).host_name]
                host = host+".ros.rmbot.cn"
    return render(request, 'index.html', locals())

@csrf_exempt
def robot(request):
    pudu_robot_list = pudu_robot.objects.all()
    reeman_robot_list = reeman_robot.objects.all()
    global name,robot_id,robot_type,host
    if robot_type == "pudu":
        destList_total,dest_list = obtain_robot_destination_on_map(device_id,robot_id)
    elif robot_type == "reeman":
        destList_total,dest_list = get_position(host)
    robot_name = name
    if request.method == "POST":
        # 哪個機器人
        if "type" in request.POST.keys():
            if request.POST["type"] == "pudu":
                robot_type = request.POST["type"]
                name = request.POST["robot"]
                robot_id = pudu_robot.objects.get(name=name).robotid
                destList_total,dest_list = obtain_robot_destination_on_map(device_id,robot_id)
                print(dest_list)
            elif request.POST["type"] == "reeman":
                robot_type = request.POST["type"]
                name = request.POST["robot"]
                robotlist = get_robotlist(get_token())
                host = robotlist[reeman_robot.objects.get(name=name).host_name]
                host = host+".ros.rmbot.cn"
                destList_total,dest_list = get_position(host)
                print(dest_list)
            robot_name = name
        # 取得狀態
        if "get" in request.POST.keys():
            if robot_type == "pudu":
                now_state = obtain_status_of_robot(device_id,robot_id)
                now_state = json.loads(now_state)
                return JsonResponse(now_state["data"], safe=False)
            elif robot_type == "reeman":
                power,chargeStage = get_power(host)
                robotState = get_nav(host)
                robotPose = get_pose(host)
                now_state = {"robotState":robotState,"robotPower":power,"chargeStage":chargeStage,"robotPose":robotPose}
                return JsonResponse(now_state, safe=False)
        # 圖片
        if "image" in request.POST.keys():
            path = "/static/Image/"+name+".png"
            print(path)
            return HttpResponse(path)
        # 命令：抵達目的、充電、返航
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
def pudu(request):
    al = pudu_robot.objects.all()
    print(al)
    if request.method == "POST":
        robot_group = get_status_of_robots_in_a_group(device_id,group_id)
        # 顯示 destList_total
        if "order" in request.POST.keys():
            if request.POST["order"] == "charge":
                for i in range(len(robot_group["data"]["state"])):
                    robot_id = robot_group["data"]["state"][i]["robotId"]
                    destList_total,dest_list = obtain_robot_destination_on_map(device_id,robot_id)
                    #寫死哪台機器是哪個待機點
                    if robot_id == "08e9f6cf6c56":
                        dest = "喵喵充電"
                    elif robot_id == "08e9f6cf6eee":
                        dest = "拉拉充電"
                    call_robot_from_a_destination_on_map(device_id,robot_id,dest,destList_total)
            if request.POST["order"] == "goback":
                for i in range(len(robot_group["data"]["state"])):
                    robot_id = robot_group["data"]["state"][i]["robotId"]
                    if robot_id == "08e9f6cf6c56":
                        dest = "喵喵待機"
                    elif robot_id == "08e9f6cf6eee":
                        dest = "拉拉待機"
                    destList_total,dest_list = obtain_robot_destination_on_map(device_id,robot_id)
                    call_robot_from_a_destination_on_map(device_id,robot_id,dest,destList_total)
    return render(request, 'pudu.html', locals())
    
@csrf_exempt
def reeman(request):
    if request.method == "POST":
        robotlist = get_robotlist(get_token())
        # 顯示 destList_total
        if "order" in request.POST.keys():
            if request.POST["order"] == "charge":
                for i in range(len(robotlist)):
                    host = robotlist+".ros.rmbot.cn"
                    destList_total,dest_list = get_position(host)
                    dest = "充電站"
                    post_destname(dest)
            if request.POST["order"] == "goback":
                for i in robotlist.values:
                    host = i+".ros.rmbot.cn"
                    destList_total,dest_list = get_position(host)
                    dest = "充電站"
                    post_destname(dest)
    return render(request, 'pudu.html', locals())

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