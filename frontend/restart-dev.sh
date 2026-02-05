#!/bin/bash

# Frontend Restart Script
# This script clears cache and restarts Next.js dev server

echo "🧹 Clearing Next.js cache..."
rm -rf .next

echo "📦 Rebuilding Next.js..."
npm run dev

echo "✅ Server restarted!"
echo ""
echo "Routes available:"
echo "  - http://localhost:3000        (Landing page)"
echo "  - http://localhost:3000/login   (Sign in)"
echo "  - http://localhost:3000/signup  (Sign up)"
echo "  - http://localhost:3000/dashboard (Task dashboard)"
