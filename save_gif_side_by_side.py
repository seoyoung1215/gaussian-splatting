import os
from PIL import Image, ImageSequence
import pdb

def create_side_by_side_gif(folder_path1, folder_path2, folder_path3, output_path):
    # Get a list of file paths in each folder
    files1 = [os.path.join(folder_path1, file) for file in os.listdir(folder_path1) if file.endswith(('.jpg', '.png'))
                and file[-8:-4].isdigit()]
                # if 'instanceSegmentation' not in file if 'segmentation' not in file]
    # pdb.set_trace()
    # files1 = [f for f in files1 if 'instanceSegmentation' not in f and 'segmentation' not in f]
    files2 = [os.path.join(folder_path2, file) for file in os.listdir(folder_path2) if file.endswith(('.jpg', '.png'))]
    files3 = [os.path.join(folder_path3, file) for file in os.listdir(folder_path3) if file.endswith(('.jpg', '.png'))]

    # Sort the file lists to ensure consistent order
    files1.sort()
    files2.sort()
    files3.sort()

    # Ensure there are an equal number of files in both folders
    num_frames = min(len(files1), len(files2), len(files3))

    # Create a new image with double the width
    new_width = 0  # will be determined by the first image
    min_height = float('inf')  # initialize with a large value

    frames = []

    for i in range(num_frames):
        # Open the images
        image1 = Image.open(files1[i])
        image2 = Image.open(files2[i])
        image3 = Image.open(files3[i])

        # Resize images to the same height
        common_height = min(image1.height, image2.height, image3.height)
        image1 = image1.resize((int(image1.width * common_height / image1.height), common_height))
        image2 = image2.resize((int(image2.width * common_height / image2.height), common_height))
        image3 = image3.resize((int(image3.width * common_height / image3.height), common_height))

        # Update minimum height
        min_height = min(min_height, common_height)

        # Update new width for the first frame
        if i == 0:
            new_width = image1.width + image2.width + image3.width

        # Create a new frame with double the width
        new_frame = Image.new('RGB', (new_width, min_height))

        # Paste the resized images side by side
        new_frame.paste(image1, (0, 0))
        new_frame.paste(image2, (image1.width, 0))
        new_frame.paste(image3, (image1.width + image2.width, 0))

        frames.append(new_frame)

    # Save the result as a GIF
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=500, loop=0)

# Example usage
folder_path1 = '/workspace/gaussian-splatting/output/imagery/siteACC0010/vehicle_transients/test/ours_30000/gt' #'/dataset/imagery/231002/230927_siteACC0036-delivery/siteACC0036/camACC001-security_pinhole/2023-09-27-14-58-05' #"path/to/first/folder"
folder_path2 = '/workspace/gaussian-splatting/output/imagery/siteACC0010/vehicle_transients/test/ours_30000/renders' #'/app/out/gnt_released_synth_siteACC0036_security' #"path/to/second/folder"
folder_path3 = '/workspace/gaussian-splatting/output/imagery/siteACC0010/vehicle_transients/test/ours_60000/renders' #'/app/out/gnt_released_synth_siteACC0036_security' #"path/to/second/folder"
output_gif_path = '/workspace/gaussian-splatting/output/imagery/siteACC0010/vehicle_transients/test/result_30000_60000.gif' #'/app/out/gnt_released_synth_siteACC0036_security/result.gif' #"output/result.gif"

create_side_by_side_gif(folder_path1, folder_path2, folder_path3, output_gif_path)
