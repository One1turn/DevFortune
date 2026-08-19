# 🔮 DevFortune — 开发者代码占卜

> 输入你的 GitHub 用户名，用你的 commit 历史、语言分布和活跃时间算一卦。

## 这是什么？

DevFortune 是一个 Python 脚本，它通过分析你的 GitHub 公开数据来生成一份"开发者运势报告"：
- 🎯 今日开发运势（SSR/S/A/B/C/D评级）
- 💻 你的主语言决定了你的性格属性
- ⏰ commit 时间分布揭示你的作息真相
- 🍀 今日幸运框架
- ⚠️ 今日避雷指南

## 安装

```bash
git clone https://github.com/One1turn/DevFortune.git
cd DevFortune
pip install -r requirements.txt
```

## 使用

```bash
python devfortune.py <你的GitHub用户名>
```

例如：
```bash
python devfortune.py torvalds
```

## 示例输出

```
🔮 正在占卜 One1turn 的开发运势...

═══════════════════════════════════════
  DevFortune — 开发者运势报告
  占卜对象: One1turn
═══════════════════════════════════════

⭐ 综合运势: SSR
  今天你写的每一行代码都会是优雅的

💻 开发者属性: 
  主语言 Python — 你是那种"能 import 就不手写"的人
  commit 午夜占比 38% — 众所周知，bug 只在深夜诞生

🍀 今日幸运框架: FastAPI
🎨 今日幸运颜色: #61DAFB
🔢 今日幸运数字: 42

⚠️ 今日避雷:
  - 不要在生产环境 rm -rf
  - 不要相信"这个小改一下就行"
  - 不要在周五下午 deploy

📈 GitHub 数据:
  公开仓库: 12 个
  总 commit: 1024 次
  最活跃时间: 23:00 - 01:00

命运提示: 今天的 pull request 会被一次 merge 通过 ✨
═══════════════════════════════════════
```

## 原理

基于 GitHub API 获取用户公开数据，用预置的运势文本库（包含 200+ 条开发者文案）随机组合生成。

**纯属娱乐，请勿用于 serious 人生决策。**

## License

MIT
