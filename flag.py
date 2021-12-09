import DobotDllType as dType
import socket
import threading
import time

# 定义机械臂状态， 用键盘存储
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

# 加载机械臂动态链接库
api = dType.load()

# 初始化机械臂
def Dobot():
    # 连接机械臂
    state = dType.ConnectDobot(api, "", 115200)[0]
    # 打印机械臂连接状态
    print("Connect status:", CON_STR[state])

    # 设置机械臂末端为吸盘
    dType.SetEndEffectorParams(api, 59.7, 0, 0, isQueued=0)
    # 设置机械臂PTP运动模式参数(门型运动时抬升高度为60，最大高度为80)
    dType.SetPTPJumpParams(api, 60, 80, isQueued=0)
    # 设置PTP运动速度百分比和加速度百分比，默认为100
    dType.SetPTPCommonParams(api, 32, 32, isQueued=0)

    # 初始化清空机械臂指令
    dType.SetQueuedCmdClear(api)
    # 开始执行队列指令
    dType.SetQueuedCmdStartExec(api)

    # 机械臂初始位置
    dType.SetPTPCmd(api, 1, 150, -150, 50, 0, isQueued=1)
    print("starting...")

# 来回搬运单个方块函数
def move(x, y, z):
    print("机械臂从A点移动到B点")
    # 移动到A点
    dType.SetPTPCmd(api, 0, x, y, z, 0, isQueued=1)
    # 打开气泵
    dType.SetEndEffectorSuctionCup(api, 1, 1, isQueued=1)
    # 移动到B点
    dType.SetPTPCmd(api, 0, x, y, z, 0, isQueued=1)
    # 关闭气泵
    dType.SetEndEffectorSuctionCup(api, 0, 0, isQueued=1)
    time.sleep(2)   # 延时2s
    print("机械臂从B点移动到A点")

def server():
    server = socket.socket()
    server.bind(("192.168.0.101", 6969))   #绑定要监听的端口
    server.listen()   #监听
    print('waiting...')
    flag, _ = server.accept()   #等待电话打进来
    print('success')

    data = flag.recv(1024)   #接收消息
    str1 = str(data, encoding='utf-8')
    list = str1.split(',')

    server.close()
    return list[0], list[1], list[2]

def test():
    x, y, z = server()

    print(x)
    print(y)
    print(z)

hello = threading.Thread(target=test)
hello.start()

