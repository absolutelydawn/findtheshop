# #!/bin/bash

# pid=$(lsof -t -i :5000)

# if [ -n "$pid" ]; then
#     pm2 delete my-json-server
# fi
# pm2 start json-server --watch db.json --name my-json-server -- --port 5000 &

# # fastapi
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

#!/bin/bash

restart_server() {
    json-server --watch items.json --port 5000 &
    echo "JSON Server restarted."
}

# 파일 변경 감지 및 서버 재시작을 수행하는 메인 함수
main() {
    # 이전에 실행 중이던 JSON Server 프로세스를 모두 종료
    pkill -f "json-server --watch items.json --port 5000"

    # 파일 변경 감지
    inotifywait -m -e close_write,moved_to,create . |
    while read -r directory events filename; do
        if [ "$filename" = "items.json" ]; then
            restart_server
        fi
    done
}

# 메인 함수 호출
main
