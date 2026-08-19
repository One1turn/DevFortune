#!/usr/bin/env python3
"""
🔮 DevFortune — 开发者代码占卜
通过分析 GitHub 公开数据生成开发者运势报告
"""

import sys
import random
import urllib.request
import json
from datetime import datetime, timezone

FORTUNE_LEVELS = [
    ("SSR", "✨ 今天你写的每一行代码都会是优雅的"),
    ("S",   "🌟 灵感爆棚的日子，bug 看到你会自己改"),
    ("A",   "🐛 今天遇到的 bug 都是你自己写的，改起来很快"),
    ("B",   "📝 适合写文档和重构，不适合写新功能"),
    ("C",   "😅 今天代码能跑就行，别追求优雅"),
    ("D",   "💀 今天最好别碰生产环境，真的"),
]

LANG_PERSONALITIES = {
    "Python":     '你是那种"能 import 就不手写"的人',
    "JavaScript": '你是"console.log 大法好"的信徒',
    "TypeScript": '你活着就是为了消灭 any 类型',
    "Java":       '你以为自己是面向对象大师，其实只是个 @Autowired 注入器',
    "C":          '你背得过 malloc 的签名但记不住老婆生日',
    "C++":        '你用了 10 年还没搞懂 std::move 到底 move 了什么',
    "Go":         '你的 if err != nil 比 main 函数还长',
    "Rust":       '你花在跟编译器吵架上的时间比写代码还多',
    "Shell":      '你的脚本只有你能看懂，包括你自己三天后',
    "PHP":         '你偷偷写 PHP 但告诉别人你在做"后端"',
    "Ruby":        '你觉得世界上最美的事就是读自己的代码',
    "Swift":       '你还在等 optional 解包的人生答案',
    "Kotlin":      '你不是在写代码，你是在跟 Java 证明自己更优雅',
    "HTML":       '你跟设计师吵架的时间比写标签还长',
    "CSS":        '你的一生都在 center 一个 div',
    "Lua":        '你的 index 从 1 开始，你与众不同',
    "Haskell":    '你写了一段没人看得懂的 monad 来证明纯函数的力量',
    "Other":      '你是个有趣的人，用着没人听过的语言',
}

LUCKY_FRAMEWORKS = [
    "FastAPI", "React", "Vue", "Next.js", "Flask", "Spring Boot",
    "Express", "Django", "Flutter", "Tailwind CSS", "Svelte",
    "Electron", "Astro", "Three.js", "Bun", "Tauri"
]

LUCKY_COLORS = [
    "#61DAFB", "#3776AB", "#F7DF1E", "#ED8B00", "#00ADD8",
    "#3178C6", "#DEA584", "#A53B6", "#777BB4", "#375EAB",
]

WARNINGS = [
    "不要在生产环境 rm -rf",
    "不要相信\"这个小改一下就行\"",
    "不要在周五下午 deploy",
    "不要跳过 code review",
    "不要在忘记密码时直接改数据库",
    "不要 git push --force 到 main 分支",
    "不要把 API key 提交到 GitHub",
    "不要在有 merge conflict 时 force push",
    "不要用 var，都 2026 了",
    "不要在注释里骂同事",
]

FORTUNE_TIPS = [
    "今天的 pull request 会被一次 merge 通过 ✨",
    "今天你会发现一个让代码快 10 倍的优化",
    "今天有个资深 dev 会夸你的 commit message",
    "今天你写的测试会一次通过",
    "今天你会轻松解决一个困扰三天的 bug",
    "今天 audit 提出的建议，你真的会改",
    "今日适合重构，但只重构一个文件",
    "今日不宜写正则表达式",
    "今天你会学会一个新的快捷键",
    "今天你的编译会一次过",
]


def fetch_github_user(username):
    url = f"https://api.github.com/users/{username}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DevFortune",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"error": "GitHub 用户不存在！检查拼写喵~"}
        return {"error": f"GitHub API 报错：HTTP {e.code}"}
    except Exception as e:
        return {"error": f"请求失败：{e}"}


def fetch_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DevFortune",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return []


def setupSeed(username):
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    seed = hash(f"{username}{today}") & 0xFFFFFFFF
    random.seed(seed)


def buildReport(username):
    setupSeed(username)

    user = fetch_github_user(username)
    if "error" in user:
        print(f"\n❌ {user['error']}")
        return

    repos = fetch_github_repos(username)

    # 统计语言
    lang_counts = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

    top_lang = max(lang_counts, key=lang_counts.get) if lang_counts else "Other"

    # 运势
    luck_idx = random.randint(0, len(FORTUNE_LEVELS) - 1)
    luck_level, luck_desc = FORTUNE_LEVELS[luck_idx]

    lucky_fw = random.choice(LUCKY_FRAMEWORKS)
    lucky_color = random.choice(LUCKY_COLORS)
    lucky_num = random.randint(1, 99)
    warnings = random.sample(WARNINGS, min(3, len(WARNINGS)))
    tip = random.choice(FORTUNE_TIPS)

    personality = LANG_PERSONALITIES.get(top_lang, LANG_PERSONALITIES["Other"])

    # 午夜 commit 推测
    midnight_pct = random.randint(15, 65)

    print(f"\n🔮 正在占卜 {username} 的开发运势...\n")
    print("═" * 45)
    print(f"  DevFortune — 开发者运势报告")
    print(f"  占卜对象: {username}")
    print("═" * 45)
    print()
    print(f"⭐ 综合运势: {luck_level}")
    print(f"  {luck_desc}")
    print()
    print("💻 开发者属性:")
    print(f"  主语言 {top_lang} — {personality}")
    print(f"  commit 午夜占比 {midnight_pct}% — 众所周知，bug 只在深夜诞生")
    print()
    print(f"🍀 今日幸运框架: {lucky_fw}")
    print(f"🎨 今日幸运颜色: {lucky_color}")
    print(f"🔢 今日幸运数字: {lucky_num}")
    print()
    print("⚠️ 今日避雷:")
    for w in warnings:
        print(f"  - {w}")
    print()
    print("📈 GitHub 数据:")
    print(f"  公开仓库: {user.get('public_repos', '?')} 个")
    print(f"  followers: {user.get('followers', '?')} 人")
    print()
    print(f"命运提示: {tip}")
    print("═" * 45)


def main():
    if len(sys.argv) < 2:
        print("Usage: python devfortune.py <GitHub用户名>")
        print("Example: python devfortune.py torvalds")
        sys.exit(1)

    username = sys.argv[1].strip()
    if not username:
        print("❌ 用户名不能为空")
        sys.exit(1)

    buildReport(username)


if __name__ == "__main__":
    main()
