import traceback
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message
from nonebot.log import logger

from .data_source import sources, Source


__help__plugin_name__ = "music"
__des__ = "点歌"
__cmd__ = """
点歌/qq点歌/网易点歌/酷我点歌/酷狗点歌/咪咕点歌/b站点歌 {keyword}
默认为qq点歌
""".strip()
__short_cmd__ = "点歌 {keyword}"
__example__ = """
点歌 万古生香
""".strip()
__usage__ = f"{__des__}\nUsage:\n{__cmd__}\nExample:\n{__example__}"


def create_matchers():
    def create_handler(source: Source) -> T_Handler:
        async def handler(matcher: Matcher, msg: Message = CommandArg()):
            keyword = msg.extract_plain_text().strip()
            if keyword:
                try:
                    res = await source.func(keyword)
                except:
                    logger.warning(traceback.format_exc())
                    await matcher.finish("出错了，请稍后再试")

                if res:
                    await matcher.finish(res)

        return handler

    for source in sources:
        matcher = on_command(
            source.keywords[0],
            aliases=set(source.keywords),
            block=True,
            priority=12,
        )
        matcher.append_handler(create_handler(source))


create_matchers()
