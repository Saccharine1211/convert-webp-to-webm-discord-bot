# WebP to WebM Discord Bot

Discord 메시지에 첨부된 애니메이션 `.webp` 파일을 WebM 동영상으로 변환해 원본 메시지에 답장하는 봇입니다. 명령어는 없으며, 조건에 맞는 첨부 파일이 올라오면 자동으로 처리합니다.

## 처리 과정

1. 첨부 파일을 `temp.webp`로 저장합니다.
2. `webpmux -info`로 프레임 시간을 읽습니다.
3. `imageio`로 프레임을 읽고 NumPy 배열로 변환합니다.
4. MoviePy 이미지 클립을 생성하고 연결합니다.
5. `libvpx`, `5000k` bitrate로 `output.webm`을 생성합니다.
6. 변환 파일을 원본 메시지에 답장으로 업로드합니다.

## 요구 사항

- Python 3
- `discord.py`
- MoviePy 1.x
- `imageio`
- `numpy`
- FFmpeg
- WebP Tools의 `webpmux`
- Discord 봇 애플리케이션과 토큰

소스가 `moviepy.editor`를 사용하므로 MoviePy 1.x 계열을 권장합니다.

```bash
pip install "moviepy<2" discord.py imageio numpy
```

## Discord 설정

1. [Discord Developer Portal](https://discord.com/developers/applications)에서 애플리케이션과 봇을 만듭니다.
2. Bot 설정에서 **Message Content Intent**를 활성화합니다.
3. 봇을 서버에 초대하고 채널 보기, 메시지 기록 읽기, 메시지 보내기, 파일 첨부 권한을 부여합니다.

## 설정

현재 소스는 다음처럼 토큰을 직접 전달합니다.

```python
client.run('TOKEN')
```

실제 토큰을 Git에 커밋하지 마세요. 노출되었다면 Developer Portal에서 즉시 재발급해야 합니다. 현재 코드는 환경 변수나 설정 파일을 읽지 않습니다.

`get_webp_info()`의 `webpmux` 경로도 실제 실행 파일 경로로 수정해야 합니다. FFmpeg와 `webpmux`가 실행 가능한지 확인하세요.

## 실행

```bash
python bot_github.py
```

봇이 접속한 뒤 접근 가능한 채널에 애니메이션 `.webp`를 업로드하면 `output.webm`으로 답장합니다.

## 제한 사항과 위험 요소

- URL이 `.webp`로 정확히 끝나는 첨부만 감지하며 대소문자를 구분합니다.
- 실제 MIME 타입이나 파일 내용을 검증하지 않습니다.
- 고정 파일명(`temp.webp`, `output.webm`)을 사용해 동시 변환 시 서로 덮어쓸 수 있습니다.
- 임시 파일을 자동 삭제하지 않습니다.
- 모든 프레임을 메모리에 올리므로 큰 파일은 메모리를 많이 사용할 수 있습니다.
- 가변 프레임 시간을 보존하지 않고 평균 FPS 하나로 변환합니다.
- 변환 오류를 Discord 사용자에게 전달하지 않고 로컬에만 출력합니다.
- 파일 크기·프레임 수 제한, 테스트, lockfile, 라이선스가 없습니다.

## 파일 구조

```text
bot_github.py
README.md
.gitattributes
```

공개 서버에서 사용하기 전 입력 크기 제한과 작업별 임시 디렉터리를 추가하는 것을 권장합니다.

## 라이선스

저장소에 라이선스가 명시되어 있지 않습니다.
