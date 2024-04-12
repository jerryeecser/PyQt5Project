import sys
from pathlib import Path
import json
py_idl_path = str(Path(__file__).parents[2].resolve() / "py_idl")
if py_idl_path not in sys.path:
    sys.path.append(py_idl_path)


import time

from srv.infra.power.efusecontrol_pb2 import *
from google.protobuf.json_format import MessageToJson
from niotest_soa import *

set_log_level(NrpcTraceLevel.kInfo)


service_name = "srv.infra.power.EfuseControl:ZONE_FT_LITE"
client = NrpcClientProxy("efuse-tester", service_name)
client.connect(5000)

for _ in range(10):
    if client.get_connection_state() == NrpcConnectionState.kConnected:
        print(f"Success to connect service {service_name!r}.")
        break

    print("Wait for connecting service...")
    time.sleep(1)
else:
    print(
        f"Fail to connect service {service_name!r}, current connection state is {client.get_connection_state()!r}"
    )
    exit(1)

# Subscribe ControlFL_BaiscEfuseSts_Msg
sts_msg = ControlBasicEfuseSts()
#sts_msg.efusests.add().efuseid=131328
#sts_msg.efusests.add().efuseid=131329
#sts_msg.efusests.add().efuseid=131330
#sts_msg.efusests.add().efuseid=131331
#sts_msg.efusests.add().efuseid=131332
#sts_msg.efusests.add().efuseid=131333
#sts_msg.efusests.add().efuseid=131334
#sts_msg.efusests.add().efuseid=131335

def sts_msg_callback(data: bytes):
    sts_msg.ParseFromString(data)

    print(status_timer(),"=========== Receive via rpc_id 101 ===========")
    QQW101=(MessageToJson(sts_msg, including_default_value_fields=True, sort_keys=True))

    data = json.loads(QQW101)
    # print(data)
    '''
    data["efusests"]结构:
    [
        {"efuseid": 1, "basicefusests": "OK", "efusesafetystatus": "Safe"},
        {"efuseid": 2, "basicefusests": "Failed", "efusesafetystatus": "Unsafe"},
        {"efuseid": 3, "basicefusests": "OK", "efusesafetystatus": "Safe"}
    ]
    efuse_id结构:
    [1, 2, 3, ......]
    '''
    efuse_id = [item["efuseid"] for item in data["efusests"]] 
    EFUSE_STS = [item["basicefusests"] for item in data["efusests"]]
    efuse_safe = [item["efusesafetystatus"] for item in data["efusests"]]
    lege = len(efuse_id)
    for i in range(0, lege):
        print("\033[92m" + "efuseid:" + "\033[0m", efuse_id[i], "\033[92m" + "    Efuse_sts:" + "\033[0m", EFUSE_STS[i]
                     , "\033[92m" + "   Efuse_safety:" + "\033[0m", efuse_safe[i])


client.subscribe(101, sts_msg_callback)


def status_timer():
    Status_time = time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time()))
    return Status_time

# 102

sts_msg_102 = ControlBasicEfuseDiagSts()

def sts_msg_102_callback(data: bytes):
    sts_msg_102.ParseFromString(data)

    print(
        status_timer(),"=========== Receive  via rpc_id 102 ==========="
    )
    QQW= (
        MessageToJson(sts_msg_102, including_default_value_fields=True, sort_keys=True)
    )
    data = json.loads(QQW)
    # print(data)
    efuse_id = [item["efuseid"] for item in data["basicefusediagstatus"]]
    EFUSE_STS = [item["basicefusediagsts"] for item in data["basicefusediagstatus"]]
    lege = len(efuse_id)
    for i in range(0, lege):
        print("\033[92m" + "efuseid:" + "\033[0m", efuse_id[i], "\033[92m" + "        Efuse_sts:" + "\033[0m", EFUSE_STS[i])


client.subscribe(102, sts_msg_102_callback)

###103
sts_msg_103 = ControlBasicEfuseSelftestSts()

def sts_msg_103_callback(data: bytes):
    sts_msg_103.ParseFromString(data)

    print(
        status_timer(),"=========== Receive  via rpc_id 103 ==========="
    )
    QQW1O3=(
        MessageToJson(sts_msg_103, including_default_value_fields=True, sort_keys=True)
    )
    data = json.loads(QQW1O3)
    efuse_id = [item["efuseid"] for item in data["basicefuseselfteststs"]]
    selftest_sts = [item["efuseselfteststs"] for item in data["basicefuseselfteststs"]]
    lege = len(efuse_id)
    for i in range(0,lege):
        print("\033[92m"+"efuseid:"+"\033[0m",efuse_id[i],"\033[92m"+"       selftest_sts:"+"\033[0m",selftest_sts[i])


client.subscribe(103, sts_msg_103_callback)

###109
sts_msg_107 = ControlBasicEfuseCurrentVoltage()

def sts_msg_107_callback(data: bytes):
    sts_msg_107.ParseFromString(data)

    print(
        status_timer(),"=========== Receive  via rpc_id 107 ==========="
    )
    CC=(
        MessageToJson(sts_msg_107, including_default_value_fields=True, sort_keys=True)
    )
    data=json.loads(CC)
    #print(data)
    efuse_id= [item["efuseid"] for item in data["efuseCurrentVoltageSig"]]
    voltages = [item["efusevoltage"] for item in data["efuseCurrentVoltageSig"]]
    current = [item["efusecurrent"] for item in data["efuseCurrentVoltageSig"]]
    lege=len(efuse_id)
    for i in range(0,lege):
        print("\033[92m"+"efuseid:"+"\033[0m",efuse_id[i],"\033[92m"+"        Volt:"+"\033[0m",voltages[i],"\033[92m"+" Current:"+"\033[0m",current[i])

client.subscribe(107, sts_msg_107_callback)

while True:
	time.sleep(5)
