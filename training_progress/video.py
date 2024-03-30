import os
from tqdm import tqdm
import cv2  # from opencv-python


def sort_images_by_filename(directory):
    """
    Sorts images in a directory by filename and returns the full file path of each image.

    Args:
        directory (str): The directory containing the images.

    Returns:
        List[str]: A list of full file paths of the sorted images.
    """
    images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            images.append(image_path)
    images.sort()
    return images


def crop_images(images, output_dir, frame_width, frame_height):
    for image_path in tqdm(images, desc="Processing images"):
        image = cv2.imread(image_path)
        if image is None:
            print(f"Unable to read image at {image_path}")
            continue

        if image.shape[0] < frame_height or image.shape[1] < frame_width:
            print(
                f"Warning: Image at {image_path} is too small. Expected size: ({frame_width}, {frame_height}). Actual size: {image.shape[:2]}"
            )
            continue

        # cropped_image = cv2.resize(image, (frame_width, frame_height))
        cropped_image = image[:frame_height, :frame_width]

        if (
            cropped_image.shape[0] != frame_height
            or cropped_image.shape[1] != frame_width
        ):
            print(
                f"Warning: cropped image {image_path} is too small. Expected size: ({frame_width}, {frame_height}). Actual size: {image.shape[:2]}"
            )
            continue

        # write images to intermediate path
        cv2.imwrite(output_dir + "/" + image_path.split("/")[-1], cropped_image)


def create_video(images, output_path, fps):
    frame_width = cv2.imread(images[0]).shape[1]
    frame_height = cv2.imread(images[0]).shape[0]
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    video = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    for image_path in tqdm(images, desc="Creating video"):
        image = cv2.imread(image_path)
        video.write(image)
    video.release()


if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # original input images
    source_dir = os.path.join(current_dir, "..", "raw_data/training-video/input")
    # cropped images
    intermediate_dir = os.path.join(
        current_dir, "..", "raw_data/training-video/intermediate"
    )
    output_video_path = os.path.join(
        current_dir, "..", "raw_data/training-video/output/video.mp4"
    )
    print(current_dir, source_dir, output_video_path)

    # halt if directories do not exist

    for target_dir in [
        source_dir,
        intermediate_dir,
        os.path.dirname(output_video_path),
    ]:
        if not os.path.exists(target_dir):
            print(f"Error: Source directory not found at {source_dir}")
            exit(1)

    # crop the original input images, if not already processed
    # re-enable this manually if needed
    # crop_images(sort_images_by_filename(source_dir), intermediate_dir, 1280, 1024)

    # turn cropped images into video
    sorted_images = sort_images_by_filename(intermediate_dir)
    print(sorted_images)
    create_video(sorted_images, output_video_path, fps=4)
