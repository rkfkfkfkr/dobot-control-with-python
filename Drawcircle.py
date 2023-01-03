import threading
import DobotDllType as dType
import math

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound", 
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#dll을 메모리에 읽어들여 CDLL 인스턴스 가져오기
#Load Dll and get the CDLL object
api = dType.load()

#dobot과의 연결을 설정
#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):

    circle_dot_num = input("circle dot num") #점의 갯수 입력
    circle_r = input("r? : ") # 반지름 입력
    
    #Clean Command Queued
    dType.SetQueuedCmdClear(api)
    
    #Async Motion Params Setting
    dType.SetHOMEParams(api, 200, 200, 200, 100, isQueued = 1) # x, y, z, r
    dType.SetPTPJointParams(api, 100, 200, 200, 200, 200, 200, 200, 200, isQueued = 1) # velocity[4], acceleration[4]
    dType.SetPTPCommonParams(api, 30, 30, isQueued = 1) # velocityRatio(속도율), accelerationRation(가속율)
    
    #Async Home
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    dot_num = int(circle_dot_num) # 형변환
    r = float(circle_r)

    degree = 360/dot_num # 점들 사이의 각도 계산

    arr = [[0 for col in range(2)] for row in range(dot_num)] # 좌표 배열 생성

    for i in range(0, dot_num):
        arr[i][0] = r * math.cos(math.radians(i * degree)) # 각도에 따른 x좌표 생성
        arr[i][1] = r * math.sin(math.radians(i * degree)) # 각도에 따른 y좌표 생성
    
    #Async PTP Motion
    for i in range(0, dot_num): # 좌표계 변환 및 마지막에는 출발 지점으로 돌아오도록 

        if i == dot_num - 1:
            offset_x = -arr[0][1]
            offset_y = arr[0][0]         

        else:
            offset_x = -arr[i][1]
            offset_y = arr[i][0]

        
        
        
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode,200+ offset_x, offset_y, 0, 0, isQueued = 1)[0]

    #Start to Execute Command Queue
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        Curindex = dType.GetQueuedCmdCurrentIndex(api)

        #print(Curindex)
        pose = dType.GetPose(api)
        print( "x: ", pose[0], "y: ", pose[1], "z: ", pose[2])
        print("\n")
        dType.dSleep(100)

    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)

#Disconnect Dobot
dType.DisconnectDobot(api)
