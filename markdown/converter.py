# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "numpy",
# ]
# ///
import argparse
import datetime
import os
import re
import numpy as np


def convert(filename):
    # read in input file
    with open(filename, "rt") as f:
        content = f.read()

    # Find code blocks
    done = False
    while not done:
        (content, n_subs) = re.subn("```", "<pre>", content, count=1)
        if n_subs == 0:
            done = True

        content = re.sub("```", "</pre>", content, count=1)

    lines = content.split("\n")
    n_lines = len(lines)
    last_break = n_lines

    # separate out blocks
    ##########################################
    # A list of list of lines
    blocks = []

    for i_line in np.flip(np.arange(n_lines)):
        if(lines[i_line] == "" or lines[i_line].isspace()):
            # This is an empty line
            if last_break - i_line > 1:
                blocks.append("\n".join(lines[i_line + 1 : last_break]))

            last_break = i_line

    if last_break > 0:
        blocks.append("\n".join(lines[: last_break]))

    blocks.reverse()

    converted_blocks = []
    for block in blocks:

        # convert horizontal line
        if block[:5] in ["-----", "_____", "====="]:
            block = "<hr>"

        # special character conversions
        # Here are a bunch of others:
        # https://web.html.support/reference/greek-characters.cfm
        block = re.sub("---", "&mdash;", block)
        block = re.sub(r'\$<\$', "&lt;", block)
        block = re.sub(r'\$>\$', "&gt;", block)
        block = re.sub(r'\$\*\$', r'&#42;', block)
        block = re.sub(r'\$pi\$', "&pi;", block)
        block = re.sub(r'\$deg\$', "&#176;", block)
        block = re.sub(r'\$epsilon\$', "&epsilon;", block)
        block = re.sub(r'\$theta\$', "&theta;", block)
        block = re.sub(r'\$tau\$', "&tau;", block)
        block = re.sub(r'\$omega\$', "&omega;", block)
        block = re.sub(r'\$blackcircle\$', "&#9899;", block)
        block = re.sub(r'\$whitecircle\$', "&#9711;", block)
        block = re.sub(r'\$lowerhalfblackcircle\$', "&#9682;", block)

        # convert images
        # ![A diagram](images/pendulum.png "Pendulum")
        # <img title="Pendulum" alt="A diagram" src="/images/pendulum.png">
        block = re.sub(
            r'!\[([^\[]+)\]\((.*) "(.*)"\)',
            r'''<figure>
  <img title="\3" alt="\1" src="\2">
  <figcaption>\3</figcaption>
</figure>''',
            block
        )

        # ![A diagram](images/pendulum.png)
        # <img alt="A diagram" src="/images/pendulum.png">
        block = re.sub(
            r'!\[([^\[]+)\]\((.*)\)',
            r'<img alt="\1" src="\2">',
            block
        )

        # convert embedded vimeo videos
        # ^[A video](vimeo_url)
        block = re.sub(
            r'\^\[([^\[]+)\]\((.*)\)',
            r'<iframe src="\2?title=0&byline=0&portrait=0&badge=0&autopause=0&player_id=0&app_id=58479&embedded=true" width="660" height="400" frameborder="0"  allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media" title="\1"></iframe>',
            block
        )

        # convert links
        # \[          exact match for opening square bracket
        #   (         begin group 0
        #    [^\[]    any characters except an opening square bracket
        #         +   1 or more, as many as possible
        #   )         end group 0
        # \]          exact match for closing square bracket
        # \(          exact match for opening parenthesis
        #   (         begin group 1
        #    .        any character
        #     *       0 or more, as many as possible
        #   )         end group 1
        # \)          exact match for closing parenthesis
        block = re.sub(r'\[([^\[]+)\]\((.*)\)', r'<a href="\2">\1</a>', block)

        # convert bold
        # \*\*        exact match for "**"
        #   (         begin group 0
        #    .        any characters
        #     +?       1 or more, as few as possible, but as many as it needs to
        #   )         end group 0
        # \*\*        exact match for closing square bracket
        block = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', block)

        # convert italics
        # regex = r'\*(.+?)\*'
        # \*        exact match for "*"
        #   (         begin group 0
        #    .        any characters
        #     +?       1 or more, as few as possible, but as many as it needs to
        #   )         end group 0
        # \*        exact match for closing square bracket
        block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)

        # convert strikethrough
        # ~~          exact match for "**"
        #   (         begin group 0
        #    .        any characters
        #     +?       1 or more, as few as possible, but as many as it needs to
        #   )         end group 0
        # ~~          exact match for closing square bracket
        block = re.sub(r'~~(.+?)~~', r'<del>\1</del>', block)

        # convert inline code
        block = re.sub(r'`(.+?)`', r'<code>\1</code>', block)

        # convert headings
        if block[:4] == "####":
            heading = block[5:]
            link_name = "-".join(heading.split(" "))
            block = (
                f'<h4><a id="{link_name}">' +
                f'</a><a href="#{link_name}">' +
                f'{heading}</a></h4>'
            )
        elif block[:3] == "###":
            heading = block[4:]
            link_name = "-".join(heading.split(" "))
            block = (
                f'<h3><a id="{link_name}">' +
                f'</a><a href="#{link_name}">' +
                f'{heading}</a></h3>'
            )
        elif block[:2] == "##":
            heading = block[3:]
            link_name = "-".join(heading.split(" "))
            block = (
                f'<h2><a id="{link_name}">' +
                f'</a><a href="#{link_name}">' +
                f'{heading}</a></h2>'
            )

        # Pull out the top level heading as the title.
        # Better not have more than one of these
        elif block[:1] == "#":
            title = block[2:]
            continue
        # convert lists
        elif block[:2] in ["- ", "* "]:
            block = convert_block_to_unordered_list(block)
        elif re.match(r'\A[0-9]*\.', block):
            block = convert_block_to_ordered_list(block)
        elif block[0] == "|" and block[-1] == "|":
            block = convert_block_to_table(block)
        else:
            # handle paragraphs
            block = "<p>\n" + block + "\n</p>"

        converted_blocks.append(block)

    blocks = converted_blocks

    # save converted file
    with open("header.html", "rt") as f:
        html_header = f.read()
    html_header = re.sub("put_title_here", title, html_header)

    today = datetime.datetime.now()
    formatted_date = today.strftime("%B %d, %Y")
    html_header = re.sub("put_date_here", formatted_date, html_header)

    with open("footer.html", "rt") as f:
        html_footer = f.read()

    html_content = "\n\n".join(blocks)
    html_all = "\n\n".join([html_header, html_content, html_footer])

    html_filename = ".".join(filename.split(".")[:-1] + ["html"])
    try:
        os.rename(
            os.path.join("..", "html", html_filename),
            os.path.join("..", "html", html_filename + ".bak")
        )
    except FileNotFoundError:
        pass

    with open(os.path.join("..", "html", html_filename), "wt") as f:
        f.write(html_all)


def convert_block_to_unordered_list(block):
    # Break on each list item beginning
    # (         begin group 0
    #  \A       beginning of string
    #    |      either-or 
    #     \n    newline
    # )         end group 0
    # (         begin group 1
    #  [        begin set
    #   \*\-    "*" or "-" character
    #  ]        end set
    #   <space> spaces patter
    # )         end group 1
    block = re.sub(r'(\A|\n)([\*\-] )', r'</li>\n<li> ', block)
    # roll the initial </li> around to the end
    block = block[6:] + block[:5]
    block = "<ul>\n" + block + "\n</ul>"
    # Turn segments into list items
    return block


def convert_block_to_ordered_list(block):
    # Break on each list item beginning
    # (         begin group 0
    #  \A       beginning of string
    #    |      either-or 
    #     \n    newline
    # )         end group 0
    # (         begin group 1
    #  [        begin set
    #   \*\-    "*" or "-" character
    #  ]        end set
    #   <space> spaces patter
    # )         end group 1
    block = re.sub(r'(\A|\n)([0-9]*\. )', r'</li>\n<li> ', block)
    # roll the initial </li> around to the end
    block = block[6:] + block[:5]
    block = "<ol>\n" + block + "\n</ol>"
    # Turn segments into list items
    return block


def convert_block_to_table(block):
    """
    Markdown for tables will be formatted like this:

|Header1 |Header2  | Header3|
| --- | --- | ---|
|data1|data2|data3|
|data11|data12|data13|

    But needs to end up like this:

<table>
  <thead>
    <tr>
      <th>Header1</th>
      <th>Header2</th>
      <th>Header3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>data1</td>
      <td>data2</td>
      <td>data3</td>
    </tr>
    <tr>
      <td>data11</td>
      <td>data12</td>
      <td>data13</td>
    </tr>
  </tbody>
</table>
    """
    html = """<table>
  <thead>
    <tr>
"""

    rows = block.split("\n")
    header_cells = rows[0].strip().split("|")[1 : -1]
    for header_cell in header_cells:
        html += f"      <th>{header_cell.strip()}</th>\n"
    html += """
    </tr>
  </thead>
  <tbody>
"""
    # skip row 1, showing the heaading divider
    for row in rows[2:]:
        html += "    <tr>\n"
        cells = row.strip().split("|")[1 : -1]
        for cell in cells:
            html += f"      <td>{cell.strip()}</td>\n"
        html += "    </tr>\n"
    html += """ </tbody>
</table>
"""
    return html

# input filename as command line argument
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    convert(args.filename)
