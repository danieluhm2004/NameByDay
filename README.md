# NAME BY DAY !

## 요일마다 이름을 바꾸자!

**애플 연락처 기능**을 사용하여, 원하는 연락처의 이름을 매요일마다 새로운 이름을 지정해줄 수 있습니다. 뿐만 아니라, 날짜를 입력하여 디데잍 또한 지정해줄 수 있습니다.

~~여자친구 기념일을 잊어버려 싸움이 일어날 수도 있는 분들을 위한 최고의 솔류션~~

⚠️ 해당 소프트웨어를 사용함에 따른 책임은 이를 이용하는 사용자에게 있음을 알려드립니다. 실험용으로 만들어진 프로젝트니 절대 신뢰하지 마세요.

## 환경변수 설정

먼저, 아래와 같이 환경 변수를 지정해주세요.

```bash
NBD_ICLOUD_EMAIL="아이클라우드 로그인할때 사용하는 아이디"
NBD_ICLOUD_PASSWORD="나의 소듕한 아이클라우드 비밀번호"
NBD_PHONE_NUMBER="ㅇ..여자친구.. ㅈ..전화번호" # 전화번호
NBD_NAME_PREFIX="ㅇ..여자친구 이ㄹ..름" # 접두사 (optional)
NBD_NAME_SUFFIX="일" # 접미사 (optional)
NBD_NAME_SUNDAY="🤍" #일요일 (optional)
NBD_NAME_MONDAY="❤️" #월요일 (optional)
NBD_NAME_TUESDAY="🧡" #화요일 (optional)
NBD_NAME_WEDNESDAY="💛" #수요일 (optional)
NBD_NAME_THURSDAY="💚" #목요일 (optional)
NBD_NAME_FRIDAY="💙" #금요일 (optional)
NBD_NAME_SATURDAY="💜" #토요일 (optional)
NBD_DDAY_DATE="2021-07-08" #DDAY(optional)
```

위처럼 입력하여, `.env` 파일에 저장합니다. \*\*다만, 전화번호

## 도커로 실행

기본적으로 해당 프로젝트는 도커 위에서 배포하는 방법으로 제공됩니다.

```yaml
version: '3'

services:
  namebyday:
    image: ghcr.io/danieluhm2004/namebyday:1.0.0
    container_name: NameByDay
    volumes:
      - sessions:/app/sessions
    env_file:
      - .env

volumes:
  sessions:
    external: true
```

위처럼 입력하신 다음 `docker-compose.yaml`에 저장 후 아래 명령어를 입력하여 볼륨을 생성해줍니다. **여기서 볼륨은 로그인 세션을 지속적으로 저장하기 위해 사용됩니다.**

```bash
docker volume create --name=sessions
```

먼저, 크론탭을 등록하기 전에 로그인부터 진행해주어야 합니다.

```bash
docker-compose run namebyday
```

환경변수 설정을 올바르게 했다면 아래와 같이 메세지가 뜨며, 애플 2차 인증 알림이 뜹니다.

```bash
Creating example_namebyday_run ... done
Two-factor authentication required.
Enter the code you received of one of your approved devices:
```

여기서 애플 2차 인증 알림을 승인하고 뜬 6자리 임시 번호를 입력하면 아래와 같이 정상적으로 뜨며 프로그램이 종료될 것입니다.

```bash
Creating example_namebyday_run ... done
Two-factor authentication required.
Enter the code you received of one of your approved devices: 513452
Code validation result: True
```

이제 크론탭을 등록하여 자동으로 연락처 이름을 바뀌도록 해봅시다.

```bash
crontab -e
```

명령어를 사용하여 크론탭 에디터 창으로 넘어갑니다.

```bash
* * * * * docker-compose <프로젝트 위치>/docker-compose.yaml up >> <프로젝트 위치>/main.log
```

`<프로젝트 위치>`부분을 `docker-compose.yaml`을 설정한 디렉토리로 지정합니다.

이제, ~~당신은 여자친구의 기념일을 놓치지 않을 수 있습니다.~~ 매요일 새로운 이름으로 친한 사람의 이름을 저장할 수 있습니다.
