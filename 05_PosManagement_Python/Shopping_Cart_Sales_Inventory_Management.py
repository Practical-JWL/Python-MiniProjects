import flet as ft
import random # 랜덤 기능 추가

def main(page: ft.Page):
    page.title = "Smart Mart POS 시스템 (전 품목)"
    page.theme_mode = "light"
    page.window_width = 1000
    page.window_height = 800
    page.padding = 20

    # --- 전체 물품 리스트 ---
    물품_list = [
        "비누", "치약", "샴푸", "린스", "바디워시", "폼클렌징", "칫솔", "수건",
        "휴지", "물티슈", "세탁세제", "섬유유연제", "주방세제", "수세미", "고무장갑",
        "쌀", "라면", "햇반", "생수", "우유", "계란", "두부", "콩나물", "시금치",
        "양파", "감자", "고구마", "사과", "바나나", "오렌지", "귤", "토마토",
        "김치", "된장", "고추장", "간장", "식용유", "참기름", "소금", "설탕",
        "커피", "차", "과자", "빵", "젤리", "초콜릿", "음료수", "맥주", "소주",
        "고기(돼지고기)", "고기(소고기)", "닭고기", "생선", "오징어", "새우", "게",
        "쌀국수", "파스타", "잼", "버터", "치즈", "요거트", "아이스크림", "통조림",
        "냉동만두", "어묵", "햄", "소시지", "김", "미역", "다시마", "멸치",
        "밀가루", "부침가루", "튀김가루", "빵가루", "식초", "소스", "향신료",
        "양초", "성냥", "건전지", "전구", "쓰레기봉투", "지퍼백", "호일", "랩"
    ]

    # --- 데이터베이스 자동 생성 ---
    inventory = {}
    for item in 물품_list:
        # 가격: 500 ~ 10000원 사이 (100원 단위로 떨어지게)
        price = random.randint(5, 100) * 100 
        # 재고: 1 ~ 100개 사이
        stock = random.randint(1, 100)
        
        inventory[item] = [price, stock]

    cart = []
    total_sales_count = 0
    total_sales_revenue = 0

    # --- UI 요소 ---
    cart_list_view = ft.ListView(expand=True, spacing=5)
    total_price_text = ft.Text(value="현재 결제 금액: 0원", size=20, weight="bold", color="blue")
    sales_summary_text = ft.Text(value="오늘 총 매출: 0원 (0개 판매)", size=16, color="green")

    # --- 기능 함수 ---
    def add_to_cart(e):
        item_name = e.control.data
        if inventory[item_name][1] > 0:
            inventory[item_name][1] -= 1
            cart.append(item_name)
            cart_list_view.controls.append(ft.Text(f"• {item_name} ({inventory[item_name][0]:,}원)"))
            
            current_total = sum(inventory[item][0] for item in cart)
            total_price_text.value = f"현재 결제 금액: {current_total:,}원"
            
            # 버튼 내부 재고 텍스트 업데이트
            e.control.content.controls[2].value = f"({inventory[item_name][1]}개 남음)"
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"{item_name} 재고가 없습니다!"))
            page.snack_bar.open = True
            page.update()

    def checkout(e):
        nonlocal total_sales_count, total_sales_revenue, cart
        if not cart: return
        current_bill = sum(inventory[item][0] for item in cart)
        total_sales_count += len(cart)
        total_sales_revenue += current_bill
        
        sales_summary_text.value = f"오늘 총 매출: {total_sales_revenue:,}원 ({total_sales_count}개 판매)"
        cart.clear()
        cart_list_view.controls.clear()
        total_price_text.value = "현재 결제 금액: 0원"
        
        page.snack_bar = ft.SnackBar(ft.Text("결제가 완료되었습니다!"))
        page.snack_bar.open = True
        page.update()

    # --- 레이아웃 구성 ---
    # 물품이 많아졌으므로 GridView가 유용하게 쓰입니다. (마우스 휠로 스크롤 가능)
    product_grid = ft.GridView(expand=True, runs_count=4, max_extent=120, spacing=10)

    for name, info in inventory.items():
        # 가격 정보도 버튼에 같이 보이도록 추가했습니다.
        btn_layout = ft.Column(
            controls=[
                ft.Text(name, weight="bold", size=13),
                ft.Text(f"{info[0]:,}원", size=11, color="blue700"), # 가격 표시
                ft.Text(f"({info[1]}개 남음)", size=11)
            ],
            alignment="center",
            horizontal_alignment="center"
        )
        
        product_grid.controls.append(
            ft.Container(
                content=btn_layout,
                data=name,
                on_click=add_to_cart,
                bgcolor="blue50",
                border_radius=8,
                border=ft.border.all(1, "blue200"),
                padding=5
            )
        )

    # 우측 결제 패널
    right_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("🛒 장바구니", size=24, weight="bold"),
                ft.Divider(),
                ft.Container(content=cart_list_view, height=400), # 장바구니 높이 조절
                total_price_text,
                ft.ElevatedButton(
                    content=ft.Text("결제하기", color="white", weight="bold"),
                    bgcolor="blue",
                    on_click=checkout,
                    width=300
                ),
                ft.Divider(),
                ft.Text("📊 오늘 정산", size=18, weight="bold"),
                sales_summary_text
            ]
        ),
        padding=20,
        bgcolor="#f8f9fa",
        border_radius=12,
        width=350
    )

    page.add(
        ft.Row(
            controls=[
                ft.Column(controls=[ft.Text("상품 목록 (스크롤 하세요)", size=24, weight="bold"), product_grid], expand=True),
                right_panel
            ],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)