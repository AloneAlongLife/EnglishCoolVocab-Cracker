from config import TOKEN
from gen import gen

from asyncio import CancelledError, Queue, sleep as asleep, get_running_loop
from datetime import datetime
from io import BytesIO
from os import getpid, system
from time import time
from traceback import format_exc

from discord import ApplicationContext, Bot, Embed, File, Interaction, Option

# intents = Intents.default()
# intents.message_content = True
client = Bot()

task_queue = Queue()

PETS = [
    "片語龜",
    "拼字龜",
    "詞性龜",
    "猜拳龜",
    "流行語龜",
    "農夫龜",
    "肥料龜",
    "媽媽龜",
    "時間龜",
    "神龜",
    "無"
]
LEVELS = [
    "果園 1",
    "果園 2",
    "果園 3",
    "果園 4",
    "果園 5",
    "果園 6",
    "果園 7",
    "果園 8",
    "果園 9",
    "果園 10",
    "多益",
    "托福",
    "雅斯",
    "流行語",
    "片語",
]

options = [
    Option(
        int,
        name="target_level",
        description="目標果園",
        default=6,
        min_value=1,
        max_value=15,
    ),
    Option(
        str,
        name="pets",
        description="要加入的烏龜 請輸入0-9(0-片語龜 1-拼字龜 2-詞性龜 3-猜拳龜 4-流行語龜 5-農夫龜 6-肥料龜 7-媽媽龜 8-時間龜 9-神龜)的字串(如: 0179)",
        default="",
        max_length=10,
    ),
    Option(
        int,
        name="fruits",
        description="果實數量",
        require=False,
        min_value=0,
    )
]


async def run_task():
    try:
        loop = get_running_loop()
        target_level: int
        pets: str
        response: Interaction
        embed: Embed
        while True:
            if task_queue.empty():
                await asleep(0.5)
                continue
            target_level, pets, fruits, response, embed = await task_queue.get()
            embed.colour = 0xff8800
            embed.title = "備份碼生成中..."
            embed.description = f"備份碼生成中，請等待約30秒。"

            message = await response.edit_original_response(
                embed=embed,
            )

            try:
                timer = time()
                img = await loop.run_in_executor(None, gen, target_level, pets, fruits)
                img_io = BytesIO(img)

                embed.colour = 0x00ff00
                embed.title = "備份碼生成完成"
                embed.description = f"備份碼生成完成!\n花費時間: `{format(time() - timer, '.2f')}s`"

                embed.add_field(name="使用方法", value="\n".join([
                    "1.啟動單字庫。",
                    "2.點擊右下角\"更多\"。",
                    "3.往下滑至\"裝置轉移\"，點擊\"取回資料\"。",
                    "4.輸入以下圖片中之備份密碼。"
                ]), inline=False)

                embed.add_field(
                    name="目標果園", value=LEVELS[target_level - 1], inline=False)
                embed.add_field(name="烏龜", value="\n".join(
                    map(lambda i: PETS[int(i)], set(pets) or {10, })), inline=False)

                message = await message.edit(
                    embed=embed,
                    file=File(img_io, "code.png")
                )
                embed.set_image(url=message.attachments[0].url)
                await message.edit(
                    embed=embed,
                    attachments=[]
                )
            except CancelledError:
                return
            except:
                embed.colour = 0xff0000
                embed.title = "備份碼生成失敗"
                embed.description = f"備份碼生成失敗!\n```{format_exc()}```"

                await message.edit(
                    embed=embed
                )
    except CancelledError:
        return


@client.event
async def on_ready():
    print(f"{client.user.display_name} Start!")
    client.loop.create_task(run_task())


@client.slash_command(
    name="get_code",
    description="取得備份碼",
    options=options,
)
async def get_code(
    ctx: ApplicationContext,
    target_level: int = 6,
    pets: str = "",
    fruits: int = -1
):
    print(f"User: {ctx.author.display_name}")
    embed = Embed(
        colour=0x0066ff,
        title="請求等待中...",
        description="等待貯列中其他請求完成...",
        timestamp=datetime.now()
    )
    embed.set_author(name="單字庫終結者", icon_url=client.user.display_avatar.url)
    embed.set_image(url="https://i.imgur.com/EUste4G.png")
    embed.add_field(name="使用者", value=ctx.author.mention, inline=False)
    embed.set_footer(text=f"由 {ctx.author.display_name} 生成",
                     icon_url=ctx.author.display_avatar.url)
    response = await ctx.respond(
        embed=embed,
    )
    fruits = None if fruits == -1 else fruits
    await task_queue.put((target_level, pets, fruits, response, embed))


@client.slash_command(
    name="update"
)
async def update(
    ctx: ApplicationContext
):
    if ctx.author.id != 302774180611358720:
        return
    system("git pull")
    system("start start.cmd")
    system(f"taskkill /f /pid {getpid()}")

if __name__ == "__main__":
    client.run(TOKEN)
