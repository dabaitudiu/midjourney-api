from PIL import Image

from constants import images_output_parent_dir, sub_dir_name

images_output_dir = images_output_parent_dir + sub_dir_name


def cut_and_save_image(ctime):
    # 打开图像
    filename = images_output_dir + ctime + ".png"
    input_image = Image.open(filename)

    # 获取图像的宽度和高度
    width, height = input_image.size

    # 计算四个子图像的大小
    sub_width = width // 2
    sub_height = height // 2

    # 切割成四个子图像
    sub_images = [input_image.crop((x, y, x + sub_width, y + sub_height)) for x in range(0, width, sub_width) for y in
                  range(0, height, sub_height)]

    # index_0_image.show()  # 显示图像

    for i in range(4):
        # 获取索引为i的子图像
        index_i_image = sub_images[i]
        inner_dir_name = f'image_group_{i+1}/'
        filename = images_output_dir + inner_dir_name + "_trimmed_" + ctime + "_" + str(i) + "_.png"
        index_i_image.save(filename)

