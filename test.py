import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)

# 문제가 되는 두 사람의 DB ID
target_users = {
    "유연송": "2316b448193680939059d2e5c0e20eba",
    "한원탁": "2316b448193680a9a50cfe2cb8cdcc9b"
}

print("🕵️  페이지의 '작성일시' 속성을 함께 확인합니다...")
print("---------------------------------")

for name, db_id in target_users.items():
    try:
        response = notion.databases.query(database_id=db_id)
        pages = response.get("results", [])
        
        print(f"[{name}] - 총 {len(pages)}개의 페이지를 찾았습니다.")
        
        for page in pages:
            properties = page.get("properties", {})
            
            # --- 제목 가져오기 ---
            title_info = properties.get("이름") or properties.get("Name")
            title = "제목 없음"
            if title_info and title_info.get("title"):
                title = title_info["title"][0]["plain_text"]
            
            # ▼▼▼ '작성일시' 속성 값 가져오는 부분 ▼▼▼
            creation_date_prop = properties.get("작성일시") # 속성 이름으로 접근
            creation_date = "작성일시 없음"
            
            # '작성일시' 속성이 존재하고, 날짜(date) 타입의 데이터가 있다면
            if creation_date_prop and creation_date_prop.get("date"):
                creation_date = creation_date_prop["date"]["start"] # 날짜 값 추출
            # ▲▲▲ 여기까지 ▲▲▲

            print(f"  - 제목: {title} (작성일시: {creation_date})")
        print("---")

    except Exception as e:
        print(f" ❌ [{name}] 오류 발생: {e}")

print("---------------------------------")