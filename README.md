# CPU Defense

<img width="630" height="480" alt="start_scene_background" src="https://github.com/user-attachments/assets/f45134b6-005b-4824-b200-42d38476d006" />


컴퓨터 내부 세계를 배경으로 CPU를 바이러스로부터 지켜내는 탑다운 2D 디펜스 게임입니다.
플레이어는 다양한 보안 터렛을 설치하여 웨이브마다 몰려오는 바이러스를 막아내야 합니다.

## 게임 소개

장르: 2D 타워 디펜스</br>
플랫폼: PC (Windows, Linux)</br>
그래픽 스타일: 64×64 픽셀 아트</br>
핵심 목표: CPU까지 도달하기 전에 적절한 위치에 적절한 터렛을 배치하여 모든 바이러스를 처치하면 됩니다.

## 게임 플레이 방식

* 마우스 클릭으로 터렛 설치
* 라운드 시작(Start Round) 버튼을 누르면 웨이브 시작
* 바이러스가 CPU에 도달하면 체력이 감소, 체력이 0이 될 시 게임 오버.
* 모든 웨이브를 막아내면 승리
* 각 터렛은 고유한 공격 범위 / 공격 속도 / 공격력을 가짐.

### 주요 터렛

| 터렛 종류    | 이미지 | 설명                                    |
| ------------ | -------- | --------------------------------------- |
| 보안 패치 캐논 | <img width="64" height="64" alt="cannon" src="https://github.com/user-attachments/assets/30d9b9f9-f600-4d9a-8048-fc80e3c0f277" /> |가장 일반적인 보안 터렛입니다. 보안 패치를 적에게 발사합니다. |
| 코어 디버거 | <img width="64" height="64" alt="core_debugger" src="https://github.com/user-attachments/assets/3d3629bd-7ec7-47d1-9486-155cd6f57b6c" /> | 공격 범위가 넓고 공격력이 강하지만 공격 속도는 다른 터렛에 비해 느립니다. |
  
### 주요 적

| 바이러스 종류    | 이미지 | 설명                                    |
| ------------ | -------- | --------------------------------------- |
| 바이터 | <img width="64" height="64" alt="enemy_byter" src="https://github.com/user-attachments/assets/1c7fb372-bd4a-4c72-9aa0-dab96638b7f2" /> | 일반적인 형태의 바이러스입니다. |
| 웜 바이러스 | <img width="64" height="64" alt="enemy_worm" src="https://github.com/user-attachments/assets/58f4fe99-8f54-4235-bc6a-c9e8457f788e" /> | 체력은 낮지만 이동속도가 빠른, 민첩형 바이러스입니다.|
| 디도스 콜로서스 | <img width="64" height="64" alt="enemy_boss" src="https://github.com/user-attachments/assets/b3259d65-18f9-48c9-a306-dc8ada1666eb" /> | 10 라운드에 등장하는 보스 바이러스입니다.</br> 속도는 느리지만 체력이 일반 바이러스에 비해 월등히 높습니다.|

## 각 디렉토리 설명
* core/ : 
게임의 뼈대(루프, 씬 관리, UI 시스템)를 담당.

* scenes/ : 
시작, 게임, 종료 등 모든 화면(Stage) 을 담당하는 클래스들이 위치.

* entities/ : 
터렛, 적  등 모든 게임 오브젝트가 들어가는 곳.

* assets/ : 
이미지·사운드·폰트 등 리소스 파일 저장.

* data/ :
맵, 웨이브 정보 등 데이터 기반 파일 관리.

* ui/ :
UI 관련 JSON 파일 및 UI 시스템을 담당하는 클래스들이 위치.

## 실행 파일 (.exe) 빌드하기
아래 명령은 PyInstaller를 사용해 `dist/CPUDefense.exe`를 생성합니다. Windows/Linux 터미널에서 프로젝트 루트 기준으로 실행하세요.</br>

1. 프로젝트 클론
  ```bash
  git clone [해당 프로젝트 URL]
  ```
2. 의존성 설치

  ```bash
  pip install -r requirements.txt
  ```
3. 실행 파일 빌드

  ```bash
  python -m PyInstaller CPUDefense.spec
  ```

4. dist 폴더 안의 파일 실행
* 윈도우의 경우 CPUDefense.exe 파일을 실행
* 리눅스의 경우 CPUDefense 파일을 실행 (`./CPUDefense`)
     
