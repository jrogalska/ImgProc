import sys
from input_output import load_image, save_image
from commands.brightness import do_brightness
from commands.help import do_help

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

    if command == '--brightness':
        im = load_image(input_path)
        const = int(args.get('-const', 0))
        newIm = do_brightness(im, const)
        save_image(output_path, newIm)

    else:
        print("Unknown command: " + command)
    print("")
