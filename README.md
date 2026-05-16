# ✈️ 航班延误风险助手

输入航班号，实时查询延误风险、接机指引、两地天气与 AI 生成的目的地旅行指南。

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Flask](https://img.shields.io/badge/Flask-3.x-green) ![Railway](https://img.shields.io/badge/Deploy-Railway-blueviolet)

**线上体验：** [https://flight-delay-risk-production-58b5.up.railway.app](https://flight-delay-risk-production-58b5.up.railway.app)

---

## 功能

| 功能 | 说明 |
|------|------|
| 🎫 **登机牌卡片** | 航班信息以登机牌样式呈现，大字 IATA 代码、中文城市名、飞行时长一目了然 |
| 📊 **实时飞行进度** | 飞行中航班实时显示已飞时间、剩余时间与百分比，正确处理各时区本地时间 |
| ⏱ **延误状态** | 起飞/落地延误以分钟/小时展示，颜色高亮（🟡 延误 / 🟢 提早）|
| 🚨 **风险评级** | 综合航班状态与两地天气，给出 🟢低 / 🟡中 / 🔴高 三级风险评级及具体建议 |
| 🚗 **接机指引** | 预计落地时间、等候航站楼、出关时长估算（国内/国际）、状态感知提示 |
| 🌤 **两地实时天气** | 出发地与目的地温度、体感、湿度、能见度、风速、降水，描述全中文 |
| 🎒 **AI 行李建议** | GPT-4o-mini 根据目的地实时天气，推荐带什么、不需要带什么 |
| 🗺 **AI 目的地指南** | AI 生成当地必去景点 Top 3、必吃美食 Top 3 及交通小贴士，覆盖全球任意城市 |
| 🔐 **Google 登录** | 支持 Google OAuth 登录，自动保存最近 15 条查询历史 |
| 🔄 **自动刷新** | 飞行中航班每 60 秒自动拉取最新数据 |

---

## 快速开始

### 1. 获取 API Key

- **AviationStack**：前往 [aviationstack.com](https://aviationstack.com) 注册，获取免费 Key（100 次/月）
- **OpenAI**：前往 [platform.openai.com](https://platform.openai.com) 获取 API Key（用于 AI 行李建议与目的地指南）

### 2. 克隆项目

```bash
git clone https://github.com/ZhangHejunjie/flight-delay-risk.git
cd flight-delay-risk
```

### 3. 安装依赖

```bash
pip install -r web/requirements.txt
```

### 4. 配置环境变量

在 `web/` 目录下创建 `.env` 文件（可参考 `web/.env.example`）：

```env
AVIATIONSTACK_KEY=你的AviationStack_Key
OPENAI_API_KEY=你的OpenAI_Key
SECRET_KEY=任意随机字符串

# Google OAuth（可选，不填则关闭登录功能）
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### 5. 启动

```bash
python web/app.py
```

打开浏览器访问 `https://flight-delay-risk-production-58b5.up.railway.app/`

> **注意**：未配置 `OPENAI_API_KEY` 时，AI 行李建议和目的地指南会自动回退到内置静态数据（覆盖 70+ 城市）。

---

## 部署到 Railway

1. Fork 本仓库
2. 在 [Railway](https://railway.app) 新建项目，连接该仓库
3. 在 Railway Variables 中设置环境变量：

```
AVIATIONSTACK_KEY=...
OPENAI_API_KEY=...
SECRET_KEY=...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

4. Railway 自动构建部署，访问分配的域名即可

> Google OAuth 回调地址需在 [Google Cloud Console](https://console.cloud.google.com) 中添加 `https://你的域名/callback`

---

## 风险评级逻辑

| 评级 | 触发条件 |
|------|---------|
| 🔴 高风险 | 航班取消/备降、延误 ≥ 45 分钟、雷暴/暴风雪、能见度 < 1 km、风速 > 65 km/h |
| 🟡 中等风险 | 延误 15–44 分钟、中大雨/小雪/雾、能见度 1–3 km、风速 40–65 km/h |
| 🟢 低风险 | 无延误、两地天气晴好、能见度 > 3 km |

出发地和目的地天气均纳入评估——目的地雷暴同样可能导致飞机无法降落。

---

## 项目结构

```
flight-delay-risk/
├── web/
│   ├── app.py              # Flask 后端（路由、API 调用、风险与接机逻辑）
│   ├── requirements.txt    # Python 依赖
│   ├── templates/
│   │   └── index.html      # 前端页面（CSS + JS 全内联）
│   ├── data/
│   │   └── history.json    # 用户查询历史（本地）
│   └── .env.example        # 环境变量模板
├── SKILL.md                # Claude Code skill 配置
├── railway.toml            # Railway 部署配置
└── requirements.txt        # 根目录依赖（Railway 入口）
```

---

## 技术栈

- **后端**：Python / Flask、Authlib（Google OAuth）、Flask-Login、zoneinfo + tzdata（时区处理）
- **前端**：原生 HTML + CSS + JavaScript（无框架）
- **航班数据**：[AviationStack API](https://aviationstack.com)
- **天气数据**：[wttr.in](https://wttr.in)（无需 Key）
- **AI 功能**：[OpenAI GPT-4o-mini](https://platform.openai.com)
- **部署**：[Railway](https://railway.app)

---

## 数据说明

- AviationStack 免费版每月限 100 次请求，仅支持当日航班
- 天气数据由 wttr.in 提供，无需 API Key
- 查询历史存储在服务器本地 `web/data/history.json`，按 Google 账号隔离
- 未提供 OpenAI Key 时自动使用内置 70+ 城市静态指南

---

## License

MIT
