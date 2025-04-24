echo "🔧 Updating apt-get and installing ffmpeg..."
sudo apt-get update && sudo apt-get install -y ffmpeg
echo "✅ ffmpeg installed!"

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed!"