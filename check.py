#pip install notion-client

from notion_client import Client
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

#노션 토큰 가져오기
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

#기본값
notion = Client(auth=NOTION_TOKEN)

#최근 7일
today = datetime.now()
weekly = today - timedelta(days=7)

# 스터디원 각자의 노션 데이터베이스 ID 등록
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

#노트 개수 확인
def count_notes(db_id):
    try:
        result = notion.databases.query(
            database_id=db_id,
            filter={
                "property": "최종편집",
                "date": {
                    "on_or_after": weekly.isoformat()
                }
            }
        )
        return len(result["results"])
    except Exception as e:
        print(f" 오류: {db_id} 접근 실패 - {e}")
        return 0

#출력
def main():
    print("이번 주 노트 작성 현황: ")
    for name, db_id in user_databases.items():
        count = count_notes(db_id)
        if count >= 3:
            print(f"👌 {name} - {count}회 작성 (통과)")
        else:
            print(f"💸 {name} - {count}회 작성 (벌금 500원)")

if __name__ == "__main__":
    main()
