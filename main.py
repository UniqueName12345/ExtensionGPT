import os
import yaml
import textwrap
import re
import hfapi
import advinput

sandboxed_extension_template = """
class [extension id in camelCase] {
  getInfo() {
    return {
      id: '[extension id]',
      name: '[extension name]',
      blocks: [
        /* ... */
      ]
    };
  }

  // function definitions here
}

Scratch.extensions.register(new [extension id in camelCase]());
"""

unsandboxed_extension_template = """
(function(Scratch) {
  'use strict';
  class [extension id in camelCase] {
    getInfo () {
      return {
        id: '[extension id]',
        name: '[extension name]',
        blocks: [
            /* ... */
        ]};
    }
  }
  Scratch.extensions.register(new [extension id in camelCase]());
})(Scratch);
"""



# Setup AI
token = os.environ.get("HFTOKEN")
client = hfapi.Client(token)

# Setup Config
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)


def cls():
    """
    Clear the console by executing the appropriate command based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def _createfile(path: str) -> None:
    """
    Create a file at the specified path.

    Args:
        path (str): The path where the file should be created.
    """
    if os.name == "nt":
        path = path.replace("/", "\\")
        os.system(f"powershell.exe New-Item -Path {path} -ItemType File")
    else:
        os.system(f"touch {path}")


def get_extension_path_format(extension_name: str, extension_id: str) -> None:
    """
    Updates the extension path format based on the configuration and user input.

    Args:
        extension_name: The name of the extension.
        extension_id: The ID of the extension.

    Returns:
        The updated extension path format.
    """
    if config["is_turbowarp"]:
        os.system("python launchturbowarp.py")
        extensions_path_format = "[server_path]/extensions/[username]/[name_of_extension].js"
        if os.name == "nt":
            extensions_path_format = extensions_path_format.replace("/", "\\")
    else:
        print("The extension format is like a secret code with four placeholders: [server_path], [username], [name_of_extension], and [extension_id]. Let me know how you're playing this extension game!")
        extensions_path_format = input()

    extension_path_format = turn_placeholders_into_actual_useable_data(extensions_path_format, config["server_path"], config["username"], extension_name, extension_id)
    return extension_path_format

def detect_extension_type(template: str) -> str:
    """
    Detects the type of extension based on the given template.
    
    Args:
        template (str): The template code to check.
        
    Returns:
        str: The type of extension detected. Possible values are "sandboxed",
             "unsandboxed", and "unknown".
    """
    if "class" in template and "Scratch.extensions.register(new" in template and not "(function(Scratch) {" in template:
        return "sandboxed"
    elif "(function(Scratch) {" in template and "Scratch.extensions.register(new" in template:
        return "unsandboxed"
    else:
        return "unknown"

def turn_placeholders_into_actual_useable_data(string: str, server_path: str, username: str, extension_name: str, extension_id: str) -> str:
    """
    Replaces placeholders in a string with actual values.

    Args:
        string (str): The string containing the placeholders.
        server_path (str): The server path value to replace.
        username (str): The username value to replace.
        extension_name (str): The extension name value to replace.
        extension_id (str): The extension ID value to replace.

    Returns:
        str: The updated string with the placeholders replaced.
    """
    placeholders = {
        "[server_path]": server_path,
        "[username]": username,
        "[name_of_extension]": extension_name,
        "[extension_id]": extension_id
    }
    for placeholder, value in placeholders.items():
        string = string.replace(placeholder, value)
    
    return string

def to_camel_case(string: str) -> str:
    """
    Convert a string from snake case or kebab case to camel case.

    Args:
        string: The input string in snake case or kebab case.

    Returns:
        The converted string in camel case.
    """
    words = re.split(r'[_-]+', string)
    camel_case = ''.join([word.capitalize() for word in words])
    return camel_case[0].lower() + camel_case[1:]

def turn_template_into_useable_data(string: str, extension_name: str, extension_id: str) -> str:
    """
    Turn the given template string into useable data.

    Args:
        string (str): The template string.
        extension_name (str): The name of the extension.
        extension_id (str): The ID of the extension.

    Returns:
        str: The specific extension template with placeholders replaced.

    Raises:
        ValueError: If the extension type is unknown.
    """
    is_sandboxed = detect_extension_type(string)
    specific_extension_template = ""
    sandboxed_extension_template_temp = sandboxed_extension_template

    if is_sandboxed == "sandboxed" or is_sandboxed == "unsandboxed":
        # for the "class [extension id in camelCase]" part, we need to replace the placeholder with the extension ID in camel case
        extension_id_temp = to_camel_case(extension_id)
        specific_extension_template = sandboxed_extension_template_temp.replace("[extension id in camelCase]", extension_id_temp)
        # for the id: '[extension id]' bit, we need to replace the placeholder with the extension ID
        specific_extension_template = specific_extension_template.replace("[extension id]", extension_id)
        # for the name: '[extension name]' bit, we need to replace the placeholder with the extension name
        specific_extension_template = specific_extension_template.replace("[extension name]", extension_name)
        return specific_extension_template
    else:
        raise ValueError("Unknown extension type")


def create_sandboxed_extension(extension_name: str, extension_id: str, extensions_path_format: str):
    specific_extension_template = turn_template_into_useable_data(sandboxed_extension_template, extension_name, extension_id)
        # replace the contents of the file with the sandboxed template
        with open(extensions_path_format, "w") as f:
            f.write(specific_extension_template)

def create_unsandboxed_extension(extension_name: str, extension_id: str, extensions_path_format: str):
    specific_extension_template = turn_template_into_useable_data(unsandboxed_extension_template, extension_name, extension_id)
        # replace the contents of the file with the sandboxed template
        with open(extensions_path_format, "w") as f:
            f.write(specific_extension_template)

# Setup CLI
def create_file():
    change_screen("main_menu", "create_extension")
    print("Enter the name of the extension you want to create:")
    extension_name = input()

    print("Enter the extension id (it is highly recommended to be '[your username in lowercase][name of extension in lowercase]'):")
    extension_id = input()


    cls()

    extensions_path_format = get_extension_path_format(extension_name, extension_id)

    # create file at that path
    _createfile(extensions_path_format)

    # Display success message
    print(
        f"Extension '{extension_name}.js' created at '{extensions_path_format}'"
    )

    # Ask wether or not you want the extension to be sandboxed
    advinput.handle_input(
        "Do you want the extension to be sandboxed?",
        ["Yes", "No"],
        "create_extension",
        {
            1: create_sandboxed_extension(extension_name, extension_id, extensions_path_format),
            2: create_unsandboxed_extension(extension_name, extension_id, extensions_path_format)
        }
    )
cls()

def change_screen(emigrated_screen: str, immigrating_screen: str) -> None:
    """
    Change the current screen to a new screen.

    Args:
        emigrated_screen (str): The screen that the user is currently on.
        immigrating_screen (str): The screen that the user is transitioning to.

    Returns:
        None
    """
    prev_screen: str = emigrated_screen
    current_screen: str = immigrating_screen


def main():
    current_screen = "main_menu"
    
    while True:
        if current_screen == "main_menu":
            advinput.handle_input(
                "What do you want to do?",
                ["Create a new extension", "Exit"],
                current_screen,
                {
                    1: create_file,
                    2: exit
                },
                "Invalid option. Please try again.",
            )


# Run the CLI
main()