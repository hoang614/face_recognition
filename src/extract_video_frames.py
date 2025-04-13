import os
import cv2
import glob
import random

def extract_frames_from_video(video_path, output_dir, num_frames=200):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        return
    
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        vidcap.release()
        return
    
    step = max(1, total_frames // num_frames)  # Đảm bảo step ít nhất là 1
    frame_indices = [i * step for i in range(num_frames) if i * step < total_frames]
    
    random_indices = random.sample(range(200), len(frame_indices))  # Tạo các chỉ mục ngẫu nhiên
    
    count = 0
    for idx, random_idx in zip(frame_indices, random_indices):
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        success, image = vidcap.read()
        if not success:
            continue

        # Lưu khung hình với chỉ mục ngẫu nhiên
        frame_path = os.path.join(output_dir, f"frame_{random_idx}.jpg")
        cv2.imwrite(frame_path, image)
        count += 1

    vidcap.release()

def process_videos_in_directory(video_dir, training_data_dir, num_frames=200):
    if not os.path.exists(training_data_dir):
        os.makedirs(training_data_dir)
    video_paths = glob.glob(os.path.join(video_dir, "*.mp4"))
    for video_path in video_paths:
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        
        output_dir = os.path.join(training_data_dir, video_name)
        extract_frames_from_video(video_path, output_dir, num_frames)

video_dir = "Dataset/video"  # đường dẫn đến thư mục chứa video
training_data_dir = "Dataset/faceData/raw"  # đường dẫn đến thư mục lưu trữ dữ liệu huấn luyện
process_videos_in_directory(video_dir, training_data_dir, num_frames=200)
    