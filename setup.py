import os
import yaml
import getpass
import subprocess
import textwrap
import sys

def cls():
    """
    Clear the console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input(prompt, secret=False):
    """
    Prompt the user for input. If 'secret' is True, use getpass to hide the input.
    """
    if secret:
        try:
            return getpass.getpass(prompt)
        except ImportError:
            print("Warning: 'getpass' module not available. Input will be visible.")
    return input(prompt)

def save_config(token, server_path, is_turbowarp, username):
    """
    Save the configuration to config.yaml
    """
    config_data = {
        'token': token,
        'server_path': server_path,
        'is_turbowarp': is_turbowarp,
        'username': username
    }

    with open('config.yaml', 'w') as config_file:
        yaml.safe_dump(config_data, config_file)

def is_program_setup():
    """
    Check if the program is already setup.
    """
    return os.path.isfile('config.yaml')

def run_program():
    """
    Run the main program.
    """
    subprocess.run(["python", "main.py"])

def main():
    if is_program_setup():
        run_program()
    else:
        cls()
        print("""
        _______ _______ _______ _     _  _____ 
        |______ |______    |    |     | |_____]
        ______| |______    |    |_____| |      
        """)

        print(textwrap.dedent("""
            Hey there! Ready to dive into the ExtensionGPT setup journey. Buckle up, it's gonna be a breeze!
            =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="""
            ))
        
        # Check if -headless parameter is given
        if "-headless" in sys.argv:
            # Read installconf.yaml file
            with open("installconf.yaml") as f:
                install_config = yaml.safe_load(f)
            
            token = install_config.get("token")
            server_path = install_config.get("server_path")
            is_turbowarp = install_config.get("is_turbowarp")
            username = install_config.get("username")
        else:
            # Get user input
            token = get_user_input(textwrap.dedent("""
                Hey there! Ready to roll with some HuggingFace magic? If you've got your API token, drop it like it's hot. If not, no stress - just hop over to their site, create an account, and snag that shiny new token. Quick note: OpenAI keys won't cut it here, so make sure it's the right flavor.

                And hey, no need to stress about your token's security. It's got its own little nest on your local machine - ain't going anywhere without your say-so! """), secret=True)
            server_path = input("Yo, where's your personalized extensions server hangin' out? Drop that directory path, and ExtensionGPT will whip up some fresh extensions there! ")
            
            # Ask whether it's Turbowarp's "better extension server"
            is_turbowarp = input("You rollin' with Turbowarp's 'better extension server' vibes? Yes or no, spill the beans! ").lower() == 'yes'
            
            if is_turbowarp:
                username = get_user_input("Drop that username you flex on Turbowarp with! It's all about that '[username]/[extension_name].js' game. What's yours? ")
        
        # Store the token in environment variable
        os.environ["HFTOKEN"] = token
    
        # Save configuration in config.yaml
        save_config(token, server_path, is_turbowarp, username)
    
        cls()

        print(textwrap.dedent('''
            Alright, setup's a go! 
            Time to give that program a little restart dance to get things rolling with ExtensionGPT. 
            If you gotta tweak some settings down the road, remember to dive into the config.yaml file - that's your go-to manual adjustments spot.

            Quick heads-up: If you ever somehow get hit with a "KeyError: 'HFTOKEN'" message, no need to break a sweat. 
            Just whip up an environ called 'HFTOKEN' and toss your token in there.

            For the Windows crew, hit up the command line with "> setx HFTOKEN [your token]". 
            Mac folks, it's "> export HFTOKEN=[your token]" in your terminal. 
            And Linux peeps, you're on the same boat - "> export HFTOKEN=[your token]" in your terminal wizardry. Happy coding!
        '''))

if __name__ == "__main__":
    main()
