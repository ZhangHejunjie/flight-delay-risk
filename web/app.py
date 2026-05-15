import os
import json
import requests
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = None

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

AVIATIONSTACK_KEY = os.environ.get("AVIATIONSTACK_KEY", "68c479c674a89fee0639d9433cad909a")

HISTORY_FILE = Path(__file__).parent / "data" / "history.json"
HISTORY_MAX = 15


def _load_history_db():
    if not HISTORY_FILE.exists():
        return {}
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_history_db(db):
    HISTORY_FILE.parent.mkdir(exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


def push_history(user_id, entry):
    """将新查询记录插到用户历史最前面，去重并限制 HISTORY_MAX 条。"""
    db = _load_history_db()
    records = db.get(user_id, [])
    records = [r for r in records if r["flight"] != entry["flight"]]
    records.insert(0, entry)
    db[user_id] = records[:HISTORY_MAX]
    _save_history_db(db)


def get_history(user_id):
    db = _load_history_db()
    return db.get(user_id, [])

# 机场 IATA → wttr.in 查询城市名
AIRPORT_CITY = {
    "PEK": "Beijing", "PKX": "Beijing", "SHA": "Shanghai", "PVG": "Shanghai",
    "CAN": "Guangzhou", "SZX": "Shenzhen", "CTU": "Chengdu", "TFU": "Chengdu",
    "KMG": "Kunming", "XIY": "Xian", "WUH": "Wuhan", "NKG": "Nanjing",
    "HGH": "Hangzhou", "XMN": "Xiamen", "CSX": "Changsha", "DLC": "Dalian",
    "SHE": "Shenyang", "HRB": "Harbin", "TSN": "Tianjin", "TAO": "Qingdao",
    "URC": "Urumqi", "KRY": "Karamay", "LHW": "Lanzhou", "SYX": "Sanya",
    "HAK": "Haikou", "NNG": "Nanning", "KWE": "Guiyang", "KHN": "Nanchang",
    "HKG": "Hong+Kong", "MFM": "Macau", "TPE": "Taipei", "KHH": "Kaohsiung",
    "NRT": "Tokyo", "HND": "Tokyo", "KIX": "Osaka", "ICN": "Seoul",
    "GMP": "Seoul", "SIN": "Singapore", "BKK": "Bangkok", "DMK": "Bangkok",
    "KUL": "Kuala+Lumpur", "CGK": "Jakarta", "MNL": "Manila",
    "SGN": "Ho+Chi+Minh+City", "HAN": "Hanoi", "SYD": "Sydney",
    "MEL": "Melbourne", "AKL": "Auckland", "DEL": "Delhi", "BOM": "Mumbai",
    "DXB": "Dubai", "AUH": "Abu+Dhabi", "DOH": "Doha",
    "LHR": "London", "LGW": "London", "CDG": "Paris", "ORY": "Paris",
    "FRA": "Frankfurt", "MUC": "Munich", "AMS": "Amsterdam", "MAD": "Madrid",
    "BCN": "Barcelona", "FCO": "Rome", "MXP": "Milan", "ZRH": "Zurich",
    "VIE": "Vienna", "IST": "Istanbul", "SVO": "Moscow",
    "JFK": "New+York", "LGA": "New+York", "EWR": "Newark",
    "LAX": "Los+Angeles", "ORD": "Chicago", "ATL": "Atlanta",
    "DFW": "Dallas", "SFO": "San+Francisco", "SEA": "Seattle",
    "BOS": "Boston", "MIA": "Miami", "YYZ": "Toronto", "YVR": "Vancouver",
}

# 机场 IATA → 中文名称
AIRPORT_ZH = {
    "PEK": "北京首都国际机场", "PKX": "北京大兴国际机场",
    "SHA": "上海虹桥国际机场", "PVG": "上海浦东国际机场",
    "CAN": "广州白云国际机场", "SZX": "深圳宝安国际机场",
    "CTU": "成都天府国际机场", "TFU": "成都双流国际机场",
    "KMG": "昆明长水国际机场", "XIY": "西安咸阳国际机场",
    "WUH": "武汉天河国际机场", "NKG": "南京禄口国际机场",
    "HGH": "杭州萧山国际机场", "XMN": "厦门高崎国际机场",
    "CSX": "长沙黄花国际机场", "DLC": "大连周水子国际机场",
    "SHE": "沈阳桃仙国际机场", "HRB": "哈尔滨太平国际机场",
    "TSN": "天津滨海国际机场", "TAO": "青岛胶东国际机场",
    "URC": "乌鲁木齐地窝堡国际机场", "KRY": "克拉玛依机场",
    "LHW": "兰州中川国际机场", "SYX": "三亚凤凰国际机场",
    "HAK": "海口美兰国际机场", "NNG": "南宁吴圩国际机场",
    "KWE": "贵阳龙洞堡国际机场", "KHN": "南昌昌北国际机场",
    "HKG": "香港国际机场", "MFM": "澳门国际机场",
    "TPE": "台北桃园国际机场", "KHH": "高雄小港国际机场",
    "NRT": "东京成田国际机场", "HND": "东京羽田机场",
    "KIX": "大阪关西国际机场", "ITM": "大阪伊丹机场",
    "ICN": "首尔仁川国际机场", "GMP": "首尔金浦国际机场",
    "SIN": "新加坡樟宜机场", "BKK": "曼谷素万那普机场",
    "DMK": "曼谷廊曼机场", "KUL": "吉隆坡国际机场",
    "CGK": "雅加达苏加诺-哈达国际机场", "MNL": "马尼拉尼诺伊·阿基诺国际机场",
    "SGN": "胡志明市新山一国际机场", "HAN": "河内内排国际机场",
    "SYD": "悉尼金斯福德·史密斯机场", "MEL": "墨尔本机场",
    "AKL": "奥克兰国际机场", "DEL": "德里英迪拉·甘地国际机场",
    "BOM": "孟买查特拉帕蒂·希瓦吉国际机场",
    "DXB": "迪拜国际机场", "AUH": "阿布扎比国际机场", "DOH": "多哈哈马德国际机场",
    "LHR": "伦敦希思罗机场", "LGW": "伦敦盖特威克机场",
    "CDG": "巴黎戴高乐机场", "ORY": "巴黎奥利机场",
    "FRA": "法兰克福机场", "MUC": "慕尼黑机场",
    "AMS": "阿姆斯特丹史基浦机场", "MAD": "马德里巴拉哈斯机场",
    "BCN": "巴塞罗那埃尔普拉特机场", "FCO": "罗马菲乌米奇诺机场",
    "MXP": "米兰马尔彭萨机场", "ZRH": "苏黎世机场",
    "VIE": "维也纳国际机场", "IST": "伊斯坦布尔机场", "SVO": "莫斯科谢列梅捷沃机场",
    "JFK": "纽约肯尼迪国际机场", "LGA": "纽约拉瓜迪亚机场",
    "EWR": "纽瓦克自由国际机场", "LAX": "洛杉矶国际机场",
    "ORD": "芝加哥奥黑尔国际机场", "ATL": "亚特兰大哈茨菲尔德-杰克逊机场",
    "DFW": "达拉斯-沃思堡国际机场", "SFO": "旧金山国际机场",
    "SEA": "西雅图塔科马国际机场", "BOS": "波士顿洛根国际机场",
    "MIA": "迈阿密国际机场", "YYZ": "多伦多皮尔逊国际机场",
    "YVR": "温哥华国际机场",
}


WEATHER_ZH = {
    # 晴
    "Sunny": "晴",
    "Clear": "晴",
    # 多云
    "Partly cloudy": "局部多云",
    "Partly Cloudy": "局部多云",
    "Cloudy": "多云",
    "Overcast": "阴天",
    # 雾/霾
    "Mist": "薄雾",
    "Fog": "雾",
    "Freezing fog": "冻雾",
    # 毛毛雨
    "Patchy light drizzle": "局部小毛毛雨",
    "Light drizzle": "小毛毛雨",
    "Freezing drizzle": "冻毛毛雨",
    "Heavy freezing drizzle": "大冻毛毛雨",
    # 雨
    "Patchy rain nearby": "局部有雨",
    "Patchy rain possible": "局部可能有雨",
    "Light rain": "小雨",
    "Moderate rain": "中雨",
    "Heavy rain": "大雨",
    "Light rain shower": "阵小雨",
    "Moderate or heavy rain shower": "阵中大雨",
    "Torrential rain shower": "暴雨",
    "Light freezing rain": "小冻雨",
    "Moderate or heavy freezing rain": "中大冻雨",
    # 冰雹
    "Light sleet": "小雨夹雪",
    "Moderate or heavy sleet": "中大雨夹雪",
    "Ice pellets": "冰粒",
    "Light sleet showers": "阵小雨夹雪",
    "Moderate or heavy sleet showers": "阵中大雨夹雪",
    "Light showers of ice pellets": "阵小冰粒",
    "Moderate or heavy showers of ice pellets": "阵中大冰粒",
    # 雪
    "Patchy snow possible": "局部可能有雪",
    "Patchy light snow": "局部小雪",
    "Light snow": "小雪",
    "Patchy moderate snow": "局部中雪",
    "Moderate snow": "中雪",
    "Patchy heavy snow": "局部大雪",
    "Heavy snow": "大雪",
    "Blowing snow": "吹雪",
    "Blizzard": "暴风雪",
    "Light snow showers": "阵小雪",
    "Moderate or heavy snow showers": "阵中大雪",
    # 雷暴
    "Thundery outbreaks possible": "可能有雷暴",
    "Patchy light rain with thunder": "局部小雨伴雷",
    "Moderate or heavy rain with thunder": "中大雨伴雷",
    "Patchy light snow with thunder": "局部小雪伴雷",
    "Moderate or heavy snow with thunder": "中大雪伴雷",
    "Thunderstorm": "雷暴",
    # 沙尘
    "Blowing dust": "扬沙",
    "Sandstorm": "沙尘暴",
    "Dust": "浮尘",
}


class User(UserMixin):
    def __init__(self, id, name, email, picture):
        self.id = id
        self.name = name
        self.email = email
        self.picture = picture


_users = {}


@login_manager.user_loader
def load_user(user_id):
    return _users.get(user_id)


def translate_weather(desc):
    return WEATHER_ZH.get(desc, desc)


def get_weather(city_name, iata_code):
    query = city_name.replace(" ", "+") if city_name else AIRPORT_CITY.get(iata_code, iata_code)
    try:
        r = requests.get(f"https://wttr.in/{query}?format=j1", timeout=8)
        d = r.json()["current_condition"][0]
        return {
            "desc": translate_weather(d["weatherDesc"][0]["value"]),
            "desc_en": d["weatherDesc"][0]["value"],
            "temp": d["temp_C"],
            "feels": d["FeelsLikeC"],
            "visibility": round(int(d["visibility"]) / 10, 1),
            "wind": d["windspeedKmph"],
            "precip": d["precipMM"],
            "humidity": d["humidity"],
        }
    except Exception:
        return None


def assess_risk(flight, dep_wx, arr_wx):
    status = flight.get("status", "")
    delay = flight.get("delay", 0) or 0

    if status in ("cancelled", "diverted"):
        return "high"

    high_weather_words = ["thunderstorm", "blizzard", "heavy snow"]
    for wx in [dep_wx, arr_wx]:
        if not wx:
            continue
        desc_lower = wx.get("desc_en", wx["desc"]).lower()
        if any(w in desc_lower for w in high_weather_words):
            return "high"
        if float(wx["visibility"]) < 1:
            return "high"
        if int(wx["wind"]) > 65:
            return "high"

    if delay >= 45:
        return "high"

    mid_weather_words = ["rain", "drizzle", "shower", "snow", "sleet", "fog", "mist"]
    for wx in [dep_wx, arr_wx]:
        if not wx:
            continue
        desc_lower = wx.get("desc_en", wx["desc"]).lower()
        if any(w in desc_lower for w in mid_weather_words):
            return "medium"
        if float(wx["visibility"]) < 3:
            return "medium"
        if int(wx["wind"]) > 40:
            return "medium"

    if 15 <= delay < 45:
        return "medium"

    return "low"


def build_advice(flight, risk, dep_wx, arr_wx):
    advice = []
    status = flight.get("status", "")
    delay = flight.get("delay", 0) or 0
    dep_iata = flight.get("dep_iata", "")
    arr_iata = flight.get("arr_iata", "")

    if status == "cancelled":
        advice.append("⚠️ 航班已取消，请勿前往机场。立即联系航空公司客服申请改签或退票。")
    elif status == "diverted":
        advice.append("⚠️ 航班已备降，请关注航空公司通知，了解后续安排。")
    elif status == "landed":
        advice.append("✅ 今日航班已顺利落地，以上数据可作为明日同航班的参考。")
    elif status == "active":
        advice.append("✈️ 航班目前正在飞行中，关注落地时间安排接机或后续交通。")

    if delay >= 45:
        advice.append(f"🕐 当前已延误 {delay} 分钟，建议确认最新起飞时间后再出门。")
    elif delay >= 15:
        advice.append(f"🕐 当前延误 {delay} 分钟，出发时间宽裕可稍等再去机场，但建议持续关注动态。")

    if dep_wx:
        dep_desc_en = dep_wx.get("desc_en", dep_wx["desc"]).lower()
        dep_desc_zh = dep_wx["desc"]
        if "thunderstorm" in dep_desc_en:
            advice.append("⛈ 出发地正在雷暴，机场可能实施流量管控，延误风险较高，建议提前到机场等待。")
        elif any(w in dep_desc_en for w in ["heavy rain", "heavy snow", "blizzard"]):
            advice.append(f"🌧 出发地天气恶劣（{dep_desc_zh}），建议预留充足时间前往机场，路况可能较差。")
        elif any(w in dep_desc_en for w in ["rain", "drizzle", "shower", "fog"]):
            advice.append(f"🌂 出发地{dep_desc_zh}，前往机场请携带雨具，注意路途安全。")

    if arr_wx:
        arr_desc_en = arr_wx.get("desc_en", arr_wx["desc"]).lower()
        arr_desc_zh = arr_wx["desc"]
        if "thunderstorm" in arr_desc_en:
            advice.append("⛈ 目的地正在雷暴，飞机可能无法降落需绕航，建议保持与航空公司联系。")
        elif any(w in arr_desc_en for w in ["heavy rain", "snow", "blizzard", "fog"]):
            advice.append(f"🌦 目的地天气（{arr_desc_zh}）可能影响落地，建议到达后安排弹性交通。")

    if risk == "low" and status == "scheduled":
        large_airports = {"PEK", "PVG", "CAN", "CTU", "KUL", "LHR", "CDG", "JFK", "DXB", "ICN", "SIN", "HKG"}
        medium_airports = {"SHA", "NKG", "HGH", "WUH", "XIY", "NRT", "BKK", "SYD"}
        if dep_iata in large_airports:
            advice.append("🕑 出发地为大型枢纽机场，建议起飞前 2.5–3 小时到达，预留充足安检和步行时间。")
        elif dep_iata in medium_airports:
            advice.append("🕑 建议起飞前 2 小时到达机场，安排好前往机场的交通。")
        else:
            advice.append("🕑 建议起飞前 2 小时到达机场。")

    if status in ("scheduled", "active"):
        advice.append("📱 建议在航空公司 App 或飞常准开启航班动态提醒，有变化第一时间通知。")

    return advice


def packing_advice(wx):
    if not wx:
        return [], []
    bring, skip = [], []
    temp = int(wx["temp"])
    desc = wx.get("desc_en", wx["desc"]).lower()
    humidity = int(wx["humidity"])
    wind = int(wx["wind"])

    if temp >= 33:
        bring += ["轻薄衣物", "防晒霜", "墨镜", "防晒帽"]
        skip += ["外套", "厚衣物"]
    elif temp >= 26:
        bring += ["短袖", "透气衣物"]
        skip += ["厚外套", "羽绒服"]
        if humidity > 75:
            bring.append("薄外套（防室内冷气）")
    elif temp >= 18:
        bring += ["薄外套", "长袖"]
        skip += ["羽绒服", "夏装"]
    elif temp >= 10:
        bring += ["外套", "厚长裤"]
        skip += ["夏装", "短袖"]
    elif temp >= 3:
        bring += ["厚外套", "保暖内衣", "围巾"]
        skip += ["单薄衣物", "短袖"]
    else:
        bring += ["羽绒服", "手套", "围巾", "厚袜子"]
        skip += ["单薄衣物"]

    rain_words = ["rain", "drizzle", "shower", "thunder"]
    snow_words = ["snow", "blizzard", "sleet"]
    if any(w in desc for w in rain_words):
        bring.append("雨伞 / 雨衣")
    else:
        skip.append("雨伞")
    if any(w in desc for w in snow_words):
        bring += ["防滑靴", "保暖手套"]

    if humidity > 80 and temp >= 24:
        bring.append("备用换洗衣物")
    if temp >= 28 and ("clear" in desc or "sunny" in desc):
        if "防晒霜" not in bring:
            bring.append("防晒霜")
    if wind > 40:
        bring.append("防风外套")

    return bring[:6], skip[:4]


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/callback")
def callback():
    token = google.authorize_access_token()
    userinfo = token.get("userinfo") or google.userinfo()
    user_id = userinfo["sub"]
    user = User(
        id=user_id,
        name=userinfo.get("name", ""),
        email=userinfo.get("email", ""),
        picture=userinfo.get("picture", ""),
    )
    _users[user_id] = user
    login_user(user, remember=True)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/history")
def history():
    if not current_user.is_authenticated:
        return jsonify([])
    return jsonify(get_history(current_user.id))


@app.route("/history/<flight>", methods=["DELETE"])
def delete_history(flight):
    if not current_user.is_authenticated:
        return jsonify({"ok": False}), 401
    db = _load_history_db()
    records = db.get(current_user.id, [])
    db[current_user.id] = [r for r in records if r["flight"] != flight.upper()]
    _save_history_db(db)
    return jsonify({"ok": True})


@app.route("/")
def index():
    return render_template("index.html", user=current_user)


@app.route("/query", methods=["POST"])
def query():
    raw = request.json.get("flight", "").strip().upper().replace(" ", "")
    if not raw:
        return jsonify({"error": "请输入航班号"}), 400

    try:
        r = requests.get(
            "http://api.aviationstack.com/v1/flights",
            params={"access_key": AVIATIONSTACK_KEY, "flight_iata": raw},
            timeout=10
        )
        data = r.json()
    except Exception as e:
        return jsonify({"error": f"API 请求失败: {e}"}), 500

    flights = data.get("data", [])
    if not flights:
        return jsonify({"error": f"查不到航班 {raw}，请确认航班号是否正确或今日是否运营"}), 404

    f = flights[0]
    dep = f.get("departure", {})
    arr = f.get("arrival", {})

    dep_iata = dep.get("iata", "")
    arr_iata = arr.get("iata", "")

    flight_info = {
        "number": raw,
        "airline": f.get("airline", {}).get("name", ""),
        "status": f.get("flight_status", ""),
        "delay": dep.get("delay") or 0,
        "dep_iata": dep_iata,
        "dep_airport_en": dep.get("airport", ""),
        "dep_airport_zh": AIRPORT_ZH.get(dep_iata, dep.get("airport", dep_iata)),
        "dep_city": dep.get("city", ""),
        "dep_terminal": dep.get("terminal", ""),
        "dep_gate": dep.get("gate", ""),
        "dep_scheduled": dep.get("scheduled", ""),
        "dep_estimated": dep.get("estimated", ""),
        "dep_actual": dep.get("actual", ""),
        "arr_iata": arr_iata,
        "arr_airport_en": arr.get("airport", ""),
        "arr_airport_zh": AIRPORT_ZH.get(arr_iata, arr.get("airport", arr_iata)),
        "arr_city": arr.get("city", ""),
        "arr_terminal": arr.get("terminal", ""),
        "arr_baggage": arr.get("baggage", ""),
        "arr_scheduled": arr.get("scheduled", ""),
        "arr_estimated": arr.get("estimated", ""),
        "arr_actual": arr.get("actual", ""),
    }

    dep_wx = get_weather(flight_info["dep_city"], dep_iata)
    arr_wx = get_weather(flight_info["arr_city"], arr_iata)

    risk = assess_risk(flight_info, dep_wx, arr_wx)
    advice = build_advice(flight_info, risk, dep_wx, arr_wx)
    bring, skip = packing_advice(arr_wx)

    if current_user.is_authenticated:
        push_history(current_user.id, {
            "flight": raw,
            "queried_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "airline": flight_info["airline"],
            "dep_iata": flight_info["dep_iata"],
            "arr_iata": flight_info["arr_iata"],
            "risk": risk,
        })

    return jsonify({
        "flight": flight_info,
        "dep_weather": dep_wx,
        "arr_weather": arr_wx,
        "risk": risk,
        "advice": advice,
        "bring": bring,
        "skip": skip,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
