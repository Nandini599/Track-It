from app import app, db
from models import Video
import os

try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
    MOVIEPY_AVAILABLE = True
    print("✓ moviepy is available")
except Exception as e:
    MOVIEPY_AVAILABLE = False
    print(f"✗ moviepy import failed: {e}")
    print("  Trying alternative import...")
    try:
        from moviepy.editor import VideoFileClip
        MOVIEPY_AVAILABLE = True
        print("✓ moviepy (via editor) is available")
    except Exception as e2:
        print(f"✗ Alternative import also failed: {e2}")

ctx = app.app_context()
ctx.push()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'videos')

videos = Video.query.all()
print(f"Found {len(videos)} videos to update")

if not MOVIEPY_AVAILABLE:
    print("\n⚠️  Manually setting durations as fallback...")
    # For now, set them to reasonable default values or ask user
    for video in videos:
        if video.duration == 0:
            # Set a default of 10 minutes (600 seconds) as placeholder
            video.duration = 600
            db.session.commit()
            print(f"- {video.title}: Set to default 600s")
else:
    for video in videos:
        if video.duration == 0:
            file_path = os.path.join(UPLOAD_FOLDER, video.file_path.replace('videos/', ''))
            
            if os.path.exists(file_path):
                try:
                    clip = VideoFileClip(file_path)
                    duration = int(clip.duration)
                    clip.close()
                    
                    video.duration = duration
                    db.session.commit()
                    print(f"✓ {video.title}: {duration} seconds")
                except Exception as e:
                    print(f"✗ {video.title}: Error - {str(e)}")
                    # Set default
                    video.duration = 600
                    db.session.commit()
                    print(f"  → Set to default 600s")
            else:
                print(f"✗ {video.title}: File not found at {file_path}")
        else:
            print(f"- {video.title}: Already has duration ({video.duration}s)")

print("\n✅ Duration update complete!")
