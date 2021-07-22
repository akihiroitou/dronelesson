import time
from dronekit import connect, VehicleMode,LocationGlobalRelative

#機体接続
vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True, timeout=60)

#テレメトリー接続
#vehicle = connect('/dev/ttyS5', wait_ready=True, timeout=60,baud=57600)

# vehicle.home_locationに値が設定されるまで
# downloadを繰り返し実行する
while not vehicle.home_location:
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

    if not vehicle.home_location:
        print("ホームロケーションを待っています…")

# ホームロケーションの取得完了
print("ホームロケーション: %s" % vehicle.home_location)

# arm不可能なモードもしくはセーフティロックがかかっている場合はこの処理でスタックする可能性があります
while not vehicle.is_armable:
    print("初期化中です")
    time.sleep(1)

print("アームします")
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

while not vehicle.armed:
    print("アームを待ってます")
    time.sleep(1)

targetAltude = 100

print("離陸！")
vehicle.simple_takeoff(targetAltude)

while True:
    print("高度:",vehicle.location.global_relative_frame.alt)
    if vehicle.location.global_relative_frame.alt >= targetAltude * 0.95:
        print("目標高度に到達しました")
        break

    time.sleep(1)

print("スピードを3に設定")
vehicle.airspeed = 3

print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(35.4764551,138.7372435, 20)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(60)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
