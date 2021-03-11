import os
import imageio
from imageio.core.functions import imwrite
from PIL import Image
from PIL import ImageSequence




### 读写gif使用：imageio.mimread(), imageio.mimsave()
### 读写单张图片使用：imageio.imread(), imageio.imwrite()

def split_gif_to_single_pic(gif_uri: str, save_all: bool=False) -> None:
    """[summary]

    Args:
        gif_uri    (str): [gif文件的资源地址]
        new_uri    (str): [保存图片的资源地址]
        save_all  (bool): [是否保存所有帧图片]
            save_all 为False则默认返回第一帧图片
                     为True返回所有图片
    """
    dirname, filename = os.path.split(gif_uri)
    folder_name = os.path.splitext(filename)[0]
    im = Image.open(gif_uri)
    if save_all:
        if not os.path.exists(os.path.join(dirname, folder_name)):
            os.makedirs(os.path.join(dirname, folder_name))
        for idx, frame in enumerate(ImageSequence.Iterator(im)):
            # save the first frame
            frame.save(os.path.join(dirname, folder_name, folder_name+f"{idx+1}.png"))
    else:
        for frame in ImageSequence.Iterator(im):
            # save the first frame
            frame.save(os.path.join(dirname, folder_name+".png"))
            break


def combine_to_gif(pic_folder: str, target_name: str) -> None:
    """[summary]

    Args:
        pic_folder (str): [pictures uri]
        target_name (str): [target_name.gif]
    """
    img_type = [".png", ".jpeg", ".jpg"]
    images = []
    all_pics = sorted(
        os.listdir(pic_folder), 
        key=lambda x: int(os.path.splitext(x)[0].replace("default", "")))
    for each_frame in all_pics:
        if not img_type.__contains__(os.path.splitext(each_frame)[1]):
            continue
        images.append(Image.open(os.path.join(pic_folder, each_frame)))
    images[0].save(os.path.join(os.path.dirname(pic_folder), target_name),
               save_all=True, 
               append_images=images[1:], 
               optimize=False, 
               duration=60, 
               loop=0)



if __name__=="__main__":
    # split_gif_to_single_pic(r"C:\Users\ci24924\Desktop\default.gif", save_all=True)
    # combine_to_gif(r"C:\Users\ci24924\Desktop\default", "test.gif")
    pass