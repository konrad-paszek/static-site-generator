from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        tmp = []
        tmp_text = node.text
        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
            continue
        for image in images:
            sections = tmp_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                tmp.append(TextNode(sections[0], TextType.TEXT))
            tmp.append(TextNode(image[0], TextType.IMAGE, image[1]))
            tmp_text = "".join(sections[1])
        if tmp_text != "":
            tmp.append(TextNode(tmp_text, TextType.TEXT))
        result.extend(tmp)
    return result

def split_nodes_link(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        tmp = []
        tmp_text = node.text
        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
            continue
        for link in links:
            sections = tmp_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                tmp.append(TextNode(sections[0], TextType.TEXT))
            tmp.append(TextNode(link[0], TextType.LINK, link[1]))
            tmp_text = "".join(sections[1])
        if tmp_text != "":
            tmp.append(TextNode(tmp_text, TextType.TEXT))
        result.extend(tmp)
    return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)



