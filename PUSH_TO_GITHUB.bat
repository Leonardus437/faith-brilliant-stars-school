@echo off
echo ========================================
echo  PUSHING TO GITHUB
echo ========================================
echo.

echo Step 1: Adding remote origin...
git remote add origin https://github.com/Leonardus437/faith-brilliant-stars-school.git

echo.
echo Step 2: Pushing to main branch...
git push -u origin main

echo.
echo ========================================
echo  PUSH COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Go to Render.com to deploy backend
echo 2. Go to Cloudflare Pages to deploy frontend
echo 3. Check DEPLOYMENT_STEPS.md for details
echo.
pause