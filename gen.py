from utils import get_data, get_f_data, get_screenshot, start, stop, swipe, tap, update_data, update_f_data
from match_template import ident_image
from modify import run_modify

from time import sleep, time

from cv2 import imencode

def gen(target_level: int, pets: str, fruit: int, bg: int) -> tuple[int, bytes]:
    timer = time()
    stop()
    get_data()
    get_f_data()

    fruit = run_modify(target_level - 1, pets, fruit, bg)
    
    update_data()
    update_f_data()

    start()

    timeout = time()
    while not ident_image(get_screenshot(), "t1.png", y_range=(1670, 1920)) and time() - timeout < 60:
        sleep(0.5)
    if time() - timeout > 60:
        raise TimeoutError("Setting Timeout")
    tap(930, 1800)
    sleep(0.5)
    swipe(540, 1900, 0, -1820, 100)
    sleep(0.5)
    tap(660, 560)
    sleep(0.5)
    tap(540, 1220)
    timeout = time()
    while not ident_image(screen_shot := get_screenshot(), "t2.png", y_range=(900, 1490)) and time() - timeout < 30:
        sleep(0.5)
    if time() - timeout > 60:
        raise TimeoutError("Setting Timeout")
    print(f"Finish {time() - timer}s")
    stop()

    return fruit, imencode(".png", screen_shot[770:890, 300:780])[1].tobytes()
