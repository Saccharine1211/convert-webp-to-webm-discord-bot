import discord
import subprocess
from moviepy.editor import *
import imageio
import os
import numpy as np

def get_webp_info(file_path):
    # 현재 스크립트의 위치를 가져옴
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 상대 경로를 사용하여 webpmux의 경로를 만듦
    webpmux_path = os.path.join(current_dir, 'your webpmux.exe path')
    # webpmux 명령을 실행하여 파일 정보를 가져옴
    result = subprocess.run([webpmux_path, '-info', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running webpmux: {result.stderr.decode('utf-8')}")
        return None
    return result.stdout.decode('utf-8')

def extract_durations(info):
    lines = info.split('\n')
    durations = []
    # 각 프레임의 지속 시간을 추출
    for line in lines[1:]:
        if 'no' in line:
            parts = line.split()
            duration = int(parts[6])
            durations.append(duration)
    return durations

def calculate_fps(durations):
    # 전체 지속 시간 계산
    total_duration = sum(durations)
    # 평균 지속 시간 계산
    average_duration = total_duration / len(durations) if durations else 0
    # 초당 프레임 수 계산
    fps = 1000 / average_duration if average_duration > 0 else 0
    return fps

# 의도를 초기화
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 메시지 첨부 파일을 검사
    for attachment in message.attachments:
        if attachment.url.endswith('.webp'):
            # 임시 webp 파일로 저장
            webp_file = 'temp.webp'
            await attachment.save(webp_file)

            # webp 파일 정보 추출
            info = get_webp_info(webp_file)
            if info:
                durations = extract_durations(info)
                fps = calculate_fps(durations)
                frame_count = len(durations)

                # 이미지 읽기 및 클립 생성
                reader = imageio.get_reader(webp_file)
                frames = [np.array(frame) for frame in reader]
                clips = [ImageClip(frame, duration=1/fps) for frame in frames[:frame_count]]

                # 클립을 연결하여 최종 동영상 파일 생성
                final_clip = concatenate_videoclips(clips, method="compose")
                webm_file = 'output.webm'
                final_clip.write_videofile(webm_file, codec="libvpx", fps=fps, bitrate="5000k")

                # 결과 파일을 디스코드 채널에 전송
                await message.reply(file=discord.File(webm_file), mention_author=True)

# 봇 실행 (토큰을 적절한 값으로 변경하세요)
client.run('your token')
