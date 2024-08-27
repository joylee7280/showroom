### 控制邏輯函式 ###
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from datetime import datetime
from showroom_app.models import pudu_robot, reeman_robot
from django.contrib import auth
from showroom_app.reeman_function import *
from showroom_app.pudu_function import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# pudu 機器人參數
device_id = "1709533220727"
group_id = "Z8Qp8N4sjgZyshhuJLmdz"
deviceSecret = "deviceSecret"
region = "ap-southeast-1"
robot_type = ""
robot_id = ""
name = ""
# 控制進入頁面 index.html


@csrf_exempt  # 每個函式前都要加
def index(request):
    global name, robot_id, robot_type, host
    pudu_robot_list = pudu_robot.objects.all()  # 取出資料庫中所有 pudu 的機器人
    reeman_robot_list = reeman_robot.objects.all()  # 取出資料庫中所有 reeman 的機器人
    print(pudu_robot_list)
    print(reeman_robot_list)
    # if request.method == "POST":  # 當使用者按下某個機器人（即發出 post）
    #     if "type" in request.POST.keys():
    #         if request.POST["type"] == "pudu":  # 若是 pudu
    #             destList_total, dest_list = obtain_robot_destination_on_map(
    #                 device_id, robot_id)
    #             robot_type = request.POST["type"]  # 存 robot_type
    #             name = request.POST["robot"]  # 存 name
    #             robot_id = pudu_robot.objects.get(
    #                 name=name).robotid  # 存 robot_id
    #         elif request.POST["type"] == "reeman":  # 若是 reeman
    #             robot_type = request.POST["type"]  # 存 robot_type
    #             name = request.POST["robot"]  # 存 name
    #             robotlist = get_robotlist(get_token())
    #             host = robotlist[reeman_robot.objects.get(
    #                 name=name).host_name]  # 獲得此機器人的專屬 id
    #             host = host+".ros.rmbot.cn"  # 在 reeman 機器人中的 host 要是專屬 id + .ros.rmbot.cn
    return render(request, 'index.html', locals())  # 對應到 index.html

# 控制單一 robot 頁面


@csrf_exempt
def robot(request):
    pudu_robot_list = pudu_robot.objects.all()
    reeman_robot_list = reeman_robot.objects.all()
    global name, robot_id, robot_type, host, destList_total, dest_list
    ### 放在這裡才會一開始顯示 ###
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
        # 取得狀態
        if "get" in request.POST.keys():
            if robot_type == "pudu":
                now_state = obtain_status_of_robot(device_id, robot_id)
                now_state = json.loads(now_state)
                if "data" not in now_state:
                    return HttpResponse("未連接機器人")
                else:
                    return JsonResponse(now_state["data"], safe=False)
            elif robot_type == "reeman":
                power, chargeStage = get_power(host)
                robotState = get_nav(host)
                robotPose = get_pose(host)
                now_state = {"robotState": robotState, "robotPower": power,
                             "chargeStage": chargeStage, "robotPose": robotPose}
                return JsonResponse(now_state, safe=False)
        # 地圖
        if "map" in request.POST.keys():
            if robot_type == "pudu":
                if (obtain_robot_destination_on_map(device_id, robot_id) == "未連接機器人"):
                    return HttpResponse("未連接機器人")
                else:
                    destList_total, dest_list = obtain_robot_destination_on_map(
                        device_id, robot_id)
                    print("!!!!!!!!!!!!!")
                    print(dest_list)
                    print("!!!!!!!!!!!!!")
                    dest_list_as_json = json.dumps(
                        dest_list, ensure_ascii=False)
                    return HttpResponse(dest_list_as_json, 'application/json')
            elif robot_type == "reeman":
                destList_total, dest_list = get_position(host)
        # 圖片
        if "image" in request.POST.keys():
            path = "/static/Image/"+name+".png"
            print(path)
            return HttpResponse(path)
        # 命令：抵達目的、充電、返航
        if "order" in request.POST.keys():
            if robot_type == "pudu":
                dest = pudu_robot.objects.get(name=name).waitpoint
                call_robot_from_a_destination_on_map(
                    device_id, robot_id, dest, destList_total)
            elif robot_type == "reeman":
                dest = reeman_robot.objects.get(name=name).waitpoint
                post_destname(dest)
            if request.POST["order"] == "go":
                dest = request.POST["dest"]
                if robot_type == "pudu":
                    call_robot_from_a_destination_on_map(
                        device_id, robot_id, dest, destList_total)
                elif robot_type == "reeman":
                    post_destname(dest)
            elif request.POST["order"] == "cancel":
                dest = request.POST["dest"]
                if robot_type == "pudu":
                    cancel_task_from_a_destination_on_map(
                        device_id, robot_id, dest, destList_total)
                elif robot_type == "reeman":
                    post_cancel_nav(host)
            elif request.POST["order"] == "goback":
                if robot_type == "pudu":
                    dest = pudu_robot.objects.get(name=name).waitpoint
                    call_robot_from_a_destination_on_map(
                        device_id, robot_id, dest, destList_total)
                elif robot_type == "reeman":
                    dest = reeman_robot.objects.get(name=name).waitpoint
                    post_cancel_nav(host)
            elif request.POST["order"] == "charge":
                if robot_type == "pudu":
                    dest = pudu_robot.objects.get(name=name).chargepoint
                    call_robot_from_a_destination_on_map(
                        device_id, robot_id, dest, destList_total)
                elif robot_type == "reeman":
                    dest = reeman_robot.objects.get(name=name).chargepoint
                    post_cancel_nav(host)
    return render(request, 'robot.html', locals())


@csrf_exempt
def pudu(request):
    pudu_robot_list = pudu_robot.objects.all()
    if request.method == "POST":
        robot_group = get_status_of_robots_in_a_group(device_id, group_id)
        # 顯示 destList_total
        if "order" in request.POST.keys():
            if request.POST["order"] == "charge":
                for i in range(len(robot_group["data"]["state"])):
                    robot_id = robot_group["data"]["state"][i]["robotId"]
                    destList_total, dest_list = obtain_robot_destination_on_map(
                        device_id, robot_id)
                    dest = pudu_robot.objects.get(robotid=robot_id).chargepoint
                    call_robot_from_a_destination_on_map(
                        device_id, robot_id, dest, destList_total)
            if request.POST["order"] == "goback":
                for i in range(len(robot_group["data"]["state"])):
                    robot_id = robot_group["data"]["state"][i]["robotId"]
                    dest = pudu_robot.objects.get(robotid=robot_id).waitpoint
                    destList_total, dest_list = obtain_robot_destination_on_map(
                        device_id, robot_id)
                    call_robot_from_a_destination_on_map(
                        device_id, robot_id, dest, destList_total)
    return render(request, 'pudu.html', locals())


@csrf_exempt
def reeman(request):
    reeman_robot_list = reeman_robot.objects.all()
    if request.method == "POST":
        robotlist = get_robotlist(get_token())
        # 顯示 destList_total
        if "order" in request.POST.keys():
            if request.POST["order"] == "charge":
                for i in range(len(robotlist)):
                    host = robotlist+".ros.rmbot.cn"
                    destList_total, dest_list = get_position(host)
                    dest = "充電站"
                    post_destname(dest)
            if request.POST["order"] == "goback":
                for i in robotlist.values:
                    host = i+".ros.rmbot.cn"
                    destList_total, dest_list = get_position(host)
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
    return render(request, 'listone.html', locals())


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
    return render(request, 'listall.html', locals())


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        uName = request.POST.get('uName')  # login.html 傳來的變數
        uPass = request.POST.get('uPass')  # login.html 傳來的變數
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
