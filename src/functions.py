from converters import *
import os
import shutil

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path,'r') as f:
        template_content = f.read()
    
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    final_output = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(final_output)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    raise Exception("No H1 header found in Markdown")


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

def generate_all_pages(content_dir, template_path, public_dir):
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                rel_path = os.path.relpath(from_path, content_dir)
                dest_rel_path = rel_path[:-3] + ".html"  # change .md to .html
                dest_path = os.path.join(public_dir, dest_rel_path)
                print(f"Generating page: {from_path} -> {dest_path}")
                generate_page(from_path, template_path, dest_path)