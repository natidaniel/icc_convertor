from PIL import Image, ImageCms
import io
import os
import argparse
from os import listdir
from os.path import join, isdir, isfile


def make_path_compatible(path):
    path = path.replace("\\",'/')
    items = path.split('/')
    return join(*items)


def imageRGB(image):
    DP200 = ImageCms.getOpenProfile(join(args.ProfilePath,'DP200-Profile.icc'))
    sRGB = ImageCms.getOpenProfile(join(args.ProfilePath,'sRGB.icm'))
    outputProfile = sRGB

    if 'icc_profile' in image.info:
        inputProfile = ImageCms.ImageCmsProfile(io.StringIO(image.info['icc_profile']))
    else:
        image = image.convert('RGB')
        inputProfile = DP200

    new_image = ImageCms.profileToProfile(image, inputProfile, outputProfile, outputMode="RGB")

    return new_image


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("ImagePath", help="images location dir")
    arg_parser.add_argument("ProfilePath", help="profiles location dir")
    arg_parser.add_argument("OutputPath",help="new images location dir")
    args = arg_parser.parse_args()

    imgs_path = sorted([join(args.ImagePath, make_path_compatible(f)) for f in listdir(args.ImagePath) if isfile(join(args.ImagePath,f))])

    for i, im in enumerate(imgs_path):
        print('image process #',i)
        image = Image.open(im)
        img_out = imageRGB(image)
        filename, ext = os.path.splitext(im)
        name = filename[39:]
        #img_out.save(args.OutputPath + str(i+1) + '.png', "PNG")
        img_out.save(args.OutputPath + name +'.png',"PNG")
    print('END convertor to sRGB')