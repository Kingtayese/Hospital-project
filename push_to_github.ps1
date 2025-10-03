# King Care Hospital Management System - GitHub Push Script
# Run this script to push your professional hospital management system to GitHub

Write-Host "🏥 King Care Hospital Management System - GitHub Push Script" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (Test-Path "manage.py") {
    Write-Host "✅ Found Django project files" -ForegroundColor Green
} else {
    Write-Host "❌ Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Check git status
Write-Host "📊 Checking git status..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "🔧 Current git configuration:" -ForegroundColor Yellow
git config user.name
git config user.email

Write-Host ""
Write-Host "📝 This script will push the following to GitHub:" -ForegroundColor Cyan
Write-Host "   • Complete Hospital Management System" -ForegroundColor White
Write-Host "   • Professional README with comprehensive documentation" -ForegroundColor White
Write-Host "   • Render deployment configuration" -ForegroundColor White
Write-Host "   • PostgreSQL database setup" -ForegroundColor White
Write-Host "   • Security and performance optimizations" -ForegroundColor White
Write-Host "   • Contributing guidelines and license" -ForegroundColor White

Write-Host ""
$confirm = Read-Host "🚀 Ready to push to GitHub? (y/N)"

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host ""
    Write-Host "🔐 GitHub Authentication Required:" -ForegroundColor Yellow
    Write-Host "   When prompted, use your GitHub username: Kingtayese" -ForegroundColor White
    Write-Host "   For password, use your Personal Access Token (not your GitHub password)" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 How to get a Personal Access Token:" -ForegroundColor Cyan
    Write-Host "   1. Go to: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "   2. Click 'Generate new token (classic)'" -ForegroundColor White
    Write-Host "   3. Select 'repo' scope" -ForegroundColor White
    Write-Host "   4. Copy the token and use it as password when prompted" -ForegroundColor White
    Write-Host ""
    
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Green
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 SUCCESS! Your Hospital Management System is now on GitHub!" -ForegroundColor Green
        Write-Host "📋 Repository URL: https://github.com/Kingtayese/Hospital-project" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
        Write-Host "   1. Visit your GitHub repository to see the professional README" -ForegroundColor White
        Write-Host "   2. Follow DEPLOYMENT.md to deploy to Render" -ForegroundColor White
        Write-Host "   3. Set up environment variables for production" -ForegroundColor White
        Write-Host "   4. Create a superuser after deployment" -ForegroundColor White
        Write-Host ""
        Write-Host "✨ Your repository now showcases enterprise-level development skills!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Push failed. Please check your credentials and try again." -ForegroundColor Red
        Write-Host ""
        Write-Host "🔧 Troubleshooting:" -ForegroundColor Yellow
        Write-Host "   • Make sure you're using 'Kingtayese' as username" -ForegroundColor White
        Write-Host "   • Use Personal Access Token as password" -ForegroundColor White
        Write-Host "   • Ensure token has 'repo' permissions" -ForegroundColor White
        Write-Host "   • Check repository URL: https://github.com/Kingtayese/Hospital-project" -ForegroundColor White
    }
} else {
    Write-Host "❌ Push cancelled. Run this script again when ready." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📚 Need help? Check the documentation:" -ForegroundColor Cyan
Write-Host "   • README.md - Complete project overview" -ForegroundColor White
Write-Host "   • DEPLOYMENT.md - Render deployment guide" -ForegroundColor White
Write-Host "   • CONTRIBUTING.md - Contributing guidelines" -ForegroundColor White