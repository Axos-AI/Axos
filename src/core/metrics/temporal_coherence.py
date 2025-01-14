import os
import cv2
import lpips
import torch
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

# Initialize LPIPS with VGG backbone
lpips_loss = lpips.LPIPS(net='vgg').to('cuda' if torch.cuda.is_available() else 'cpu')

def calculate_lpips_between_frames(frame1, frame2):
    """Calculate LPIPS score between two frames"""
    frame1_tensor = torch.tensor(frame1).permute(2, 0, 1).unsqueeze(0).float() / 255.0 * 2 - 1
    frame2_tensor = torch.tensor(frame2).permute(2, 0, 1).unsqueeze(0).float() / 255.0 * 2 - 1

    # Move tensors to the appropriate device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    frame1_tensor, frame2_tensor = frame1_tensor.to(device), frame2_tensor.to(device)

    # Calculate LPIPS score
    lpips_value = lpips_loss(frame1_tensor, frame2_tensor).item()
    return lpips_value

def video_temporal_lpips(video_path):
    """Calculate LPIPS temporal coherence across consecutive frames"""
    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    if not ret:
        print(f"Error: Could not read the video at {video_path}.")
        return None, None

    lpips_scores = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate LPIPS for consecutive frames
        lpips_value = calculate_lpips_between_frames(prev_frame, frame)
        lpips_scores.append(lpips_value)

        prev_frame = frame

    cap.release()
    
    # Calculate the average LPIPS score across the video
    avg_lpips = sum(lpips_scores) / len(lpips_scores)
    return avg_lpips, lpips_scores

def visualize_lpips_scores(lpips_scores, video_name):
    """Visualize LPIPS scores over time"""
    plt.figure(figsize=(12, 6))
    plt.plot(lpips_scores, marker='o')
    plt.title(f"LPIPS Temporal Consistency: {video_name}")
    plt.xlabel("Frame Index")
    plt.ylabel("LPIPS Score")
    plt.grid(True)
    plt.show()

def process_single_video(video_path):
    """Helper function for parallel processing of a single video"""
    video_name = os.path.basename(video_path)
    avg_lpips, lpips_scores = video_temporal_lpips(video_path)
    if avg_lpips is not None:
        visualize_lpips_scores(lpips_scores, video_name)
        print(f"Average LPIPS for {video_name}: {avg_lpips:.4f}")
    return video_name, avg_lpips

def batch_process_videos_parallel(video_folder, num_workers=4):
    """Batch process multiple videos for LPIPS analysis using multiprocessing"""
    results = {}

    # Collect all video files
    video_paths = [
        os.path.join(video_folder, f)
        for f in os.listdir(video_folder)
        if f.endswith(('.mp4', '.avi', '.mov'))
    ]

    # Parallel processing using ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_single_video, video_path) for video_path in video_paths]

        for future in futures:
            video_name, avg_lpips = future.result()
            if avg_lpips is not None:
                results[video_name] = avg_lpips

    # Display summary of results
    print("\n=== Batch Processing Summary ===")
    for video, score in results.items():
        print(f"{video}: Average LPIPS = {score:.4f}")

    return results

# Example usage (uncomment and provide the path to your folder)
# video_folder_path = "path_to_your_video_folder"
# batch_process_videos_parallel(video_folder_path, num_workers=4)


# process_single_video("path_to_your_video_folder/video_name.mp4")