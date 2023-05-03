import sqlite3
from datetime import date, datetime, timedelta

PETS_FRUIT = [
    1000,
    1000,
    1000,
    10,
    1000,
    5000,
    10000,
    15000,
    20000,
    50000
]

def run_modify(target_level: int, pets: str) -> int:
    db = sqlite3.connect("wordcool_user.db")
    cursor = db.cursor()

    dt = [1, 2, 4, 8, 14]
    e = [1, 2, 4, 8, 16]
    farms = [0] * 5 + list(range(1, 96))
    start_date = date(2023, 3, 1)
    start_datetime = datetime.combine(start_date, datetime.now().time())

    target_date: date = datetime.now().date()

    if type(target_date) == str:
        target_date = datetime.strptime(target_date, "%Y%m%d").date()
    if type(target_level) == str:
        target_level = int(target_level) - 1

    total = (target_date - start_date).days + 1

    # 登入紀錄
    if cursor.execute("SELECT * FROM User WHERE key='loginDays'").fetchone():
        cursor.execute("UPDATE 'User' SET 'value'=? WHERE key='loginDays'", ("1" * total,))
    else:
        cursor.execute("INSERT INTO 'User' ('key', 'value') VALUES ('loginDays', ?)", ("1" * total,))

    # 註冊日期
    if cursor.execute("SELECT * FROM User WHERE key='startDate'").fetchone():
        cursor.execute("UPDATE 'User' SET 'value'='2023/03/01' WHERE key='startDate'")
    else:
        cursor.execute("INSERT INTO 'User' ('key', 'value') VALUES ('startDate', '2023/03/01')")

    # 顯示教學
    if cursor.execute("SELECT * FROM User WHERE key='hasShowStartIntro'").fetchone():
        cursor.execute("UPDATE 'User' SET 'value'='1' WHERE key='hasShowStartIntro'")
    else:
        cursor.execute("INSERT INTO 'User' ('key', 'value') VALUES ('hasShowStartIntro', '1')")

    # 起始果園
    if cursor.execute("SELECT * FROM User WHERE key='startOrchardID'").fetchone():
        cursor.execute("UPDATE 'User' SET 'value'=? WHERE key='startOrchardID'", (target_level,))
    else:
        cursor.execute("INSERT INTO 'User' ('key', 'value') VALUES ('startOrchardID', ?)", (target_level,))

    # 果園背景
    bg = ["0"] * 15
    bg[target_level] = "1"
    bg = "".join(bg)
    if cursor.execute("SELECT * FROM User WHERE key='orchardSceneBG'").fetchone():
        cursor.execute("UPDATE 'User' SET 'value'=? WHERE key='orchardSceneBG'", (bg,))
    else:
        cursor.execute("INSERT INTO 'User' ('key', 'value') VALUES ('orchardSceneBG', ?)", (bg,))

    # 烏龜紀錄
    cursor.execute("DELETE FROM PetDataRecord")
    pets = list(map(int, set(pets)))
    for i in pets:
        cursor.execute("""
            INSERT INTO "PetDataRecord"
            ("db_id", "satiety_val", "reduce_timestamp", "play_num", "play_timestamp", "content", "content_timestamp") VALUES
            (?, "24", ?, "0", "0", "", "0")
        """, (target_level * 100 + i, int((datetime.now() + timedelta(days=30)).timestamp())))

    # 種植紀錄
    cursor.execute("DELETE FROM StatsDataRecord")
    cursor.execute("DELETE FROM PlotDataRecord")
    cursor.execute("DELETE FROM LearningRecord")
    nts = lambda: int(datetime.now().timestamp())

    total_seed = 0
    fruit = 0
    for day in range(total):
        seed, water, blue = 0, 0, 0
        ts = lambda x: int((start_datetime + timedelta(days=day+x)).timestamp())
        for i, farm in enumerate(farms):
            offset = day - farm
            if offset == 0:
                seed += 1
                total_seed += 1
                cursor.execute("""
                    INSERT INTO "PlotDataRecord"
                    ("db_id", "plot_id", "status", "level", "next_water_timestamp", "next_fruit_timestamp", "has_fruit", "speed_up", "fruit_show_timestamp") VALUES
                    (?, ?, "1", "1", ?, "0", "0", "0", "0")
                """, (target_level * 100 + i, i, ts(1)))

                for void in range(10):
                    cursor.execute("""
                        INSERT INTO "LearningRecord"
                        ("id", "is_toggled", "correct_answer", "incorrect_answer", "unsure_answer", "learn_time") VALUES
                        (?, '0', '0', '0', '0', ?);
                    """, (target_level * 1000 + i * 10 + void, nts()))
            elif offset == 30:
                blue += 1
                cursor.execute("""
                    UPDATE "PlotDataRecord"
                    SET status=3, level=7, next_water_timestamp=0
                    WHERE plot_id=?
                """, (i,))
                cursor.execute("""
                    UPDATE "LearningRecord"
                    SET correct_answer=6, learn_time=?
                    WHERE id BETWEEN ? AND ?
                """, (nts(), target_level * 1000 + i * 10, target_level * 1000 + i * 10 + 9))
            elif offset in e:
                water += 1
                ind = e.index(offset)
                cursor.execute("""
                    UPDATE "PlotDataRecord"
                    SET level=?, next_water_timestamp=?
                    WHERE plot_id=?
                """, (ind + 2, ts(dt[ind]), i))
                cursor.execute("""
                    UPDATE "LearningRecord"
                    SET correct_answer=?, learn_time=?
                    WHERE id BETWEEN ? AND ?
                """, (ind + 1, nts(), target_level * 1000 + i * 10, target_level * 1000 + i * 10 + 9))
            
            if offset >= 0:
                cursor.execute("""
                    UPDATE "PlotDataRecord"
                    SET next_fruit_timestamp=0, has_fruit=1, fruit_show_timestamp=?
                    WHERE plot_id=?
                """, (int((datetime.now() - timedelta(hours=1)).timestamp()), i))
        fruit += 10 * total_seed
        
        cursor.execute("""
            INSERT INTO "StatsDataRecord"
            ("date_id", "seed_count", "water_count", "review_count", "blue_count", "session_num", "correct_num", "incorrect_num", "unsure_num") VALUES
            (?, ?, ?, "0", ?, ?, ?, "0", "0");
        """, (start_date.strftime("%Y%m%d"), seed, water, blue, seed+water, water * 10))
        start_date += timedelta(days=1)

    db.commit()
    cursor.close()
    db.close()

    return fruit - sum(map(lambda pet: PETS_FRUIT[pet], pets))