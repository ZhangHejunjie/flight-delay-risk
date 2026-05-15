# 机场 IATA → wttr.in 查询名称映射

wttr.in 使用 IATA 代码查询时偶尔会解析到错误地点。优先使用 AviationStack 返回的 `departure.city` / `arrival.city` 字段直接查询；如果该字段为空，用下表的映射名称作为备用。

查询格式：`https://wttr.in/{查询名称}?format=j1`

---

## 中国大陆

| IATA | 机场名 | wttr.in 查询名 |
|------|--------|----------------|
| PEK | 北京首都 | Beijing |
| PKX | 北京大兴 | Beijing |
| SHA | 上海虹桥 | Shanghai |
| PVG | 上海浦东 | Shanghai |
| CAN | 广州白云 | Guangzhou |
| SZX | 深圳宝安 | Shenzhen |
| CTU | 成都天府 | Chengdu |
| TFU | 成都双流 | Chengdu |
| KMG | 昆明长水 | Kunming |
| XIY | 西安咸阳 | Xian |
| WUH | 武汉天河 | Wuhan |
| NKG | 南京禄口 | Nanjing |
| HGH | 杭州萧山 | Hangzhou |
| XMN | 厦门高崎 | Xiamen |
| FOC | 福州长乐 | Fuzhou |
| CSX | 长沙黄花 | Changsha |
| DLC | 大连周水子 | Dalian |
| SHE | 沈阳桃仙 | Shenyang |
| HRB | 哈尔滨太平 | Harbin |
| CGQ | 长春龙嘉 | Changchun |
| TSN | 天津滨海 | Tianjin |
| TAO | 青岛胶东 | Qingdao |
| JJN | 泉州晋江 | Quanzhou |
| NGB | 宁波栎社 | Ningbo |
| WNZ | 温州龙湾 | Wenzhou |
| KRY | 克拉玛依 | Karamay |
| URC | 乌鲁木齐地窝堡 | Urumqi |
| LHW | 兰州中川 | Lanzhou |
| INC | 银川河东 | Yinchuan |
| HET | 呼和浩特白塔 | Hohhot |
| TYN | 太原武宿 | Taiyuan |
| SJW | 石家庄正定 | Shijiazhuang |
| ZHA | 湛江 | Zhanjiang |
| SWA | 汕头揭阳潮汕 | Shantou |
| KHN | 南昌昌北 | Nanchang |
| KWE | 贵阳龙洞堡 | Guiyang |
| NNG | 南宁吴圩 | Nanning |
| HAK | 海口美兰 | Haikou |
| SYX | 三亚凤凰 | Sanya |
| LXA | 拉萨贡嘎 | Lhasa |
| RIZ | 日照山字河 | Rizhao |

## 港澳台

| IATA | 机场名 | wttr.in 查询名 |
|------|--------|----------------|
| HKG | 香港赤鱲角 | Hong+Kong |
| MFM | 澳门 | Macau |
| TPE | 台北桃园 | Taipei |
| TSA | 台北松山 | Taipei |
| KHH | 高雄小港 | Kaohsiung |

## 亚太

| IATA | 机场名 | wttr.in 查询名 |
|------|--------|----------------|
| NRT | 东京成田 | Tokyo |
| HND | 东京羽田 | Tokyo |
| KIX | 大阪关西 | Osaka |
| ITM | 大阪伊丹 | Osaka |
| ICN | 首尔仁川 | Seoul |
| GMP | 首尔金浦 | Seoul |
| SIN | 新加坡樟宜 | Singapore |
| BKK | 曼谷素万那普 | Bangkok |
| DMK | 曼谷廊曼 | Bangkok |
| KUL | 吉隆坡 | Kuala+Lumpur |
| CGK | 雅加达苏加诺 | Jakarta |
| MNL | 马尼拉 | Manila |
| SGN | 胡志明市 | Ho+Chi+Minh |
| HAN | 河内 | Hanoi |
| SYD | 悉尼 | Sydney |
| MEL | 墨尔本 | Melbourne |
| AKL | 奥克兰 | Auckland |
| DEL | 德里英迪拉甘地 | Delhi |
| BOM | 孟买 | Mumbai |
| DXB | 迪拜 | Dubai |
| AUH | 阿布扎比 | Abu+Dhabi |
| DOH | 多哈 | Doha |

## 欧洲

| IATA | 机场名 | wttr.in 查询名 |
|------|--------|----------------|
| LHR | 伦敦希思罗 | London |
| LGW | 伦敦盖特威克 | London |
| CDG | 巴黎戴高乐 | Paris |
| ORY | 巴黎奥利 | Paris |
| FRA | 法兰克福 | Frankfurt |
| MUC | 慕尼黑 | Munich |
| AMS | 阿姆斯特丹史基浦 | Amsterdam |
| MAD | 马德里 | Madrid |
| BCN | 巴塞罗那 | Barcelona |
| FCO | 罗马菲乌米奇诺 | Rome |
| MXP | 米兰马尔彭萨 | Milan |
| ZRH | 苏黎世 | Zurich |
| VIE | 维也纳 | Vienna |
| CPH | 哥本哈根 | Copenhagen |
| ARN | 斯德哥尔摩 | Stockholm |
| HEL | 赫尔辛基 | Helsinki |
| OSL | 奥斯陆 | Oslo |
| IST | 伊斯坦布尔 | Istanbul |
| SVO | 莫斯科谢列梅捷沃 | Moscow |

## 北美洲

| IATA | 机场名 | wttr.in 查询名 |
|------|--------|----------------|
| JFK | 纽约肯尼迪 | New+York |
| LGA | 纽约拉瓜迪亚 | New+York |
| EWR | 纽瓦克 | Newark |
| LAX | 洛杉矶 | Los+Angeles |
| ORD | 芝加哥奥黑尔 | Chicago |
| ATL | 亚特兰大 | Atlanta |
| DFW | 达拉斯沃思堡 | Dallas |
| SFO | 旧金山 | San+Francisco |
| SEA | 西雅图 | Seattle |
| BOS | 波士顿 | Boston |
| MIA | 迈阿密 | Miami |
| YYZ | 多伦多皮尔逊 | Toronto |
| YVR | 温哥华 | Vancouver |
| YUL | 蒙特利尔 | Montreal |
| MEX | 墨西哥城 | Mexico+City |

## 使用说明

1. **优先用 AviationStack 返回的城市名**：响应中 `departure.city` / `arrival.city` 字段通常最准确，直接用该值查 wttr.in。
2. **其次用上表映射**：如果 city 字段为空或不明确，用 IATA 查上表。
3. **最后才用原始 IATA**：如果上表也没有，直接用 IATA 代码尝试，但可能有解析偏差。
4. **城市名含空格时用 `+` 替换**：如 `Los+Angeles`、`Hong+Kong`。
