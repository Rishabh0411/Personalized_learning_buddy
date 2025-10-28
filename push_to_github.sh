#!/bin/bash

# GitHub Push Helper Script
# This script will guide you through pushing your project to GitHub

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        🚀 PUSH TO GITHUB - INTERACTIVE SETUP                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized. Run: git init"
    exit 1
fi

echo "✅ Git repository initialized"
echo ""

# Check for commits
if ! git rev-parse HEAD > /dev/null 2>&1; then
    echo "❌ No commits yet. Run:"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

echo "✅ Found commits in repository"
echo ""

# Check if remote already exists
if git remote | grep -q origin; then
    echo "⚠️  Remote 'origin' already exists:"
    git remote -v
    echo ""
    read -p "Remove existing remote and add new one? (y/n): " response
    if [ "$response" = "y" ]; then
        git remote remove origin
        echo "✅ Removed existing remote"
    else
        echo "ℹ️  Keeping existing remote"
        echo ""
        echo "To push, run: git push -u origin main"
        exit 0
    fi
fi

echo "📝 Let's set up your GitHub repository!"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " username

if [ -z "$username" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

echo ""
echo "Repository name will be: personalized-learning-buddy"
echo ""

# Choose HTTPS or SSH
echo "Choose authentication method:"
echo "1) HTTPS (easier, uses Personal Access Token)"
echo "2) SSH (no passwords, requires SSH key setup)"
read -p "Enter choice (1 or 2): " auth_choice

if [ "$auth_choice" = "2" ]; then
    # SSH
    repo_url="git@github.com:${username}/personalized-learning-buddy.git"
    echo ""
    echo "📌 Using SSH URL: $repo_url"
    echo ""
    echo "⚠️  Make sure you have:"
    echo "   1. Generated an SSH key (ssh-keygen)"
    echo "   2. Added it to GitHub (https://github.com/settings/keys)"
    echo ""
    read -p "Press Enter to continue..."
else
    # HTTPS
    repo_url="https://github.com/${username}/personalized-learning-buddy.git"
    echo ""
    echo "📌 Using HTTPS URL: $repo_url"
    echo ""
    echo "⚠️  You'll need a Personal Access Token (not your password!)"
    echo "   Get one from: https://github.com/settings/tokens"
    echo "   Scopes needed: ✅ repo"
    echo ""
    read -p "Press Enter to continue..."
fi

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "BEFORE RUNNING THE NEXT COMMAND:"
echo "══════════════════════════════════════════════════════════════"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Create a new repository:"
echo "   - Name: personalized-learning-buddy"
echo "   - Description: 🧠 AI-powered study companion"
echo "   - Visibility: Public or Private"
echo "   - DO NOT initialize with README"
echo "3. Click 'Create repository'"
echo ""
read -p "Have you created the repository on GitHub? (y/n): " created

if [ "$created" != "y" ]; then
    echo ""
    echo "⚠️  Please create the repository first, then run this script again"
    exit 0
fi

echo ""
echo "🔗 Adding remote..."
git remote add origin "$repo_url"

if [ $? -eq 0 ]; then
    echo "✅ Remote added successfully"
else
    echo "❌ Failed to add remote"
    exit 1
fi

echo ""
echo "📤 Pushing to GitHub..."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🎉 SUCCESS!                               ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  Your project is now on GitHub!                              ║"
    echo "║                                                              ║"
    echo "║  View it at:                                                 ║"
    echo "║  https://github.com/${username}/personalized-learning-buddy"
    echo "║                                                              ║"
    echo "║  Share the link with your team!                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📋 Next steps:"
    echo "   • Add topics to your repository"
    echo "   • Add screenshots"
    echo "   • Share with the world! 🌍"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "   • Repository doesn't exist on GitHub"
    echo "   • Wrong credentials"
    echo "   • SSH key not set up (if using SSH)"
    echo ""
    echo "See GITHUB_SETUP.md for detailed troubleshooting"
fi
