import os
import shutil
import sys

from block_markdown import markdown_to_html_node


def copy_tree(source_path, destination_path):
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    for item in os.listdir(source_path):
        if os.path.isfile(os.path.join(source_path, item)):
            shutil.copy(os.path.join(source_path, item), os.path.join(destination_path, item))
        else:
            copy_tree(os.path.join(source_path, item), os.path.join(destination_path, item))

def extract_title(markdown):
    lines = markdown.split("/n")
    for line in lines:
        if line.startswith("# "):
            return line.replace("# ", "")
    raise Exception("There is no h1 in markdown")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path, "r") as f:
        markdown += f.read()
    with open(template_path, "r") as f:
        template += f.read()
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    with open(dest_path[:-2] + 'html', 'w') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for item in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, item)):
           generate_page(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item), basepath)
        else:
            generate_pages_recursive(os.path.join(dir_path_content,item), template_path, os.path.join(dest_dir_path, item), basepath)

def main():
    basepath = sys.argv[0]
    shutil.rmtree("./docs")
    copy_tree("./static/", "./docs")
    generate_pages_recursive("./content/", "./template.html", "./docs/", basepath)


main()