from flask import Flask, request, redirect, render_template_string
import requests
import os

app = Flask(__name__)

# Discord OAuth2 설정
CLIENT_ID = "1314993778775560282"  # 본인의 클라이언트 ID로 변경
CLIENT_SECRET = "YOUR_CLIENT_SECRET"  # 본인의 클라이언트 시크릿으로 변경
REDIRECT_URI = "https://login.ottf.kr/redirect.html"  # Discord 개발자 페이지에 등록된 리디렉션 URI

@app.route("/process")
def process_oauth():
    code = request.args.get("code")
    if not code:
        return render_template_string("<h2>❌ 인증 코드가 없습니다.</h2>"), 400

    # Discord로부터 토큰 요청
    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code != 200:
        return render_template_string("<h2>❌ Discord 인증 서버 오류</h2><p>{{ error }}</p>", error=response.text), 400

    token_data = response.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    # 사용자 정보 조회
    user_info = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    # 예: 콘솔에 저장 (여기서 DB 저장 등으로 교체 가능)
    print("✅ 로그인 성공:")
    print("User ID:", user_info["id"])
    print("Username:", user_info["username"])
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)

    # 성공 메시지 반환
    return render_template_string("""
        <h2>✅ 로그인 성공!</h2>
        <p><strong>{{ username }}</strong>님, 환영합니다.</p>
        <p>User ID: {{ userid }}</p>
    """, username=user_info["username"], userid=user_info["id"])

if __name__ == "__main__":
    # 실제 배포 시엔 반드시 production WSGI 서버 사용 (예: gunicorn)
    app.run(host="0.0.0.0", port=7000, debug=True)
