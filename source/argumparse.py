from auxiliary import *

USAGE = """\
Usage: eng [-n EN RU [CONTEXT]] [-d WORD] 
           [-e WORD [-t RU] [-c CTX]] [-s PREFIX] [-l] [-t]

English Vocabulary Helper

Options:
  -h,                          show help message
  -n EN RU [CONTEXT]           add a new word
  -d WORD                      delete a word
  -e WORD [-t RU] [-c CONTEXT] edit entry: RU and/or CTX
  -s PREFIX                    words with a PREFIX beginning
  -l                           output the entire dictionary
  -t                           training mode
  --ai-state STATE             toggle AI context generation
                               ON or OFF (default OFF)
  --ai-key API_KEY             set Google Gemini API key\
"""

actions = {"-h", "-n", "-d", "-e", "-s", "-l", "-t", "--ai-state", "--ai-key"}

def save_config(config_data):
    """Saving the configuration to a JSON file"""
    try:
        with open(CONF_PATH, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving the configuration: {e}")
        return False


def parse_args(args):
    if not args:
        print(USAGE)
        return

    action, *other = args
    if not action:
        print(USAGE)
        return
    
    if action not in actions:
        print("Invalid option! See `eng -h`")
        return 
    
    if action == "-h":
        print(USAGE)
        return
    elif action == "--ai-state":
        if len(other) != 1:
            print("Expected ON or OFF after --ai-state. See `eng -h`")
            return

        state, *other = other
        config = load_config()

        if state == "ON":
            config["AI_ASSIST_ENABLED"] = True
            if save_config(config):
                print("AI context generation enabled.")
        elif state == "OFF":
            config["AI_ASSIST_ENABLED"] = False
            if save_config(config):
                print("AI context generation disabled.")
        else:
            print("Invalid state for --ai-state. Use ON or OFF. See `eng -h`")
    elif action == "--ai-key":
        if len(other) != 1:
            print("Expected API_KEY after --ai-key. See `eng -h`")
            return

        api_key, *other = other
        config = load_config()

        config["GOOGLE_GEMINI_API_KEY"] = api_key
        if save_config(config):
            print("Google Gemini API key saved to config.json")
        else:
            print("Failed to save API key to config.json")
    elif action == "-n":
        if len(other) < 2:
            print("Expected arguments EN RU. See `eng -h`")
            return
        
        en, ru, *other = other
        if other and len(other) < 1:
            print("Invalid syntax! See `eng -h`")
            return
        
        ctx = " ".join(other) if other else None
        add_word(en, ru, ctx)
    elif action == "-d":
        if len(other) != 1:
            print("Expected single argument WORD. See `eng -h`")
            return
    
        word, *_ = other
        delete_word(word)
    elif action == "-e":
        if not other:
            print("Expected argument WORD. See `eng -h`")
            return

        en, *other = other
        if not other:
            print("Nothing changed!")
            return

        try:
            idx_t = other.index("-t")
        except ValueError:
            idx_t = None

        try:
            idx_c = other.index("-c")
        except ValueError:
            idx_c = None

        if None not in (idx_t, idx_c) and idx_t > idx_c:
            print("Option -t must come before option -c!")
            return

        ru = None
        if idx_t is not None:
            if idx_t + 1 >= len(other):
                print("Expected parameter RU!")
                return
            ru = other[idx_t + 1]

        ctx = None
        if idx_c is not None:
            ctx_args = other[idx_c + 1:]
            if not ctx_args:
                print("Expected parameter CONTEXT!")
                return
            ctx = " ".join(ctx_args)
        edit_word(en, ru, ctx)
    elif action == "-s":
        if len(other) != 1:
            print("Expected argument PREFIX. See `eng -h`")
            return
        prefix, *_ = other
        show_by_prefix(prefix)
    elif action == "-l":
        if len(other) != 0:
            print("Extra arguments! See `eng -h`")
            return
        list_all()
    elif action == "-t":
        if len(other) != 0:
            print("Extra arguments! See `eng -h`")
            return
        training_mode()
    else:
        print(":(")