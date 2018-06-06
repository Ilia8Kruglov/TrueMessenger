
def from_str_to_img(imgString):
    imgToBytes = imgString.encode()
    return imgToBytes


if __name__ == "__main__":
    print(from_str_to_img('dasda'))