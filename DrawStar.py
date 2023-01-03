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
    
    #Clean Command Queued
    dType.SetQueuedCmdClear(api)
    
    #Async Motion Params Setting
    dType.SetHOMEParams(api, 200, 0, 200, 100, isQueued = 1) # x, y, z, r
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1) # velocity[4], acceleration[4]
    dType.SetPTPCommonParams(api, 120, 120, isQueued = 1) # velocityRatio(속도율), accelerationRation(가속율)
    
    #Async Home
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    Home_x = 200
    Home_y = 0

    r = 50
    arr = [[0 for col in range(2)] for row in range(5)]

    arr[0][0] = r * math.cos(math.radians(-126)) 
    arr[0][1] = r * math.sin(math.radians(-126)) 

    arr[1][0] = 0 
    arr[1][1] = r * math.sin(math.radians(90)) 

    arr[2][0] = r * math.cos(math.radians(-54)) 
    arr[2][1] = r * math.sin(math.radians(-54)) 

    arr[3][0] = r * math.cos(math.radians(162)) 
    arr[3][1] = r * math.sin(math.radians(162)) 

    arr[4][0] = r * math.cos(math.radians(18)) 
    arr[4][1] = r * math.sin(math.radians(18))
    
    #Async PTP Motion
    for i in range(0, 6):

        if i == 5:
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
