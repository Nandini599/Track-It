import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from models import db, User, Subject, Video, Progress

app = Flask(__name__)

# Configurations
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'dev-secret-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trackit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'videos')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 # 500 MB max limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)

db.init_app(app)

@app.context_processor
def inject_user():
    def get_current_user():
        user_id = session.get('user_id')
        if user_id:
            return User.query.get(user_id)
        return None
    return dict(current_user=get_current_user())

# -----------------
# Public Routes
# -----------------

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))
            
        is_first_user = User.query.count() == 0
        role = 'admin' if is_first_user else 'student'
        
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

# -----------------
# Student Routes
# -----------------

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
        
    total_study_time = db.session.query(db.func.sum(Progress.watched_duration)).filter_by(user_id=session['user_id']).scalar() or 0
    total_videos_watched = Progress.query.filter_by(user_id=session['user_id'], completed=True).count()
    
    stats = {
        'total_study_time': round(total_study_time / 60, 2), # In minutes
        'videos_completed': total_videos_watched
    }
    
    return render_template('dashboard.html', stats=stats)

@app.route('/subjects')
def subjects():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    all_subjects = Subject.query.all()
    return render_template('subjects.html', subjects=all_subjects)

@app.route('/videos/<int:subject_id>')
def videos(subject_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    subject = Subject.query.get_or_404(subject_id)
    return render_template('videos.html', subject=subject)

@app.route('/player/<int:video_id>')
def player(video_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    video = Video.query.get_or_404(video_id)
    
    # Get or create progress
    user_id = session['user_id']
    progress = Progress.query.filter_by(user_id=user_id, video_id=video_id).first()
    if not progress:
        progress = Progress(user_id=user_id, video_id=video_id)
        db.session.add(progress)
        db.session.commit()
        
    return render_template('player.html', video=video, progress=progress)

@app.route('/progress/update', methods=['POST'])
def update_progress():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    video_id = data.get('video_id')
    current_time = data.get('current_time')
    completed = data.get('completed', False)
    
    progress = Progress.query.filter_by(user_id=session['user_id'], video_id=video_id).first()
    if progress:
        if current_time > progress.watched_duration:
            progress.watched_duration = current_time
        if completed:
            progress.completed = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Progress not found'}), 404

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    stats = []
    
    # Aggregate data for Chart.js
    subjects = Subject.query.all()
    for sub in subjects:
        total_time = 0
        for vid in sub.videos:
            prog = Progress.query.filter_by(user_id=user_id, video_id=vid.id).first()
            if prog:
                total_time += prog.watched_duration
        stats.append({'subject': sub.name, 'time': round(total_time / 60, 2)})

    return render_template('reports.html', stats=stats)

# -----------------
# Admin Routes
# -----------------

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
        
    subjects = Subject.query.all()
    videos = Video.query.all()
    users = User.query.all()
    
    return render_template('admin.html', subjects=subjects, videos=videos, users=users)

@app.route('/admin/subject', methods=['POST'])
def add_subject():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
        
    name = request.form.get('name')
    if name:
        if Subject.query.filter_by(name=name).first():
            flash('Subject already exists!', 'error')
        else:
            new_sub = Subject(name=name)
            db.session.add(new_sub)
            db.session.commit()
            flash('Subject added successfully!', 'success')
            
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload', methods=['POST'])
def upload_video():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
        
    title = request.form.get('title')
    subject_id = request.form.get('subject_id')
    file = request.files.get('video')
    
    if file and title and subject_id:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # relative path for serving
        rel_path = f'videos/{filename}'
        
        new_vid = Video(title=title, subject_id=subject_id, file_path=rel_path)
        db.session.add(new_vid)
        db.session.commit()
        
        flash('Video uploaded successfully!', 'success')
    else:
        flash('Missing required fields for upload', 'error')
        
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
