### reeman sdk 文檔中的函式 ###
import requests
import json
import pandas as pd
# 獲取 token
def get_token():
    params = {
        "account": "hckj",
        "password": "a123456"
    }
    web = requests.post(
        "http://navi.rmbot.cn/openapispring/tokens", json=params)
    result = json.loads(web.text)
    token = result["data"]["result"]["accessToken"]
    # print(token)
    return token
# 獲取此帳號密碼底下都哪些 robot
def get_robotlist(token):
    header = {
        "Authorization": token
    }
    body = {
        "limit": {
            "page": 1,
            "size": 10
        },
        "equal": {
            "matchFeedback": None,
            "laserState": None,
            "matchState": None
        },
        "like": {
            "device": None,
            "remark": None,
            "address": None,
            "version": None
        }

    }
    web = requests.post(
        "http://navi.rmbot.cn/openapispring/ros/devices/find2", headers=header, json=body)
    result = json.loads(web.text)
    global robotlist
    # print(len(result["data"]["data"]))
    robotlist = {}
    for i in range(0, len(result["data"]["data"])):
        robotlist.setdefault(
            result["data"]["data"][i]["remark"], result["data"]["data"][i]["urlId"])
    return robotlist

# 獲取機器人位置


def get_pose(host):
    web = requests.get("http://"+host+"/reeman/pose")
    reeman_pos = json.loads(web.text)
    pos_list = {"x": reeman_pos["x"],
                "y": reeman_pos["y"], "angle": reeman_pos["theta"]}
    return pos_list
# 獲取電源管理狀態


def get_power(host):
    web = requests.get("http://"+host+"/reeman/base_encode")
    power = json.loads(web.text)["battery"]
    charge_result = json.loads(web.text)["chargeFlag"]
    if (charge_result == 1):
        return power, "Idle"
    elif (charge_result == 2):
        return power, "Charging"


def get_position(host):
    web = requests.get("http://"+host+"/reeman/position")
    result = json.loads(web.text)
    global destList_total
    destList_total = pd.DataFrame(result['waypoints'])
    global destList
    destList = []
    for i in range(0, len(result['waypoints'])):
        destList.append(result['waypoints'][i]['name'])
    return destList_total, destList
# 發送目標名稱導航


def post_destname(dest):
    print(dest)
    index = destList_total.loc[destList_total['name'] == dest].index.values[0]
    print(index)
    global reeman_destpose
    reeman_destpose = destList_total.loc[index, "pose"]
    body = {"point": dest}
    web = requests.post("http://"+host+"/cmd/nav_name", json=body)
    print("finish")
# 取消導航


def post_cancel_nav(host):
    web = requests.post("http://"+host+"/cmd/cancel_goal")
    return web.text
# 獲取導航狀態


def get_nav(host):
    web = requests.get("http://"+host+"/reeman/nav_status")
    global nav_status
    print(web.text)
    nav_status = json.loads(web.text)["res"]
    print(nav_status)
    if (nav_status == 1):
        return ("Busy")
    else:
        return ("Free")
# 獲取當前導航版本


def get_version():
    web = requests.get("http://"+host+"/reeman/current_version")
    print(web.text)
    return web.text

# 獲取當前模式


def get_state(host):
    web = requests.get("http://"+host+"/reeman/get_mode")
    print(web.text)
    return web.text

# 獲取機器hostname


def get_hostname():
    web = requests.get("http://"+host+"/reeman/hostname")
    return web.text
# 獲取IMU狀態


def get_imu():
    web = requests.get("http://"+host+"/reeman/imu")
    print(web.text)
    return web.text
# 獲取激光數據


def get_laserdata():
    web = requests.get("http://"+host+"/reeman/laser")
    return web.text

# 獲取當前速度


def get_speed():
    web = requests.get("http://"+host+"/reeman/speed")
    result = json.loads(web.text)
    return result

# 重定位


def post_relocate():
    body = {"x": 1.0, "y": 3, "theta": 0.14}
    web = requests.post("http://"+host+"/cmd/reloc_pose", json=body)
    return web.text

# Navigaion module
# 發送位置坐標導航


def post_destpos():
    body = {"x": 285, "y": 252, "theta": 1.6}
    web = requests.post("http://"+host+"/cmd/nav", json=body)
    return web.text
# 發送固定路線點為名稱導航


def post_pointspath():
    body = {"name": "A"}
    web = requests.post("http://"+host+"/cmd/points_path", json=body)
    return web.text
# 導航充電


def post_nav_charge():
    body = {"type": 0, "point": "充电桩"}
    web = requests.post("http://"+host+"/cmd/charge", json=body)
    return web.text
# 發送多個目標座標導航


def post_nav_list():
    body = {"name1": ["x", "y", "theta"]}, {"name2": ["x", "y", "theta"]}
    web = requests.post("http://"+host+"/cmd/nav_list", json=body)
    return web.text
# 設置導航最大速度


def post_maxspeed():
    body = {"speed": 0.5}
    web = requests.post("http://"+host+"/cmd/max_speed", json=body)
    return web.text
# 獲取導航路徑


def get_nav_path():
    web = requests.get("http://"+host+"/reeman/global_plan")
    return web.text
# 切換建圖模式


def shift_mode():
    body = {"mode": 1}
    web = requests.post("http://"+host+"/cmd/set_mode", json=body)
    return web.text
# 獲取當前地圖


def get_map():
    web = requests.get("http://"+host+"/reeman/map")
    return web.text
# 切換增量建圖模式


def post_setmode():
    body = {"mode": 3}
    web = requests.post("http://"+host+"/cmd/set_mode", json=body)
    return web.text
# 保存地圖


def post_savemap():
    web = requests.post("http://"+host+"/cmd/save_map")
    return web.text
# 獲取當前地圖的名稱


def get_currentmap():
    web = requests.get("http://"+host+"/cmd/current_map")
    return web.text
# 獲取所有地圖列表


def get_historymp():
    web = requests.get("http://"+host+"/cmd/history_map")
    return web.text
# 應用地圖


def post_applymap():
    body = {"name": "地图名称"}
    web = requests.post("http://"+host+"/cmd/apply_map", json=body)
    return web.text
# 導出地圖


def post_exportmap():
    body = {"name": "地图名称"}
    web = requests.post("http://"+host+"/cmd/export_map", json=body)
    return web.text
# 上傳地圖


def post_importmap(data):
    body = {data}
    web = requests.post("http://"+host+"/cmd/import_map", json=body)
    return web.text
# 重命名地圖


def post_renamemap():
    body = {"old_name": "旧名称", "new_name": "新名称"}
    web = requests.post("http://"+host+"/cmd/rename_map", json=body)
    return web.text
# 刪除地圖


def post_deletemap():
    body = {"name": "地图名称"}
    web = requests.post("http://"+host+"/cmd/delete_map", json=body)
    return web.text
# 設置標定位置


def post_position():
    body = {"name": "test", "type": "delivery", "pose":
            {"x": -3.05, "y": 0.41, "theta": 0.56}}
    web = requests.post("http://"+host+"/cmd/position", json=body)
    return web.text
# 刪除標定位置


def delete_postion():
    body = ["test"]
    web = requests.delete("http://"+host+"/cmd/position", json=body)
    return web.text
# 獲取路線


def get_naviroutes():
    web = requests.get("http://"+host+"/reeman/navi_routes")
    return web.text
# 獲取固定路線


def get_pathmodel():
    web = requests.get("http://"+host+"/reeman/path_model")
    return web.text
# 獲取特殊區


def get_specialpolygon():
    web = requests.get("http://"+host+"/reeman/special_polygon")
    return web.text
# 獲取虛擬牆


def get_restrictlayer():
    web = requests.get("http://"+host+"/reeman/restrict_layer")
    return web.text
# 保存虛擬牆


def post_restrict_layer():
    body = {"waypoints": [{"pose": {"point1": {"x": 1.1, "y": 2.2}, "point2":
                                    {"x": 3.3, "y": 4.4}}}]}
    web = requests.post("http://"+host+"/cmd/restrict_layer", json=body)
    return web.text
# 移動


def post_speed():
    body = {"vx": "直行距离-单位米", "vth": "转动角度-单位弧度"}
    web = requests.post("http://locahost/cmd/speed", json=body)
    return web.text
# 升級


def post_upgrade(file):
    data = {}
    data.append('file', file)
    body = {data}
    web = requests.post("http://"+host+"/upload/upgrade", json=body)
    return web.text
# 打開供電


def post_lock():
    web = requests.post("http://locahost/cmd/lock")
    return web.text
# 關閉供電


def post_unclock():
    web = requests.post("http://locahost/cmd/unlock")
    return web.text
# 頂升


def post_hydraulic_up():
    web = requests.post("http://"+host+"/cmd/hydraulic_up")
    return web.text
# 下降


def post_hydraulic_down():
    web = requests.post("http://"+host+"/cmd/hydraulic_down")
    return web.text
