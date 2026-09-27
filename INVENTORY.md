# QuantumultX 规则仓库清单

> 生成日期：2026-09-26 ｜ 仓库：`github.com/id002/qx`（public） ｜ 提交署名：匿名邮箱（无隐私泄露）

## 一、仓库概览

| 项目 | 内容 |
|---|---|
| 远程仓库 | `git@github.com:id002/qx.git`（public） |
| raw 前缀 | `https://raw.githubusercontent.com/id002/qx/master/` |
| 提交历史 | 4 个提交（init → 英文短路径+校验工具 → HTML 清理 → 重复清理） |
| 提交身份 | `id002 <95127491+id002@users.noreply.github.com>`（已匿名化） |
| 当前 HEAD | `2c80330`（合并汽水音乐后待推送） |
| 主要资产 | 重写 857 条 ／ 分流 210,134 条 ／ 脚本 10 个 ／ 配置 3 个 |

## 二、重写规则 rewrites/（27 个文件，共 857 条有效行）

> 口径：有效规则行 = `^` 开头且非禁用注释（`#^` / `;`）的行。2026-09-27 更新。

### App 净化（按 App 单独同步）
| 文件 | 条数 | 用途 |
|---|---|---|
| startup-ads.conf | 473 | 墨鱼去开屏 V2.0 全量（大表） |
| q-search.conf | 83 | Safari 快捷搜索引擎命令 |
| weibo.conf | 42 | 微博去广告 |
| netease.conf | 29 | 网易云音乐净化 |
| bilibili.conf | 27 | B站完整净化（信息流+开屏+会员购） |
| xiaohongshu.conf | 25 | 小红书净化+去水印 |
| ximalaya.conf | 24 | 喜马拉雅净化 |
| amap.conf | 18 | 高德地图净化（需卸载重装） |
| keep.conf | 17 | Keep 去广告 |
| qi-shui-music.conf | 16 | 汽水音乐净化（穿山甲SDK+luna接口整合） |
| aisi.conf | 4 | 爱思助手去广告（主界面+开屏接口+广告图） |
| goofish.conf | 14 | 闲鱼净化（需卸载重装） |
| smzdm.conf | 13 | 什么值得买净化 |
| caiyun.conf | 12 | 彩云天气净化 |
| china-unicom.conf | 10 | 中国联通净化 |
| bilibili-lite.conf | 8 | B站净化精简版（与 bilibili.conf 二选一） |
| tieba.conf | 7 | 百度贴吧去广告 |
| netease-mail.conf | 7 | 网易邮箱大师净化 |
| youtube.conf | 5 | YouTube 去广告 |
| xiaoyuzhou.conf | 5 | 小宇宙 FM 去广告 |
| applet.conf | 5 | 微信小程序去除广告 |
| duolingo.conf | 5 | 多邻国去广告（学习后视频/插屏） |
| da-shi-xiong.conf | 4 | 大师兄影视净化+影视公告去弹窗 |
| reddit.conf | 1 | Reddit 增强去广告 |
| wechat-unblock.conf | 1 | 微信解锁被屏蔽 URL |
| google-redirect.conf | 1 | Google 搜索重定向 |
| douban.conf | 1 | 豆瓣移动网页去广告+快捷观影 |

## 三、分流规则 filters/（12 个文件，共 210,134 条有效行）

| 文件 | 条数 | 用途 |
|---|---|---|
| adrules.conf | 202,170 | AdRules 广告域名大表（host-suffix reject） |
| china-asn.list | 5,076 | 中国大陆 IP-ASN 直连 |
| apple.list | 1,881 | Apple 服务分流 |
| global-proxy.list | 512 | 全球代理域名 |
| streaming.list | 256 | 流媒体（Netflix/Disney+ 等） |
| ai.yaml | 92 | AI 服务分流策略 |
| wechat.list | 43 | 微信/WeChat 分流 |
| unbreak.list | 31 | 防误杀（直连白名单） |
| github.list | 31 | GitHub 分流 |
| spotify.list | 30 | Spotify 分流 |
| streaming-se.list | 11 | 流媒体（新加坡区） |
| google-voice.list | 1 | Google Voice 分流 |

## 四、脚本 scripts/（10 个 .js）

| 文件 | 用途 |
|---|---|
| zhihu.ads.js | 知乎净化（信息流广告） |
| netEase.adblock.js | 网易云广告拦截 |
| jd_price.js | 京东价格查询 |
| kkmusic.vip.js | 酷狗/QQ 音乐 VIP 解锁 |
| bdpan.ads.js | 百度网盘净化 |
| 12306.js | 12306 广告拦截 |
| coolapk.js | 酷安净化 |
| pixivAds.js | Pixiv 广告拦截 |
| bdpan.unlock.js | 百度网盘倍速 |
| youtube.response.js | YouTube 响应处理 |

## 五、配置文件（3 个）

| 文件 | 说明 |
|---|---|
| MyProfile.conf | 主配置：订阅占位 + 策略 + 分流 + 重写引用 + MITM |
| MyAdBlock.conf | 本地全量去广告重写合集（792 条，大而全备份） |
| test.conf | 墨鱼去开屏原版副本 |

## 六、知识库归档 QX-Knowledge/

- `00-原始资料/`：墨鱼规则全集、脚本、教程等原始归档
- `01-整理笔记/`：规则整理笔记
- `02-规则模板/`：可复用模板

> 归档层与使用层（rewrites/）内容重叠属设计：归档保留原始文件，使用层按 App 拆分。

## 七、校验工具 _source/

| 文件 | 用途 |
|---|---|
| validate_rules.py | 规则语法校验（重写 0 错误 / 警告 6） |
| dedupe_check.py | 重复检测（文件内+跨文件） |
| dedupe_apply.py | 文件内重复自动清理 |
| dedupe-report.txt | 最近一次去重报告 |

## 八、维护命令备忘

```powershell
# 规则校验
python _source\validate_rules.py
# 重复检测
python _source\dedupe_check.py
# 文件内去重（清理后需重新校验）
python _source\dedupe_apply.py
# 同步推送
git add -A; git commit -m "chore: 同步更新"; git push origin master
```
