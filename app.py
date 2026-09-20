import streamlit as st
from math import ceil

st.set_page_config(
    page_title="天津旅游规划",
    page_icon="🌆",
    layout="wide"
)

# =========================
# 示例数据库
# =========================
ATTRACTIONS = [
    {"name":"五大道","area":"和平区","type":"历史建筑","hours":3,"pace":["慢","快"],
     "tags":["文化","慢节奏","城市"],"outskirts":False},
    {"name":"瓷房子","area":"和平区","type":"历史建筑","hours":1,"pace":["快"],
     "tags":["文化","打卡","城市"],"outskirts":False},
    {"name":"意式风情区","area":"河北区","type":"历史街区","hours":2,"pace":["慢","快"],
     "tags":["文化","街区","夜游","打卡"],"outskirts":False},
    {"name":"古文化街","area":"南开区","type":"民俗文化","hours":2.5,"pace":["慢","快"],
     "tags":["文化","津味","美食","购物"],"outskirts":False},
    {"name":"海河沿岸","area":"市中心","type":"城市景观","hours":2.5,"pace":["慢","快"],
     "tags":["夜游","城市","慢节奏"],"outskirts":False},
    {"name":"天津之眼","area":"河北区","type":"城市地标","hours":1,"pace":["快"],
     "tags":["打卡","夜游"],"outskirts":False},
    {"name":"鼓楼","area":"南开区","type":"历史文化","hours":1.5,"pace":["慢","快"],
     "tags":["文化","城市"],"outskirts":False},
    {"name":"杨柳青古镇","area":"西青区","type":"古镇民俗","hours":4,"pace":["慢"],
     "tags":["文化","慢节奏","民俗"],"outskirts":True},
    {"name":"盘山","area":"蓟州区","type":"自然山水","hours":7,"pace":["慢"],
     "tags":["自然","慢节奏","郊区"],"outskirts":True},
    {"name":"黄崖关长城","area":"蓟州区","type":"历史自然","hours":7,"pace":["慢"],
     "tags":["自然","文化","郊区"],"outskirts":True},
    {"name":"东疆湾","area":"滨海新区","type":"滨海休闲","hours":5,"pace":["慢","快"],
     "tags":["自然","休闲","郊区"],"outskirts":True},
]

RESTAURANTS = [
    {"name":"津味老字号A（示例）","cuisine":"津菜","spicy":"清淡","thickening":True,"area":"南开区","price":70},
    {"name":"天津家常菜B（示例）","cuisine":"津菜","spicy":"微辣","thickening":False,"area":"和平区","price":85},
    {"name":"鲁菜馆（示例）","cuisine":"鲁菜","spicy":"清淡","thickening":True,"area":"和平区","price":90},
    {"name":"川味馆（示例）","cuisine":"川菜","spicy":"辣","thickening":False,"area":"和平区","price":95},
    {"name":"粤菜馆（示例）","cuisine":"粤菜","spicy":"清淡","thickening":True,"area":"河西区","price":120},
    {"name":"苏菜馆（示例）","cuisine":"苏菜","spicy":"清淡","thickening":True,"area":"河西区","price":110},
    {"name":"闽菜馆（示例）","cuisine":"闽菜","spicy":"微辣","thickening":False,"area":"和平区","price":100},
    {"name":"浙菜馆（示例）","cuisine":"浙菜","spicy":"清淡","thickening":False,"area":"南开区","price":105},
    {"name":"湘菜馆（示例）","cuisine":"湘菜","spicy":"中辣","thickening":False,"area":"河西区","price":90},
    {"name":"徽菜馆（示例）","cuisine":"徽菜","spicy":"微辣","thickening":True,"area":"南开区","price":95},
]

HOTELS = [
    {"name":"经济型酒店A（示例）","area":"南开区","price":130,"level":"经济型","near":"古文化街、鼓楼"},
    {"name":"舒适型酒店B（示例）","area":"和平区","price":240,"level":"舒适型","near":"五大道、海河"},
    {"name":"品质型酒店C（示例）","area":"河北区","price":380,"level":"品质型","near":"意式风情区、天津之眼"},
    {"name":"高端酒店D（示例）","area":"和平区","price":680,"level":"高端型","near":"五大道、海河"},
]

BUDGETS = {
    "经济型": (0,150),
    "舒适型": (150,300),
    "品质型": (300,500),
    "高端型": (500,9999)
}

SPICY_LEVEL = {"清淡":0, "微辣":1, "中辣":2, "辣":3}


# =========================
# 推荐算法
# =========================
def score_attraction(a, pace, outskirts):
    score = 0

    if pace in a["pace"]:
        score += 5

    if pace == "慢" and "慢节奏" in a["tags"]:
        score += 3

    if pace == "快" and "打卡" in a["tags"]:
        score += 3

    if outskirts == "希望包含郊区" and a["outskirts"]:
        score += 6
    elif outskirts == "可去郊区" and a["outskirts"]:
        score += 2
    elif outskirts == "只玩市区" and not a["outskirts"]:
        score += 2

    if "文化" in a["tags"]:
        score += 2

    return score


def get_attractions(pace, outskirts):
    candidates = [
        a.copy() for a in ATTRACTIONS
        if not (outskirts == "只玩市区" and a["outskirts"])
    ]

    for a in candidates:
        a["score"] = score_attraction(a, pace, outskirts)

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates


def generate_itinerary(days, pace, outskirts):
    candidates = get_attractions(pace, outskirts)

    # 防止同一景点重复安排
    result = []
    used = set()
    cursor = 0

    if pace == "慢":
        daily_count = 2
        daily_limit = 7
    else:
        daily_count = 4
        daily_limit = 9

    themes = [
        "近代天津",
        "津门民俗",
        "海河与城市生活",
        "天津文化漫游",
        "自然与古镇",
        "城市深度体验",
        "自由探索"
    ]

    for day in range(1, days + 1):
        today = []
        total_hours = 0

        # 第一轮：从高分景点中选择
        for i in range(len(candidates)):
            a = candidates[(cursor + i) % len(candidates)]

            if a["name"] in used:
                continue

            if not today or total_hours + a["hours"] <= daily_limit:
                today.append(a)
                used.add(a["name"])
                total_hours += a["hours"]

            if len(today) >= daily_count:
                break

        # 如果景点已经用完，允许循环使用，保证1-7天都有结果
        if not today:
            a = candidates[(day - 1) % len(candidates)]
            today = [a]

        cursor += max(1, len(today))

        result.append({
            "day": day,
            "title": themes[(day - 1) % len(themes)],
            "spots": today,
            "hours": round(total_hours, 1)
        })

    return result


def recommend_restaurants(thickening, spicy, cuisines):
    candidates = []

    for r in RESTAURANTS:
        if cuisines and r["cuisine"] not in cuisines:
            continue

        if thickening == "否" and r["thickening"]:
            continue

        # 辣度允许上下浮动一级，避免没有完全匹配时一个都推荐不出来
        if abs(SPICY_LEVEL[r["spicy"]] - SPICY_LEVEL[spicy]) > 1:
            continue

        candidates.append(r)

    if not candidates:
        # 如果条件过严，优先保证“不接受勾芡”这一条件
        candidates = [
            r for r in RESTAURANTS
            if not (thickening == "否" and r["thickening"])
        ]

    return candidates[:5]


def recommend_hotel(budget):
    low, high = BUDGETS[budget]
    candidates = [
        h for h in HOTELS
        if low <= h["price"] <= high
    ]

    if not candidates:
        # 演示数据不足时选择最接近预算的酒店
        target = (low + min(high, 1000)) / 2
        candidates = sorted(
            HOTELS,
            key=lambda h: abs(h["price"] - target)
        )

    # 市中心住宿优先，方便旅游
    candidates.sort(
        key=lambda h: (
            0 if h["area"] == "和平区" else 1,
            h["price"]
        )
    )

    return candidates[0]


def calculate_budget(days, people, hotel, pace):
    hotel_cost = hotel["price"] * days

    # 每人每天餐饮参考预算
    food_per_person = 90
    food_cost = days * people * food_per_person

    # 快节奏通常移动次数更多
    transport_per_person = 70 if pace == "快" else 50
    transport_cost = days * people * transport_per_person

    total = hotel_cost + food_cost + transport_cost

    return {
        "hotel": hotel_cost,
        "food": food_cost,
        "transport": transport_cost,
        "total": total
    }


# =========================
# 页面
# =========================
st.title("🌆 天津旅游规划")
st.caption("输入你的旅行偏好，自动生成 1～7 天个性化天津行程")

st.divider()

# ---------- 用户输入 ----------
st.subheader("① 基本旅行信息")

col1, col2, col3 = st.columns(3)

with col1:
    days = st.selectbox("旅游天数", list(range(1, 8)), index=2, format_func=lambda x: f"{x} 天")

with col2:
    people = st.selectbox("旅行人数", [1, 2, 3, 4, 5, 6], index=1, format_func=lambda x: f"{x} 人")

with col3:
    pace = st.radio(
        "游玩节奏",
        ["慢", "快"],
        horizontal=True,
        format_func=lambda x: "🐢 慢节奏融入本地" if x == "慢" else "⚡ 快节奏打卡"
    )

st.subheader("② 饮食偏好")

col1, col2 = st.columns(2)

with col1:
    thickening = st.radio(
        "能否接受勾芡？",
        ["能", "否"],
        horizontal=True
    )

with col2:
    spicy = st.select_slider(
        "辣度",
        options=["清淡", "微辣", "中辣", "辣"],
        value="清淡"
    )

cuisines = st.multiselect(
    "偏好菜系（可多选）",
    ["鲁菜", "川菜", "粤菜", "苏菜", "闽菜", "浙菜", "湘菜", "徽菜", "津菜"],
    default=["津菜"]
)

st.subheader("③ 住宿与活动范围")

col1, col2 = st.columns(2)

with col1:
    hotel_budget = st.radio(
        "住宿预算",
        ["经济型", "舒适型", "品质型", "高端型"],
        index=1
    )

with col2:
    outskirts = st.radio(
        "是否愿意前往市区以外？",
        ["只玩市区", "可去郊区", "希望包含郊区"]
    )

st.divider()

generate = st.button(
    "✨ 生成我的天津旅游规划",
    type="primary",
    use_container_width=True
)

# =========================
# 生成结果
# =========================
if generate:

    if not cuisines:
        st.warning("请至少选择一种偏好菜系。")
        st.stop()

    itinerary = generate_itinerary(days, pace, outskirts)
    restaurants = recommend_restaurants(thickening, spicy, cuisines)
    hotel = recommend_hotel(hotel_budget)
    budget = calculate_budget(days, people, hotel, pace)

    st.success("已经根据你的偏好生成行程！")

    st.header("📋 你的旅行方案")

    st.write(
        f"**{days}天 · {'慢节奏本地体验' if pace == '慢' else '快节奏城市打卡'} · "
        f"{hotel_budget}住宿 · {outskirts}**"
    )

    # 行程
    st.subheader("🗺️ 每日行程")

    for day in itinerary:
        with st.container(border=True):
            st.markdown(f"### DAY {day['day']}｜{day['title']}")
            st.caption(f"预计游玩时间：约 {day['hours']} 小时")

            for idx, spot in enumerate(day["spots"], start=1):
                st.markdown(
                    f"**{idx}. {spot['name']}**  \n"
                    f"{spot['area']} · {spot['type']} · 建议 {spot['hours']} 小时"
                )

                if pace == "慢":
                    st.caption("适合慢慢游览、散步，并留出休息和本地生活体验时间。")
                else:
                    st.caption("适合快速打卡，减少单个景点停留时间。")

            # 每天推荐餐厅
            if restaurants:
                r = restaurants[(day["day"] - 1) % len(restaurants)]
                st.info(
                    f"🍜 餐饮建议：{r['name']} · {r['cuisine']} · "
                    f"{r['spicy']} · 人均约 ¥{r['price']}"
                )

    # 酒店
    st.subheader("🏨 住宿建议")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("推荐酒店", hotel["name"])

    with col2:
        st.metric("每晚参考价格", f"¥{hotel['price']}")

    with col3:
        st.metric("所在区域", hotel["area"])

    st.write(f"附近景点：**{hotel['near']}**")

    # 餐饮
    st.subheader("🍜 饮食推荐")

    st.write(
        f"你的偏好：**{spicy} · "
        f"{'接受勾芡' if thickening == '能' else '不接受勾芡'} · "
        f"{'、'.join(cuisines)}**"
    )

    for r in restaurants:
        st.markdown(
            f"- **{r['name']}**：{r['cuisine']} · {r['spicy']} · "
            f"{'含勾芡' if r['thickening'] else '不含勾芡'} · "
            f"人均约 ¥{r['price']}"
        )

    # 预算
    st.subheader("💰 参考预算")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("住宿", f"¥{budget['hotel']}")
    c2.metric("餐饮", f"¥{budget['food']}")
    c3.metric("交通", f"¥{budget['transport']}")
    c4.metric("合计", f"¥{budget['total']}")

    st.caption(
        "以上预算为课程项目演示用估算，不代表实时市场价格。"
    )

    # 规划逻辑
    with st.expander("🔍 查看系统是怎样生成行程的"):
        st.write("""
        1. 根据“市区/郊区”筛选景点；
        2. 根据“慢节奏/快节奏”给景点评分；
        3. 综合文化、打卡、自然等标签排序；
        4. 按每天可游玩时间限制安排景点；
        5. 根据菜系、辣度和是否接受勾芡筛选餐厅；
        6. 根据住宿预算筛选酒店；
        7. 根据旅行天数、人数和节奏估算预算。
        """)

    st.warning(
        "目前景点、餐厅和酒店均为课程项目演示数据。正式项目应替换为真实、"
        "经过核验的数据，并进一步接入地图、路线、实时价格和营业状态。"
    )

else:
    st.info("👆 填写你的旅游偏好，然后点击“生成我的天津旅游规划”。")
