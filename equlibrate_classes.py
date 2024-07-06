import os
import shutil
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
import cv2
import numpy as np
from collections import Counter

def load_images_from_folder(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
            labels.append(label)
    return images, labels

def save_images_to_folder(images, labels, base_folder):
    for idx, (img, label) in enumerate(zip(images, labels)):
        label_folder = os.path.join(base_folder, label)
        if not os.path.exists(label_folder):
            os.makedirs(label_folder)
        img_path = os.path.join(label_folder, f"img_{idx}.png")
        cv2.imwrite(img_path, img)

# Paths to your dataset
base_path = 'data/train'
classes = ['covid', 'lung_opacity', 'pneumonia', 'normal']

# Load all images and labels
all_images = []
all_labels = []
for cls in classes:
    folder = os.path.join(base_path, cls)
    images, labels = load_images_from_folder(folder, cls)
    all_images.extend(images)
    all_labels.extend(labels)

# Convert to numpy arrays
all_images = np.array(all_images)
all_labels = np.array(all_labels)

# Checking the distribution of classes before balancing
print("Before balancing: ", Counter(all_labels))

# Reshape images for RandomOverSampler/RandomUnderSampler
n_samples, height, width, channels = all_images.shape
all_images_reshaped = all_images.reshape((n_samples, height * width * channels))

# Choose either RandomOverSampler or RandomUnderSampler
ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(all_images_reshaped, all_labels)

# Alternatively, undersampling the majority class
# rus = RandomUnderSampler(random_state=42)
# X_resampled, y_resampled = rus.fit_resample(all_images_reshaped, all_labels)

# Reshape images back to original shape
X_resampled = X_resampled.reshape((X_resampled.shape[0], height, width, channels))

# Checking the distribution of classes after balancing
print("After balancing: ", Counter(y_resampled))

# Save the resampled dataset
balanced_data_path = 'data/balanced_train'
if os.path.exists(balanced_data_path):
    shutil.rmtree(balanced_data_path)
os.makedirs(balanced_data_path)

save_images_to_folder(X_resampled, y_resampled, balanced_data_path)

print(f"Balanced dataset saved to {balanced_data_path}")
