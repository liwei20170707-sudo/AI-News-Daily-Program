# 手动上传GitHub指南

## 需要上传的文件

### 核心文件（必须上传）

1. **index.html** - 播客订阅页面
2. **podcast.xml** - RSS订阅文件
3. **README.md** - 项目说明
4. **PODCAST.md** - 播客说明

### 播客音频文件

- `podcasts/AI科技早报_20260405.mp3` (2.4MB)
- `podcasts/AI科技早报_20260404.mp3` (895KB)

---

## 上传步骤

### 方法1：GitHub网页上传（推荐）

1. 访问仓库：https://github.com/liwei20170707-sudo/AI-News-Daily-Program

2. 点击 **"Add file"** → **"Upload files"**

3. 拖拽以下文件到上传区域：
   ```
   index.html
   podcast.xml
   README.md
   PODCAST.md
   podcasts/AI科技早报_20260405.mp3
   podcasts/AI科技早报_20260404.mp3
   ```

4. 填写提交信息：
   ```
   更新仓库地址为AI-News-Daily-Program
   ```

5. 点击 **"Commit changes"**

---

### 方法2：GitHub Desktop

1. 打开GitHub Desktop
2. 登录GitHub账号
3. File → Add Local Repository
4. 选择：`c:/Users/lw/WorkBuddy/Claw/ai_news_daily`
5. 点击 **"Push origin"**

---

## 上传后的验证

### 1. 检查文件是否上传成功

访问：https://github.com/liwei20170707-sudo/AI-News-Daily-Program

确认以下文件存在：
- ✅ index.html
- ✅ podcast.xml
- ✅ README.md
- ✅ podcasts/AI科技早报_20260405.mp3
- ✅ podcasts/AI科技早报_20260404.mp3

### 2. 启用GitHub Pages

1. 进入仓库 **Settings**
2. 左侧菜单找到 **Pages**
3. Source选择：**Deploy from a branch**
4. Branch选择：**main** 或 **master**
5. 点击 **Save**

### 3. 测试RSS订阅

等待5分钟后访问：
```
https://liwei20170707-sudo.github.io/AI-News-Daily-Program/podcast.xml
```

---

## 新的Pocket Casts订阅地址

```
https://liwei20170707-sudo.github.io/AI-News-Daily-Program/podcast.xml
```

### 订阅步骤

1. 打开Pocket Casts
2. 点击"添加播客"
3. 选择"通过URL添加"
4. 粘贴上述RSS地址
5. 点击订阅

---

## 文件位置

所有需要上传的文件都在：
```
c:/Users/lw/WorkBuddy/Claw/ai_news_daily/
```

---

_上传完成后，RSS订阅地址将立即生效！_