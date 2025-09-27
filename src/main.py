from textnode import *
import shutil
import os
from functions import *


print("hello world")
dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():

    copy_pub_src(dir_path_static, dir_path_public)

    #generate_page("content/index.md", "template.html","public/index.html")
    '''try:
        generate_page(
                    os.path.join(dir_path_content, "index.md"),
                    template_path,
                    os.path.join(dir_path_public, "index.html"),
                      )
        print("✅ Homepage generated.")
    except Exception as e:
        print(f"❌ Failed to generate homepage: {e}")'''

    try:
        # Generate all pages recursively, not just the homepage
        generate_all_pages(dir_path_content, template_path, dir_path_public)
        print("✅ All pages generated.")
    except Exception as e:
        print(f"❌ Failed to generate pages: {e}")

if __name__ == "__main__":
    main()