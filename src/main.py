from textnode import *
import shutil
import os
from functions import *
import sys


basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath += "/"
print(f" Using basepath: {basepath}")

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():

    copy_pub_src(dir_path_static, dir_path_public)

    try:
        # Generate all pages recursively, not just the homepage
        generate_all_pages(dir_path_content, template_path, dir_path_public, basepath)
        print("✅ All pages generated.")
    except Exception as e:
        print(f"❌ Failed to generate pages: {e}")

if __name__ == "__main__":
    main()