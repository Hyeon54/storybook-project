#서버 실행용 메인 파일
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# app.run(debug=True)는 아래와 같은 기본값을 가지고 있음
# app.run(
#     host="127.0.0.1",   # 로컬호스트 = 내 컴퓨터
#     port=5000,          # 포트번호 = 5000
#     debug=True          # 디버그 모드 켬
# )


# 포트 번호 바꾸고 싶으면,
# app.run(host="127.0.0.1", port=8000, debug=True)

# 외부 접속 허용하고 싶으면,
# app.run(host="0.0.0.0", port=5000)
#host="0.0.0.0" 으로 바꾸면 다른 컴퓨터에서도 접근 가능(같은 네트워크 내에서만)
