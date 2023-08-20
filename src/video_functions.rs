//DocJade.

use opencv as cv;
use opencv::videoio::VideoCapture;
use opencv::videoio::*;

// TODO:
// Export images from video path into a folder
// next to the original video passed in

pub fn open_video(path: &str) -> VideoCapture {
    let source_video = cv::videoio::VideoCapture::from_file(path, cv::videoio::CAP_ANY);
    match source_video {
        Ok(k) => return k,
        Err(_) => panic!("Video capture error."),
    }
}

pub fn count_frames(video: VideoCapture) -> i32 {
    match video.get(opencv::videoio::VideoCaptureProperties::CAP_PROP_FRAME_COUNT as i32) {
        Ok(i) => return i as i32,
        Err(_) => panic!("Failed to count frames!"),
    }
}

// gotta make sure that stuff works

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_open_video() {
        open_video("OhMyGah_discord.mp4");
    }

    #[test]
    fn correct_amount_of_frames() {
        let frames: i32 = count_frames(open_video("OhMyGah_discord.mp4"));
        assert_eq!(frames, 266); // oh my gah should be 266 frames long
    }
}
