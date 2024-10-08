### pudu sdk 文檔中的函式 ###
import requests
import json
import pandas as pd


def add_device(device_id, deviceSecret, region):
    params = {
        "deviceId": device_id,
        "deviceSecret": deviceSecret,
        "region": region
    }
    web = requests.post("http://127.0.0.1:9050/api/add/device", json=params)
    return web.text


def delete_device(device_id):
    params = {
        "deviceId": device_id,
    }
    web = requests.post("http://127.0.0.1:9050/api/delete/device", json=params)
    return web.text


def rename_device(device_id):
    params = {
        "name": "",
        "deviceId": device_id,
    }
    web = requests.post("http://127.0.0.1:9050/api/device/name", json=params)
    return web.text


def get_all_devices():
    web = requests.get(url="http://127.0.0.1:9050/api/devices")
    return web.text


def get_bound_robot_group(device_id):
    web = requests.get(
        url="http://127.0.0.1:9050/api/robot/groups?device="+device_id)
    return web.text


def get_robots_in_a_group(device_id, group_id):
    web = requests.get(
        url="http://127.0.0.1:9050/api/robots?device="+device_id+"&group_id="+group_id)
    return web.text


def obtain_robot_destination_on_map(device_id, robot_id):
    web = requests.get(url="http://127.0.0.1:9050/api/destinations?device=" +
                       device_id+"&robot_id="+robot_id+"&page_size=200&page_index=1")
    result = json.loads(web.text)
    # print(result)
    destList = []
    # print(result)
    if "data" in result:
        destList_total = pd.DataFrame(result['data']['destinations'])
        for i in range(0, len(result['data']['destinations'])):
            destList.append(result['data']['destinations'][i]['name'])
        return destList_total, destList
    else:
        return "未連接機器人"


def register_notification_address():
    return ("")


def query_status_of_robots_in_a_group(device_id, group_id):
    params = {
        "deviceId": device_id,
        "groupId": group_id,
    }
    web = requests.post("http://127.0.0.1:9050/api/robot/state", json=params)
    return web.text


def get_status_of_robots_in_a_group(device_id, group_id):
    web = requests.get("http://127.0.0.1:9050/api/robot/state?device_id=" +
                       device_id+"&group_id="+group_id+"&timeout=10&count=5")
    robot_group = json.loads(web.text)
    return robot_group


def obtain_status_of_robot(device_id, robot_id):
    web = requests.get(
        "http://127.0.0.1:9050/api/robot/status?device_id="+device_id+"&robot_id="+robot_id)
    now_state = json.loads(web.text)
    now_state = web.text
    return now_state


def call_robot_from_a_destination_on_map(device_id, robot_id, dest, destList_total):
    type_name = destList_total.loc[destList_total['name']
                                   == dest]['type'].values[0]
    params = {
        "deviceId": device_id,
        "robotId": robot_id,
        "destination": {
            "name": dest,
            "type": type_name
        }
    }
    web = requests.post(
        url="http://127.0.0.1:9050/api/robot/call", json=params)


def cancel_task_from_a_destination_on_map(device_id, robot_id, dest, destList_total):
    type_name = destList_total.loc[destList_total['name']
                                   == dest]['type'].values[0]
    params = {
        "deviceId": device_id,
        "robotId": robot_id,
        "destination": {
            "name": dest,
            "type": type_name
        }
    }
    web = requests.post(
        url="http://127.0.0.1:9050/api/robot/cancel/call", json=params)


def send_delivery_task_to_robot():
    return ("")


def send_operation_command_to_robot():
    return ("")


def get_robot_map(device_id, robot_id):
    web = requests.get(
        "http://127.0.0.1:9050/api/robot/map?device_id="+device_id+"&robot_id="+robot_id)
    result = json.loads(web.text)
    global mapList, source
    mapList = pd.DataFrame(result['data']['map']['elements'])
    source = mapList[mapList["type"] == "source"]


def start_a_custom_calling_task():
    return ("")


def cancel_custom_calling_task():
    return ("")


def send_custom_display_content():
    return ("")


def custom_call_completion_instruction():
    return ("")
