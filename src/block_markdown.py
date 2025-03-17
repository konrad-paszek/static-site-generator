import re
from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = re.split(r'\n\s*\n', markdown.strip())

    filtered_blocks = [block.strip() for block in blocks if block.strip()]

    return filtered_blocks

def block_to_block_type(block: str):
    lines = block.split("\n")
    result = []
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif len(lines) > 1 and block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    for index, line in enumerate(lines, 1):
        result.append((index, line))
    if len([x for x in result if x[1].startswith(">")]) == len(result):
        return BlockType.QUOTE
    elif len([x for x in result if x[1].startswith("- ")]) == len(result):
        return BlockType.ULIST
    elif len([x for x in result if x[1].startswith(f"{x[0]}. ")]) == len(result):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH


def block_to_paragraph(block):
    tag = 'p'
    lines = block.split("\n")
    children = []
    for line in lines[:-1]:
        children.extend(text_to_children(line + ' '))
    children.extend(text_to_children(lines[-1]))
    return children, tag


def block_to_ordered_list(block):
    tag = 'ol'
    lines = block.split("\n")
    children = []
    for index, line in enumerate(lines, 1):
        children.extend(text_to_children(line.replace(f'{index}. ', '<li>') + '</li>'))
    return children, tag


def block_to_unordered_list(block):
    tag = 'ul'
    lines = block.split("\n")
    children = []
    for line in lines:
        children.extend(text_to_children(line.replace('- ', '<li>') + '</li>'))
    return children, tag


def block_to_heading(block):
    tag = ''
    lines = block.split("\n")
    children = []
    for line in lines:
        if line.startswith('######'):
            children.extend(text_to_children(line.replace('######', '').strip()))
            tag += 'h6'
        elif line.startswith('#####'):
            children.extend(text_to_children(line.replace('#####', '').strip()))
            tag += 'h5'
        elif line.startswith('####'):
            children.extend(text_to_children(line.replace('####', '').strip()))
            tag += 'h4'
        elif line.startswith('###'):
            children.extend(text_to_children(line.replace('###', '').strip()))
            tag += 'h3'
        elif line.startswith('##'):
            children.extend(text_to_children(line.replace('##', '').strip()))
            tag += 'h2'
        elif line.startswith('#'):
            children.extend(text_to_children(line.replace('#', '').strip()))
            tag += 'h1'

    return children, tag


def block_to_blockquote(block):
    tag = "blockquote"
    lines = block.split("\n")
    children = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        children.append(line.lstrip(">").strip())
    content = " ".join(children)
    children = text_to_children(content)
    return children, tag


def block_to_code(block):
    tag = 'pre'
    children = []
    node = TextNode(block[4:-3], TextType.CODE)
    children.append(text_node_to_html_node(node))
    return children, tag


def get_tag_from_block_type(block_type: BlockType, block):
    if block_type == BlockType.HEADING:
        return block_to_heading(block)
    elif block_type == BlockType.PARAGRAPH:
        return block_to_paragraph(block)
    elif block_type == BlockType.QUOTE:
        return block_to_blockquote(block)
    elif block_type == BlockType.CODE:
        return block_to_code(block)
    elif block_type == BlockType.OLIST:
        return block_to_ordered_list(block)
    elif block_type == BlockType.ULIST:
        return block_to_unordered_list(block)

def text_to_children(text):
    result = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        result.append(text_node_to_html_node(textnode))
    return result


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div = ParentNode("div", children=[])
    for block in blocks:
        block_type = block_to_block_type(block)
        children, block_tag = get_tag_from_block_type(block_type, block)
        block_node = ParentNode(tag=block_tag, children=children)
        div.children.append(block_node)
    return div






