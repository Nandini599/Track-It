document.addEventListener('DOMContentLoaded', () => {
    const videoElement = document.getElementById('learning-video');
    
    if (videoElement) {
        const videoId = videoElement.dataset.videoId;
        let lastReportedTime = 0;
        
        const sendProgress = (currentTime, completed = false) => {
            fetch('/progress/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    video_id: parseInt(videoId),
                    current_time: currentTime,
                    completed: completed
                })
            })
            .then(res => res.json())
            .then(data => console.log('Progress updated', data))
            .catch(err => console.error('Error updating progress:', err));
        };

        // Track every 5 seconds
        videoElement.addEventListener('timeupdate', () => {
            const current = videoElement.currentTime;
            
            // Send update if 5 seconds have passed or if 95% complete
            if (current - lastReportedTime > 5) {
                sendProgress(current);
                lastReportedTime = current;
            }
        });

        // Track on pause
        videoElement.addEventListener('pause', () => {
            sendProgress(videoElement.currentTime);
            lastReportedTime = videoElement.currentTime;
        });

        // Track on completion
        videoElement.addEventListener('ended', () => {
            sendProgress(videoElement.duration, true);
        });
    }
});
