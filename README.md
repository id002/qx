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
├── filters/                分流规则本地备份目录
├── rewrites/               重写规则本地备份目录
├── scripts/                脚本本地备份目录
└── _source/                墨鱼原始参考（README + 自用配置）
```

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
