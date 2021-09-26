from pyrogram import Client, filters
from pytgcalls import PyTgCalls, PyLogs, StreamType

app = Client("tgcall")
api_id = '387279'
api_hash = '4003b48448432acc32a9052af27d4a58'
pytgcalls = PyTgCalls(app, log_mode=PyLogs.verbose)

pytgcalls.join_group_call(
        -1001359252145,
        '/home/tomyang/temp/music/Adele - 21/A1 - Rolling In The Deep.flac',
        48000,
        pytgcalls.get_cache_peer(),
        StreamType().live_stream,
)
