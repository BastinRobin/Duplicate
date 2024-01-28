import cv2
import numpy as np
from PIL import Image
from skimage import img_as_float
from skimage.metrics import structural_similarity as ssim
#import imageio
import imageio.v2 as imageio  # Importing imageio.v2 instead of imageio
import json

def calculate_composition_score(image_path):
    # Placeholder function, actual implementation may require more sophisticated analysis
    return np.random.uniform(0, 10)

def calculate_color_harmony_score(image_path):
    img = cv2.imread(image_path)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Calculate the standard deviation of hue values
    hue_std = np.std(hsv_img[:, :, 0])
    
    # Normalize the hue_std to a scale of 0-10
    normalized_hue_std = (hue_std / 180.0) * 10
    
    return 10 - normalized_hue_std  # Higher hue_std implies less color harmony

def calculate_lighting_quality_score(image_path):
    # Placeholder function, actual implementation may require more sophisticated analysis
    return np.random.uniform(0, 10)

def calculate_subject_appeal_score(image_path):
    # Placeholder function, actual implementation may require more sophisticated analysis
    return np.random.uniform(0, 10)

def calculate_emotional_impact_score(image_path):
    # Placeholder function, actual implementation may require more sophisticated analysis
    return np.random.uniform(0, 10)

def calculate_blur(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def calculate_sharpness(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    return np.mean(gradient_magnitude)

def calculate_quality_to_print(image_path):
    img = Image.open(image_path)
    return img.info.get("dpi", (300, 300))

def calculate_duplication_score(image_path1, image_path2, target_size=(256, 256)):
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    # Check if images are loaded successfully
    if img1 is None or img2 is None:
        return 0.0  # Return a default score

    # Resize images to the target size
    img1 = cv2.resize(img1, target_size)
    img2 = cv2.resize(img2, target_size)

    # Convert to grayscale if the images are not already in grayscale
    if len(img1.shape) > 2:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    if len(img2.shape) > 2:
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Check if the images are entirely black or have no variance
    if np.all(img1 == 0) or np.all(img2 == 0) or np.var(img1) == 0 or np.var(img2) == 0:
        return 0.0  # Return a default score

    # Choose an appropriate win_size value based on the size of the resized images
    win_size = min(target_size[0], target_size[1], 7)  # You can adjust this value accordingly

    # Ensure that win_size is odd and within the valid range
    win_size = min(win_size, min(target_size[0], target_size[1]))
    win_size = win_size if win_size % 2 == 1 else win_size - 1

    try:
        ssim_score, _ = ssim(img1, img2, full=True, win_size=win_size)
        return ssim_score
    except Exception as e:
        print(f"Error calculating SSIM: {e}")
        return 0.0  # Return a default score in case of an error

def calculate_depth_of_field(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use the SGBM (Semi-Global Block Matching) algorithm to calculate the depth map
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(gray, gray)

    # Check if the disparity map contains only NaN values
    if np.isnan(disparity).all():
        return None, None

    # Normalize the disparity map for better visualization
    normalized_disparity = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)

    # Calculate the average depth value
    average_depth = np.nanmean(disparity)  # Use np.nanmean to ignore NaN values

    return normalized_disparity, average_depth

def process_images(image_paths):
    results = []
    for image_path in image_paths:
        blur = calculate_blur(image_path)
        sharpness = calculate_sharpness(image_path)
        quality_to_print = calculate_quality_to_print(image_path)
        
        # Assuming you have a second image for duplication score
        second_image_path = "/Users/bastinrobins/Desktop/1699604043573.jpeg"  # Provide a second image for duplication score calculation
        duplication_score = calculate_duplication_score(image_path, second_image_path)

        # Depth of field calculation
        depth_map, average_depth = calculate_depth_of_field(image_path)

        if depth_map is None or np.isnan(average_depth):
            average_depth = 0.0  # Set a default value if depth calculation fails

        # Calculate photographer input metrics without manual input
        composition_score = calculate_composition_score(image_path)
        color_harmony_score = calculate_color_harmony_score(image_path)
        lighting_quality_score = calculate_lighting_quality_score(image_path)
        subject_appeal_score = calculate_subject_appeal_score(image_path)
        emotional_impact_score = calculate_emotional_impact_score(image_path)

        result = {
            "image_path": image_path,
            "blur": blur,
            "sharpness": sharpness,
            "quality_to_print": quality_to_print,
            "duplication_score": duplication_score,
            "average_depth": average_depth,
            "composition_score": composition_score,
            "color_harmony_score": color_harmony_score,
            "lighting_quality_score": lighting_quality_score,
            "subject_appeal_score": subject_appeal_score,
            "emotional_impact_score": emotional_impact_score
        }

        results.append(result)

    return results

# Example usage
image_paths = ["/Users/bastinrobins/Desktop/1699604043573.jpeg", "/Users/bastinrobins/Desktop/1700240494221.jpeg"]
results = process_images(image_paths)

# Output the results as JSON
json_response = json.dumps(results, indent=2)
print(json_response)

