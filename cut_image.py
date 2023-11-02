from PIL import Image


def cut_and_save_image(ctime):
    # 打开图像
    filename = "data_source/images/" + ctime + ".png"
    input_image = Image.open(filename)

    # 获取图像的宽度和高度
    width, height = input_image.size

    # 计算四个子图像的大小
    sub_width = width // 2
    sub_height = height // 2

    # 切割成四个子图像
    sub_images = [input_image.crop((x, y, x + sub_width, y + sub_height)) for x in range(0, width, sub_width) for y in
                  range(0, height, sub_height)]

    # 获取索引为0的子图像
    index_0_image = sub_images[0]

    # 保存或显示子图像
    # index_0_image.show()  # 显示图像
    filename = "data_source/images/trimmed_" + ctime + ".png"
    index_0_image.save(filename)

