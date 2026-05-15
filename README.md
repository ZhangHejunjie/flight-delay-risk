# ✈️ 航班延误风险助手

输入航班号，实时查询延误风险、两地天气与目的地旅行指南。

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-3.x-green) ![Railway](https://img.shields.io/badge/Deploy-Railway-blueviolet)

---

## 功能亮点

| 功能 | 说明 |
|------|------|
| 🎫 **登机牌式卡片** | 航班信息以登机牌样式呈现，大字 IATA 代码、中文城市名、飞行时长一目了然 |
| 📊 **飞行进度条** | 飞行中航班实时显示已飞时间、剩余时间和百分比，流光动画指示实时状态 |
| ⏱ **延误状态** | 起飞/落地延误或提早分别以分钟/小时展示，并带颜色高亮（黄=延误，绿=提早）|
| 🌤 **两地实时天气** | 出发地与目的地温度、体感温度、湿度、能见度、风速、降水，描述全中文 |
| 🚨 **延误风险评级** | 综合航班数据与两地天气，给出 🟢低 / 🟡中 / 🔴高 三级风险评级及具体建议 |
| 🎒 **目的地携带建议** | 按目的地天气动态推荐带什么、不用带什么 |
| 🗺 **目的地旅行指南** | 到达城市的必去景点 Top 3、必吃美食 Top 3 及当地小贴士（覆盖全球 70+ 城市）|
| 🔐 **Google 登录** | 支持 Google OAuth 登录，自动保存最近 15 条查询历史 |
| 🔄 **自动刷新** | 飞行中航班每 60 秒自动拉取最新数据 |

---

## 快速开始

### 1. 获取 API Key

前往 [AviationStack](https://aviationstack.com) 注册免费账号，获取 API Key（免费版每月 100 次请求）。

### 2. 克隆项目

```bash
git clone https://github.com/ZhangHejunjie/flight-delay-risk.git
cd flight-delay-risk
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在 `web/` 目录下创建 `.env` 文件：

```env
AVIATIONSTACK_KEY=你的AviationStack_Key
SECRET_KEY=任意随机字符串

# Google OAuth（可选，不填则关闭登录功能）
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
OAUTHLIB_INSECURE_TRANSPORT=1
```

### 5. 启动

```bash
python web/app.py
```

打开浏览器访问 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 部署到 Railway

本项目已配置 Railway 一键部署。

1. Fork 本仓库
2. 在 [Railway](https://railway.app) 新建项目，连接该仓库
3. 在 Railway 的 Variables 中设置以下环境变量：

```
AVIATIONSTACK_KEY=...
SECRET_KEY=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

4. Railway 会自动构建并部署，访问分配的域名即可

> Google OAuth 回调地址需在 [Google Cloud Console](https://console.cloud.google.com) 中添加 `https://你的域名/auth/callback`

---

## 风险评级逻辑

| 评级 | 触发条件 |
|------|---------|
| 🔴 高风险 | 航班已取消/备降、延误 ≥ 45 分钟、雷暴/暴风雪、能见度 < 1 km、风速 > 65 km/h |
| 🟡 中等风险 | 延误 15–44 分钟、中大雨/小雪、能见度 1–3 km、风速 40–65 km/h |
| 🟢 低风险 | 无延误、两地天气晴好、能见度 > 3 km |

出发地和目的地天气均纳入评估——目的地雷暴同样可能导致飞机无法降落。

---

## 项目结构

```
flight-delay-risk/
├── web/
│   ├── app.py                # Flask 后端（路由、API 调用、风险逻辑）
│   ├── templates/
│   │   └── index.html        # 前端页面（CSS + JS 全内联）
│   └── data/
│       └── history.json      # 用户查询历史（本地存储）
├── references/
│   └── airports.md           # IATA 代码 → 城市名映射
├── evals/
│   └── evals.json            # 测试用例
├── SKILL.md                  # Claude Code skill 配置
├── railway.toml              # Railway 部署配置
└── requirements.txt          # Python 依赖
```

---

## 技术栈

- **后端**：Python / Flask、Authlib（Google OAuth）、Flask-Login
- **前端**：原生 HTML + CSS + JavaScript（无框架）
- **航班数据**：[AviationStack API](https://aviationstack.com)
- **天气数据**：[wttr.in](https://wttr.in)
- **部署**：[Railway](https://railway.app)

---

## 数据说明

- 免费版 AviationStack 每月限 100 次请求，仅支持当日航班
- 天气数据由 wttr.in 提供，无需 API Key
- 查询历史存储在服务器本地 `web/data/history.json`，按 Google 账号隔离

---

## License

MIT
