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
    "최창안": "2276b44819368116aabc000c9c7772a9",
    "정유빈": "2316b448193681c48a90000c627b2ea0",
    "유연송": "2316b44819368189bd6d000ce4d3ae01",
    "정종혁": "2316b4481936814aa291000c10494ca1",
    "최영은": "2316b44819368142b0af000caffe632b",
    "송현섭": "2316b44819368108a88b000c480e463c",
    "현석민": "2316b4481936817d8ed4000c21f29f39",
    "백유진": "2316b4481936811fb49d000c30074907",
    "홍지우": "2316b448193681408499000ce7f20324",
    "조정훈": "2316b448193681de9268000c69d0046b",
    "이도현": "2316b448193681728720000cef2c31d0",
    "김성민": "2316b448193681a08c6b000c16d4b04e",
    "이충신": "2316b44819368126ae95000cfd48a1a6",
    "한원탁": "2316b448193681cd8649000cd214e6f9",
    "한지민": "2316b4481936815daccb000c4afc5813",
    "박지환": "2316b448193681189dea000ca9ddf333",
    "박기현": "2316b4481936811ea9b0000c55c85290"
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
            print(f"💸 {name} - {count}회 작성 (벌금 500원)")
    print("---------------------------------")

# 이 스크립트 파일이 직접 실행될 때만 main() 함수를 호출합니다.
if __name__ == "__main__":
    main()