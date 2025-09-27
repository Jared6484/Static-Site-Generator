from textnode import *
import shutil
import os


print("hello world")

def main():
    node = TextNode("This is some anchor text", TextType.LINK.value, "https://www.boot.dev")
    print(node)
    copy_pub_src("static/", "public/")

def copy_pub_src(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
        print("REMOVED Directory")
    os.makedirs(dest)
    print(f"Created directory: {dest}")


    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        print(f"Source Item: {src_item}")
        dst_item = os.path.join(dest, item)
        print(f"Destination Item: {dst_item}")

        if os.path.isdir(src_item):
            copy_pub_src(src_item, dst_item)
        else:
            shutil.copy2(src_item,dst_item)
            print(f"Copied: {src_item} and  {dst_item}")


if __name__ == "__main__":
    main()