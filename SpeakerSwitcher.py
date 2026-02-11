import subprocess
import time


def get_current_device():
    """현재 기본 재생 장치의 이름을 가져오려고 시도합니다."""
    # nircmd 자체로는 현재 장치 이름을 텍스트로 바로 뱉게 하기 어려우므로
    # 상태 파일(txt)을 임시로 만들어 확인하는 트릭을 씁니다.
    try:
        # 현재 기본 장치 정보를 파일로 저장
        subprocess.run('nircmd sysinfo stdout > sound_info.txt', shell=True)
        with open('sound_info.txt', 'r', encoding='utf-16') as f:
            content = f.read()
            if "Headphone" in content:
                return "Headphone"
            else:
                return "Speaker"
    except:
        # 파일 읽기에 실패하면 기본적으로 Speaker라고 가정
        return "Speaker"


def toggle_audio():
    # 1. 현재 어떤 장치인지 확인 (이 방식이 복잡하면 간단하게 스위치용 파일을 하나 만듭니다)
    # 여기서는 더 확실한 '기록 파일' 방식을 쓰겠습니다.
    state_file = "audio_state.txt"

    if not hasattr(toggle_audio, "current"):
        try:
            with open(state_file, "r") as f:
                last_state = f.read().strip()
        except:
            last_state = "Speaker"

    # 2. 반대 장치로 설정
    if last_state == "Speaker":
        target = "Headphone"
        msg = "🎧 헤드폰(Headphone)으로 전환합니다."
    else:
        target = "Speaker"
        msg = "🔊 스피커(Speaker)로 전환합니다."

    try:
        # nircmd 명령 실행
        subprocess.run(['nircmd', 'setdefaultsounddevice', target], check=True)
        print(msg)

        # 3. 바뀐 상태 저장
        with open(state_file, "w") as f:
            f.write(target)

    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    toggle_audio()
    time.sleep(1.5)  # 메시지를 볼 수 있게 잠시 대기