from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import json
from datetime import datetime
import time

app = Flask(__name__, static_folder='.')
CORS(app)

# YouTube Data API configuration
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"  # احصل عليه من Google Cloud Console
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/manifest.json')
def manifest():
    """Serve the PWA manifest"""
    return send_from_directory('.', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    """Serve the service worker"""
    return send_from_directory('.', 'sw.js')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
        r'youtu\.be\/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_info(video_id):
    """Get video information from YouTube API"""
    try:
        url = f"{YOUTUBE_API_URL}/videos"
        params = {
            'part': 'snippet,statistics,contentDetails',
            'id': video_id,
            'key': YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            video = data['items'][0]
            snippet = video['snippet']
            statistics = video['statistics']
            content_details = video['contentDetails']
            
            # Parse duration
            duration = content_details['duration']
            duration_formatted = parse_duration(duration)
            
            return {
                'title': snippet['title'],
                'channel': snippet['channelTitle'],
                'duration': duration_formatted,
                'views': format_number(statistics.get('viewCount', 0)),
                'description': snippet['description'][:200] + '...' if len(snippet['description']) > 200 else snippet['description'],
                'thumbnail': snippet['thumbnails']['medium']['url'],
                'published': snippet['publishedAt']
            }
    except Exception as e:
        print(f"Error getting video info: {e}")
        return {
            'title': 'فيديو يوتيوب',
            'channel': 'غير معروف',
            'duration': '0:00',
            'views': '0',
            'description': '',
            'thumbnail': '',
            'published': ''
        }

def parse_duration(duration):
    """Parse ISO 8601 duration to readable format"""
    import re
    
    # Extract hours, minutes, seconds from PT1H2M3S format
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration)
    
    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    return "0:00"

def format_number(num):
    """Format large numbers with commas"""
    try:
        num = int(num)
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        else:
            return str(num)
    except:
        return "0"

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    """Get transcript for a YouTube video"""
    try:
        data = request.json
        video_url = data.get('url', '').strip()
        language = data.get('language', 'en')
        include_timestamps = data.get('includeTimestamps', True)
        auto_translate = data.get('autoTranslate', False)
        
        if not video_url:
            return jsonify({'error': 'رابط الفيديو مطلوب'}), 400
        
        # Extract video ID
        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({'error': 'رابط اليوتيوب غير صحيح'}), 400
        
        # Get video information
        video_info = get_video_info(video_id)
        
        # Get transcript
        transcript_list = []
        available_languages = []
        
        try:
            # Get available transcripts
            transcript_data = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Collect available languages
            for transcript in transcript_data:
                available_languages.append({
                    'language_code': transcript.language_code,
                    'language': transcript.language,
                    'is_generated': transcript.is_generated,
                    'is_translatable': transcript.is_translatable
                })
            
            # Try to get transcript in requested language
            try:
                transcript = transcript_data.find_transcript([language])
                transcript_list = transcript.fetch()
            except NoTranscriptFound:
                # Try auto-generated transcript
                try:
                    transcript = transcript_data.find_generated_transcript([language])
                    transcript_list = transcript.fetch()
                except NoTranscriptFound:
                    # Try any available transcript
                    transcript = next(iter(transcript_data))
                    transcript_list = transcript.fetch()
                    
                    # Translate if requested and possible
                    if auto_translate and transcript.is_translatable:
                        try:
                            translated = transcript.translate(language)
                            transcript_list = translated.fetch()
                        except:
                            pass  # Use original if translation fails
            
        except TranscriptsDisabled:
            return jsonify({'error': 'الترجمة غير متوفرة لهذا الفيديو'}), 404
        except NoTranscriptFound:
            return jsonify({'error': 'لا توجد ترجمة متاحة لهذا الفيديو'}), 404
        except Exception as e:
            return jsonify({'error': f'خطأ في الحصول على الترجمة: {str(e)}'}), 500
        
        if not transcript_list:
            return jsonify({'error': 'لم يتم العثور على ترجمة'}), 404
        
        # Format transcript
        formatted_transcript = []
        for item in transcript_list:
            formatted_item = {
                'text': item['text'].strip(),
                'start': round(item['start'], 2),
                'duration': round(item['duration'], 2)
            }
            formatted_transcript.append(formatted_item)
        
        # Prepare response
        response_data = {
            'success': True,
            'videoInfo': video_info,
            'transcript': formatted_transcript,
            'availableLanguages': available_languages,
            'extractedLanguage': language,
            'totalDuration': sum([item['duration'] for item in formatted_transcript]),
            'wordCount': len(' '.join([item['text'] for item in formatted_transcript]).split()),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in get_transcript: {e}")
        return jsonify({'error': f'خطأ غير متوقع: {str(e)}'}), 500

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    languages = [
        {'code': 'ar', 'name': 'العربية', 'native': 'العربية'},
        {'code': 'en', 'name': 'English', 'native': 'English'},
        {'code': 'es', 'name': 'Spanish', 'native': 'Español'},
        {'code': 'fr', 'name': 'French', 'native': 'Français'},
        {'code': 'de', 'name': 'German', 'native': 'Deutsch'},
        {'code': 'it', 'name': 'Italian', 'native': 'Italiano'},
        {'code': 'pt', 'name': 'Portuguese', 'native': 'Português'},
        {'code': 'ru', 'name': 'Russian', 'native': 'Русский'},
        {'code': 'ja', 'name': 'Japanese', 'native': '日本語'},
        {'code': 'ko', 'name': 'Korean', 'native': '한국어'},
        {'code': 'zh', 'name': 'Chinese', 'native': '中文'},
        {'code': 'hi', 'name': 'Hindi', 'native': 'हिन्दी'},
        {'code': 'tr', 'name': 'Turkish', 'native': 'Türkçe'},
        {'code': 'nl', 'name': 'Dutch', 'native': 'Nederlands'},
        {'code': 'pl', 'name': 'Polish', 'native': 'Polski'},
        {'code': 'sv', 'name': 'Swedish', 'native': 'Svenska'},
        {'code': 'da', 'name': 'Danish', 'native': 'Dansk'},
        {'code': 'no', 'name': 'Norwegian', 'native': 'Norsk'},
        {'code': 'fi', 'name': 'Finnish', 'native': 'Suomi'},
        {'code': 'he', 'name': 'Hebrew', 'native': 'עברית'}
    ]
    
    return jsonify({
        'success': True,
        'languages': languages
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'الصفحة غير موجودة'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'خطأ في الخادم'}), 500

if __name__ == '__main__':
    print("🚀 Starting YouTube Transcript Extractor Server...")
    print("📱 PWA will be available at: http://localhost:5000")
    print("🔧 API endpoints:")
    print("   - POST /api/transcript - Extract transcript")
    print("   - GET /api/languages - Get supported languages")
    print("   - GET /api/health - Health check")
    
    # Check if required packages are installed
    try:
        import youtube_transcript_api
        import flask_cors
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install: pip install youtube-transcript-api flask-cors")
        exit(1)
    
    # Run the server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )