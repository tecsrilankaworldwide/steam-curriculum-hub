#!/bin/bash
# STEAM Curriculum Hub - Mac/Linux Startup Script

echo "========================================"
echo "STEAM Curriculum Hub - Sinhala Edition"
echo "TEC Sri Lanka Worldwide"
echo "========================================"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not installed!"
    echo "Install from: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "[1/3] Checking Docker..."
if ! docker info &> /dev/null; then
    echo "ERROR: Docker not running!"
    echo "Please start Docker and try again."
    exit 1
fi
echo "✓ Docker running"

echo ""
echo "[2/3] Starting STEAM Hub services..."
docker-compose up -d

echo ""
echo "[3/3] Opening application..."
sleep 10

# Open browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    open http://localhost:3000
fi

echo ""
echo "========================================"
echo "✓ STEAM Hub Started!"
echo "========================================"
echo ""
echo "Access at: http://localhost:3000"
echo ""
echo "Features:"
echo "- 1000 STEAM Lessons (Sinhala + English)"
echo "- FREE Voice Reading"
echo "- Ages 5-18"
echo "- Progress Tracking"
echo "- Quizzes and Certificates"
echo ""
echo "To STOP: Run ./STOP_STEAM_HUB.sh"
echo ""
