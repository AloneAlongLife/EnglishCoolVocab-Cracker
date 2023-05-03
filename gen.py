from utils import get_data, get_f_data, get_screenshot, start, stop, swipe, tap, update_data, update_f_data
from match_template import ident_image
from modify import run_modify

from time import sleep, time
from urllib.parse import quote_plus, unquote

import xml.etree.ElementTree as ET

from cv2 import imencode
from orjson import loads, dumps

def gen(target_level: int, pets: str, fruit: int) -> bytes:
    timer = time()
    stop()
    get_data()

    fruit_num = run_modify(target_level - 1, pets)
    fruit = fruit if fruit else fruit_num
    update_data()

    get_f_data()

    with open("com.EnglishCool.Vocab.v2.playerprefs.xml") as xml_file:
        raw_data = xml_file.read()
    raw_str = ET.fromstring(raw_data).find("string[@name='data']").text

    base_data = ["0"] * 15
    base_data[target_level - 1] = str(fruit)

    data = loads(unquote(raw_str))
    data["Currency"]["seed"] = "0"
    data["Currency"]["fruit"] = base_data
    new_str = quote_plus(dumps(data).decode("utf-8"))

    with open("com.EnglishCool.Vocab.v2.playerprefs.xml", mode="w") as xml_file:
        xml_file.write(raw_data.replace(raw_str, new_str))

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

    return imencode(".png", screen_shot[770:890, 300:780])[1].tobytes()
