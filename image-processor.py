import cv2 as cv
from os import listdir, path, mkdir

# Sub image is image contained in the image that we're analyzing
sub_image_width: int = 32
sub_image_height: int = 32
# Space between images
y_gap_between: int = 4
x_gap_between: int = 2

path_to_images = './test-images/'

output_images_path = './output'


def main():
    if not path.exists(path_to_images):
        mkdir(path_to_images)
    if not path.exists(output_images_path):
        mkdir(output_images_path)

    images_paths = [path.join(path_to_images, f) for f in listdir(path_to_images)
                    if path.isfile(path.join(path_to_images, f))]

    for image_path in images_paths:
        image = read_image(image_path)
        cropped_images = get_sub_images(image)

        for index, cropped_image in enumerate(cropped_images):
            image_name = path.basename(image_path)
            image_full_output_path = f'./{output_images_path}/{image_name}'
            if not path.exists(image_full_output_path):
                mkdir(image_full_output_path)
            cv.imwrite(f"{image_full_output_path}/{index}.png", cropped_image)


def read_image(path):
    return cv.imread(path, cv.IMREAD_UNCHANGED)


def get_sub_images(image):
    image_height = image.shape[0]

    image_width = image.shape[1]

    max_y = int(image_height / sub_image_height)
    max_x = int(image_width / sub_image_width)
    images = []

    for x in range(1, max_x+1):
        for y in range(1, max_y):
            print(f'getting image for: {x}, {x}')
            cropped_image = find_and_save_image_for(image, x, y)
            if not is_whole_image_alpha_channel(cropped_image):
                images.append(cropped_image)
            else:
                print(f'image for {x},{x} is not found')
    return images


def find_and_save_image_for(image, x, y):
    previous_x = y-1
    previous_y = x-1

    sub_image_offset_x = sub_image_width * \
        previous_x + x_gap_between * previous_x
    sub_image_offset_y = sub_image_height * \
        previous_y + y_gap_between * previous_y

    crop_end_x = sub_image_offset_x + sub_image_width
    crop_end_y = sub_image_offset_y + sub_image_height

    crop_img = image[sub_image_offset_x:crop_end_x,
                     sub_image_offset_y:crop_end_y]
    return crop_img


def is_whole_image_alpha_channel(image):
    for pixel_x in range(1, image.shape[0]):
        for pixel_y in range(1, image.shape[1]):
            [r, g, b, a] = image[pixel_x, pixel_y]
            if (r >= 1 or g >= 1 or b >= 1) and a == 255:
                return False
    return True


if __name__ == "__main__":
    main()
