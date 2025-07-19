import pygame
import time
import threading
import datetime

# --- 設定 ---


volume1 = 0.4  #
volume2 = 0.7  #
volume3 = 1.0

sound1_path = "sound/pink_noise_cutoff_0.005.wav"
sound2_path = "sound/1-04 海馬成長痛.mp3"
sound3_path = "sound/kiki.wav"

time1 = "07:00"  # ホワイトノイズを止める
time2 = "07:05"  # アラーム開始


#-----------------------------------------------------
def parse_future_datetime(target_time_str):

    now = datetime.datetime.now()
    target_time = datetime.datetime.strptime(target_time_str, "%H:%M").time()
    target = datetime.datetime.combine( now.date(), target_time)

    """日をまたいでる判定"""
    if target <= now and (now - target).total_seconds() > 12 * 3600:
        target += datetime.timedelta(days=1)
    return target

def wait_until(target_datetime):
    while datetime.datetime.now() < target_datetime:
        time.sleep(10)


# ------
def play_loop(path, volume):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play(loops=-1)  # ループ
    print(f"[{datetime.datetime.now().time()}] 再生開始：{path}")

def stop_all():
    pygame.mixer.stop()
    print(f"[{datetime.datetime.now().time()}] 再生停止")

def play_once(path, volume):
    if path == "":
        return
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()
    print(f"[{datetime.datetime.now().time()}] アラーム開始：{path}")
    time.sleep(sound.get_length())

# ------------------------------------------------------
def main():
    pygame.mixer.init()
    
    dt1 = parse_future_datetime(time1)
    dt2 = parse_future_datetime(time2)

    print(f"現在時刻：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"sound1 will stop ：{dt1}")
    print(f"sound2 will start：{dt2}")

    #--------------------------
    # start sound 1
    #--------------------------
    loop_thread = threading.Thread(target=play_loop, args=(sound1_path, volume1))
    loop_thread.start()
    wait_until(dt1)
    stop_all()

    #--------------------------
    # silent
    #--------------------------
    wait_until(dt2)

    #--------------------------
    # start sound 2
    #--------------------------
    play_once(sound2_path, volume2)

    #--------------------------
    # start sound 3
    #--------------------------
    time.sleep(30)
    play_once(sound3_path, volume3)

if __name__ == "__main__":
    main()
