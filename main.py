import sys
from input_output import load_image, save_image
from commands.brightness import do_brightness
from commands.help import do_help
from commands.contrast import do_contrast
from commands.negative import do_negative
from commands.horizontal import do_horizontal_flip
from commands.vertical import do_vertical_flip
from commands.adaptive import do_adaptive_noise_filter

COMMANDS = {
    "--brightness": do_brightness,
    "--help": do_help,
    "--contrast": do_contrast,
    "--horizontal": do_horizontal_flip,
    "--negative": do_negative,
    "--vertical": do_vertical_flip,
    "--adaptive": do_adaptive_noise_filter,
}


if len(sys.argv) == 1:
    print("No command line parameters given.\n")
    sys.exit()

command = sys.argv[1]

if command == '--help':
    do_help()

else:
    if len(sys.argv) == 2:
        print("Too few command line parameters given.\n")
        sys.exit()

    args = {}
    for arg in sys.argv[2:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            args[key] = value
        else:
            print("Invalid argument:" + arg)

    input_path = args.get('-input')
    output_path = args.get('-output')

    

    im = load_image(input_path)
    try:
        newIm = COMMANDS[command](im, args)
        save_image(output_path, newIm)

    except KeyError:
        print("Command not found.\n")

    print("")
