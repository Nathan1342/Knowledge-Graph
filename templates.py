from pathlib import Path
from datetime import datetime
import os

def create_md_template(output_path: Path, template_type: str, title: str):
    """Method creating .md file note with specific template and opens it"""

    if not output_path.exists():
        raise FileNotFoundError("Output folder does not exist")

    if not output_path.is_dir():
        raise NotADirectoryError("Output path is not a folder")

    if template_type not in ["alg", "ds"]:
        raise TypeError("Template must be 'alg' or 'ds'")

    title = title.lower().replace(" ", "_")

    if template_type == "alg":
        template = create_algorithm_template(title)
    if template_type == "ds":
        template = create_data_structure_template(title)

    full_path = output_path / (title + ".md")
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(template)
    os.startfile(str(full_path))

def title_parser(title: str):
    """Changing lowercase title with underscores into
    title with spaces and first uppercase"""

    result = title.lower().replace("_", " ")
    result = result[0].upper() + result[1:]

    return result


def create_algorithm_template(title: str):
    """Method creating string with .md file algorithm template"""

    # Getting current date and time
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M")

    # Parsing title
    title = title_parser(title)

    template = f"""
    #Title: {title}
    date: {date}
    type: algorithm

    ## Purpose
    What problem does this algorithm solve?

    ## Core Idea
    Explain the intuition behind it.

    ## Prerequisites
    What data structures or concepts are needed?

    ## Input

    ## Output

    ## Steps


    ## Time Complexity

    ## Space Complexity

    ## Advantages

    ## Limitations

    ## When To Use

    ## When NOT To Use

    ## Data Structures Used

    ## Alternatives
    What algorithms solve a similar problem?

    ## Real World Applications

    ## Related Concepts

    ## Implementation Notes

    ## Common Mistakes

    ## Example Problems

    ## My Insights
    Your own observations after solving problems with it.
    """
    return template

def create_data_structure_template(title: str):
    """Method creating string in .md format of data structure"""

    # Getting current date and time
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M")

    # Parsing title
    title = title_parser(title)

    template = f"""
        #Title: {title}
        date: {date}
        type: data structure

        ## Purpose
        What problem does this data structure solve? Why was it invented?

        ## Core Idea
        Describe the internal mechanism. How does it work?

        ## Operations
        - Insert:
        - Delete:
        - Search:
        - Access:

        ## Time Complexity

        | Operation | Average | Worst |
        | Insert | | |
        | Delete | | |
        | Search | | |
        | Access | | |

        ## Space Complexity

        ## Advantages

        ## Disadvantages

        ## Typical Use Cases

        ## Real World Applications

        ## Alternatives
        When would another data structure be a better choice?

        ## Related Concepts

        ## Implementation Notes
        Things to remember while implementing.

        ## Common Mistakes

        ## Interesting Facts

        ## Example Problems

        ## My Insights
        Your own thoughts and observations.
        """
    return template
