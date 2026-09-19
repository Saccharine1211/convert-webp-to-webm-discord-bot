# WebP to WebM Discord Bot

A Discord bot that automatically converts uploaded animated WebP files into WebM videos and replies with the converted file. Conversion starts when a message contains a `.webp` attachment; there are no bot commands.

## Requirements

- Python 3
- `discord.py`
- MoviePy 1.x
- `imageio`
- `numpy`
- FFmpeg
- WebP tools including `webpmux`
- A Discord bot application and token

Install the Python dependencies:

```bash
pip install "moviepy<2" discord.py imageio numpy
```

## Discord setup

1. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Enable **Message Content Intent**.
3. Invite the bot with permission to view channels, read message history, send messages, and attach files.

## Configuration

The current source contains `client.run('TOKEN')`. Replace it with your bot token, but do not commit a real token to Git. If a token is exposed, regenerate it immediately.

Update the `webpmux` executable path in `get_webp_info()` to match your system. FFmpeg and `webpmux` must be available before starting the bot.

## Running

```bash
python bot_github.py
```

Upload an animated `.webp` file in a channel the bot can access. The bot should reply with `output.webm`.

## Limitations

- Only attachment URLs ending exactly in `.webp` are recognized.
- Temporary files use fixed names (`temp.webp` and `output.webm`) and are not cleaned up.
- Concurrent conversions may overwrite each other.
- Conversion errors are printed locally rather than reported in Discord.
- No dependency lockfile, tests, or license are included.
