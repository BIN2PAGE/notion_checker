# 필요한 라이브러리들을 불러옵니다.
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from notion_client import Client
# .env 파일에서 환경 변수를 불러옵니다. (NOTION_TOKEN)
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

# 노션 API 클라이언트를 인증합니다.
notion = Client(auth=NOTION_TOKEN)

# 검사 기준이 될 7일 전의 날짜를 계산합니다.
today = datetime.now()
weekly = today - timedelta(days=7)

# 스터디원 각자의 노션 데이터베이스 ID를 등록합니다.
user_databases = {
    "최창안": "2276b448193680fdae27ccea60865377",
    "정유빈": "2316b4481936803499a3fd312cf14f1e",
    "정종혁": "2316b44819368072ad11cf8c5bd16fd2",
    "최영은": "2316b44819368078b2b7e7c971eff268",
    "송현섭": "2316b4481936806e8ec6c35aaa45da36",
    "현석민": "2316b4481936805d8c07e04fe1f31406",
    "백유진": "2316b448193680e7a5d8e1f4bed51ae1",
    "홍지우": "2316b448193680c2945ac8dc43030573",
    "조정훈": "2316b44819368089ab86c8d2e2493bd3",
    "이도현": "2316b44819368019ba3cccda6a04d3c4",
    "김성민": "2316b448193680859213f2e3e0258bbf",
    "이충신": "2316b44819368053809bdde195acf656",
    "한원탁": "2316b448193680a9a50cfe2cb8cdcc9b",
    "한지민": "2316b448193680e4bcb5e308050dd3b4",
    "박지환": "2316b448193680969a72cda16cc0298f",
    "박기현": "2316b4481936801d9af5f10ce7362097"
}

# '새로 생성된' 노트 개수를 확인하는 함수
def count_notes(db_id):
    """지정된 데이터베이스 ID에서 지난 7일 동안 '생성된' 페이지 수를 반환합니다."""
    try:
        result = notion.databases.query(
            database_id=db_id,
            # 필터 조건을 '최종 편집 시간'이 아닌 '생성 시간' 기준으로 변경
            filter={
                "timestamp": "created_time",
                "created_time": {
                    "on_or_after": weekly.isoformat()
                }
            }
        )
        return len(result["results"])
    except Exception as e:
        # 오류 발생 시 (예: 토큰 오류, DB ID 오류) 메시지를 출력하고 0을 반환합니다.
        print(f" 오류 발생: 데이터베이스 ID '{db_id}' 접근 실패 - {e}")
        return 0


money=500
# 메인 실행 함수
def main():
    """모든 사용자를 순회하며 노트 작성 현황을 출력합니다."""
    print("✅ 이번 주 신규 노트 작성 현황:")
    print("---------------------------------")
    for name, db_id in user_databases.items():
        count = count_notes(db_id)
        if count >= 3:
            print(f"👌 {name} - {count}회 작성 (통과)")
        else:
            total = 1500 - money * count
            print(f"💸 {name} - {count}회 작성(벌금 {total}원) ")
            
    print("---------------------------------")

# 이 스크립트 파일이 직접 실행될 때만 main() 함수를 호출합니다.
if __name__ == "__main__":
    main()

    