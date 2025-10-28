# 🚀 GitHub Setup Guide

Your project is now ready to be pushed to GitHub! Follow these steps:

---

## 📋 Prerequisites

1. **GitHub Account**: If you don't have one, create at https://github.com/signup
2. **Git Configured**: ✅ Already done!

---

## 🎯 Option 1: Push to GitHub (Recommended)

### Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name**: `personalized-learning-buddy`
   - **Description**: `🧠 AI-powered study companion using RAG + LLM for personalized quizzes and learning`
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click **"Create repository"**

### Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Use these:

```bash
cd "/home/rishabh/Desktop/Projects/Gen AI Project/personalized_learning_buddy"

# Add your GitHub repository as remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/personalized-learning-buddy.git

# Push your code
git push -u origin main
```

**Example with username "rishabh123":**
```bash
git remote add origin https://github.com/rishabh123/personalized-learning-buddy.git
git push -u origin main
```

### Step 3: Enter Credentials

When prompted:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your GitHub password)

#### How to Create a Personal Access Token:

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `Personalized Learning Buddy`
4. Select scopes: ✅ `repo` (all repo permissions)
5. Click **"Generate token"**
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing

---

## 🎯 Option 2: Using SSH (Advanced)

If you prefer SSH (no password prompts):

### Step 1: Generate SSH Key (if you don't have one)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter to accept default location
# Press Enter twice for no passphrase (or set one)
```

### Step 2: Add SSH Key to GitHub

```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub
```

1. Go to https://github.com/settings/keys
2. Click **"New SSH key"**
3. Paste the key
4. Click **"Add SSH key"**

### Step 3: Use SSH Remote

```bash
git remote add origin git@github.com:USERNAME/personalized-learning-buddy.git
git push -u origin main
```

---

## 📝 After Pushing to GitHub

### Add Repository Topics

1. Go to your repository page
2. Click the ⚙️ icon next to "About"
3. Add topics:
   - `machine-learning`
   - `ai`
   - `rag`
   - `llm`
   - `education`
   - `quiz`
   - `streamlit`
   - `python`
   - `openai`
   - `langchain`

### Add GitHub Secrets (for CI/CD later)

1. Go to Settings → Secrets and variables → Actions
2. Add `OPENAI_API_KEY` if you want to use GitHub Actions

### Enable GitHub Pages (Optional)

You can host documentation:
1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: /docs (if you create one)

---

## 🎨 Enhance Your Repository

### Add a LICENSE

Create a LICENSE file:
```bash
# MIT License is popular for open source
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "📄 Add MIT License"
git push
```

### Add Screenshots

Create a `screenshots/` folder with images of your app:
```bash
mkdir screenshots
# Add screenshots of your app running
git add screenshots/
git commit -m "📸 Add screenshots"
git push
```

### Add GitHub Actions (CI/CD)

Create `.github/workflows/test.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python test_setup.py
```

---

## 🔄 Future Updates

When you make changes:

```bash
# Check what changed
git status

# Stage changes
git add .

# Commit with a message
git commit -m "✨ Add new feature: [description]"

# Push to GitHub
git push
```

### Commit Message Conventions:

- `✨` `:sparkles:` - New feature
- `🐛` `:bug:` - Bug fix
- `📝` `:memo:` - Documentation
- `🎨` `:art:` - UI/Style changes
- `♻️` `:recycle:` - Refactoring
- `⚡` `:zap:` - Performance improvement
- `🔧` `:wrench:` - Configuration
- `🧪` `:test_tube:` - Tests

---

## 📢 Share Your Project

### Create a Great README.md Badge Section

Add to the top of README.md:

```markdown
# 🧠 Personalized Learning Buddy

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-green.svg)](https://openai.com)

> Your AI-powered study companion for smarter learning
```

### Share on Social Media

- **Twitter/X**: "Just built an AI study companion with RAG + LLM! 🧠✨"
- **LinkedIn**: Professional post about your project
- **Reddit**: r/Python, r/MachineLearning, r/learnprogramming
- **Dev.to**: Write a blog post about building it

---

## 🌟 Get Stars!

Encourage people to star your repo:
1. Share with friends and classmates
2. Post in relevant communities
3. Create a demo video
4. Write a blog post about it

---

## 📊 Repository Statistics

Once pushed, you can see:
- **Insights**: Traffic, clones, stars
- **Issues**: Track bugs and feature requests
- **Pull Requests**: Collaborate with others
- **Actions**: Automated workflows

---

## 🎓 Example Repository URL

Your repository will be available at:
```
https://github.com/YOUR_USERNAME/personalized-learning-buddy
```

Clone command for others:
```bash
git clone https://github.com/YOUR_USERNAME/personalized-learning-buddy.git
```

---

## ✅ Quick Checklist

- [ ] Create GitHub repository
- [ ] Add remote origin
- [ ] Push code to GitHub
- [ ] Add repository description
- [ ] Add topics/tags
- [ ] Add LICENSE file
- [ ] Add screenshots (optional)
- [ ] Set up GitHub Actions (optional)
- [ ] Share with the world! 🌍

---

## 🆘 Troubleshooting

### "Authentication failed"
- Use Personal Access Token, not password
- Get token from: https://github.com/settings/tokens

### "Repository not found"
- Check repository name spelling
- Ensure repository exists on GitHub
- Verify you have access

### "Permission denied (publickey)"
- For SSH: Check your SSH key is added to GitHub
- Or use HTTPS instead

### "Remote origin already exists"
```bash
git remote remove origin
# Then add again with correct URL
```

---

## 🚀 You're All Set!

Your project is now version controlled and ready to be shared with the world!

**Next Steps:**
1. Push to GitHub using commands above
2. Share the link with your team
3. Start collaborating!

Happy coding! 🎉
