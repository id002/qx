# QuantumultX 专属规则库

基于 **墨鱼手记（@ddgksf2013）** 2026-09 最新规则库定制的 QuantumultX 规则集合。

> 规则来源：https://github.com/ddgksf2013/ddgksf2013 ｜ TG 频道：https://t.me/ddgksf2021

---

## 目录结构

```
QuantumultX/
├── MyProfile.conf          ★ 主配置文件（导入 QX 用这个）
├── README.md               本文件
├── docs/
│   ├── 操作手册.md          从零开始的安装/导入/证书教程
│   └── 规则清单.md          所有启用规则的详细说明
├── filters/                分流规则（英文短名，手机可直接引用）
├── rewrites/               重写规则（英文短名，手机可直接引用）
├── scripts/                脚本（英文短名，手机可直接引用）
├── _source/                墨鱼原始参考 + 校验脚本 validate_rules.py
└── QX-Knowledge/           规则知识库（全量原始规则存档）
```

## 手机直接引用（GitHub raw 短路径）

仓库地址：`https://github.com/id002/qx`，raw 前缀：`https://raw.githubusercontent.com/id002/qx/master/`

**常用重写规则（rewrites/）**

| 文件 | 说明 |
|------|------|
| `rewrites/startup-ads.conf` | 墨鱼去开屏 2.0（全量开屏广告） |
| `rewrites/da-shi-xiong.conf` | 大师兄影视净化+影视公告去弹窗（整合版） |
| `rewrites/qi-shui-music.conf` | 汽水音乐净化（穿山甲SDK+luna接口整合） |
| `rewrites/aisi.conf` | 爱思助手去广告（主界面+开屏接口+广告图） |
| `rewrites/duolingo.conf` | 多邻国PLUS插屏/开屏拦截 |
| `rewrites/applet.conf` | 微信小程序去广告 |
| `rewrites/bilibili.conf` / `bilibili-lite.conf` | B站净化（完整/Lite） |
| `rewrites/youtube.conf` | YouTube 去广告 |
| `rewrites/weibo.conf` | 微博去广告 |
| `rewrites/amap.conf` | 高德地图净化 |
| `rewrites/netease.conf` | 网易云净化 |
| `rewrites/goofish.conf` | 闲鱼净化 |
| `rewrites/xiaohongshu.conf` | 小红书净化+去水印 |
| `rewrites/caiyun.conf` / `tieba.conf` / `keep.conf` / `smzdm.conf` / `reddit.conf` | 其他常用净化 |

**常用分流（filters/）**：`adrules.conf`（广告终结者）、`china-asn.list`（国内直连）、`apple.list`（苹果服务）、`streaming.list` / `streaming-se.list`（国际媒体/B站）、`ai.yaml`（AI分流）、`github.list`、`wechat.list`、`spotify.list`、`global-proxy.list`、`unbreak.list`（反误杀）、`google-voice.list`

**常用脚本（scripts/）**：`zhihu.ads.js`、`bdpan.ads.js`（网盘净化）、`bdpan.unlock.js`（网盘倍速）、`kkmusic.vip.js`、`youtube.response.js` 等

QX 里添加远程资源时填完整 raw URL 即可，例如：
```
https://raw.githubusercontent.com/id002/qx/master/rewrites/da-shi-xiong.conf
```

## 收藏夹页面（规则一键添加）

手机浏览器打开 **https://id002.github.io/qx/** （备用：doubao-html https://4m2rky2nqrx2q.doubaoapps.com/app/app_17eyfzdqu00 ），点卡片「添加到 QX」自动跳转 App 预填远程资源，或「复制」拿 raw 链接。

### 点击计数（每规则）

每张卡片显示「已点击 N 次」，取 **云端全局数** 与 **本机数** 的较大值。

- **云端服务**：`countapi.mileshilliard.com`（开源免费计数 API，零注册零认证）
  - 自增：`GET https://countapi.mileshilliard.com/api/v1/hit/{key}` → `{"value":N}`
  - 只读：`GET https://countapi.mileshilliard.com/api/v1/get/{key}` → `{"value":N}`（key 不存在返回 404，页面静默忽略）
  - key 规则：`id002-qx-` + 规则文件名（如 `id002-qx-qi-shui-music.conf`），URL 编码后拼接
- **本地兜底**：localStorage 键 `qx_clicks`（`{file: 次数}`），云端不可用时页面照常计数
- **页面代码位置**：`index.html` 中 `CNT_NS` / `cntUrl()` / `cloudFetch()` / `cloudBump()` / `clickOf()` / `bump()`

### 已实测排除的后端（维护时别走回头路）

| 方案 | 结论 |
|------|------|
| LeanCloud（国际/国内版） | 2026-01 起停新注册，2027-01 整体停服，不可用 |
| CounterAPI（counterapi.com） | 只读接口失灵、同 IP 同 key 防刷限一次，不可靠 |
| countapi.xyz | DNS 已失效（服务下线） |
| Supabase | 国内被墙（连接被重置） |
| 腾讯云 CloudBase / 国内云 | 需实名认证 + 免费体验版续期复杂，未采用 |

## 快速上手（3 步）

1. **改订阅**：打开 `MyProfile.conf`，找到 `[server_remote]` 段，把占位的订阅链接换成你自己机场的订阅。
2. **导入 QX**：把 `MyProfile.conf` 内容粘贴到 QX「配置」→「编辑」，或把文件放到 iCloud/网盘中用 QX 打开。
3. **装证书**：按 `docs/操作手册.md` 第 4 步安装并信任 MITM 证书，去广告功能才会生效。

## 已启用功能一览

| 分类 | 功能 |
|------|------|
| 会员解锁 | 哔哩哔哩广告净化、Spotify 音乐 VIP |
| 广告拦截 | 墨鱼去开屏 2.0、彩云天气、知乎、YouTube、微博、高德地图、网易云、闲鱼 |
| 网页优化 | Safari 超级搜索、豆瓣观影跳转、Google 重定向 |
| 功能增强 | 小红书去水印、百度网盘净化+倍速、微信解锁被屏蔽 URL、BoxJS |
| 智能分流 | 国内直连、苹果服务、国际流媒体、AI/GitHub 走美区、Spotify 专用 |
| 工具 | 流媒体解锁查询、节点纯净度查询 |

## 日常维护

- **更新规则**：QX 里下拉刷新配置即可，远程规则按 `update-interval` 自动更新。
- **开关功能**：改对应行末尾 `enabled=true` 为 `false`。
- **新增规则**：去 https://ddgksf2013.top 或 README 索引里挑，追加到 `[rewrite_remote]` 或 `[filter_remote]`。
- **反馈误杀**：被规则误拦的网站，把域名加到 `[filter_local]` 里 `host, 域名, direct`。

## 致谢

规则作者：@ddgksf2013、@KOP-XIAO、@blackmatrix7、@app2smile、@DivineEngine、@zZPiglet、@chavyleung、@Orz-3、@VirgilClyne 等，详见墨鱼原 README。
