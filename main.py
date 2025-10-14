import sys
from input_output import load_image, save_image
from commands.brightness import do_brightness
from commands.help import do_help
from commands.contrast import do_contrast
from commands.negative import do_negative
from commands.horizontal import do_horizontal_flip
from commands.vertical import do_vertical_flip
from commands.diagonal import do_diagonal_flip
from commands.adaptive import do_adaptive_noise_filter
from commands.shrinking import do_shrinking
from commands.enlargement import do_enlargement
from commands.min import do_min_filer
from commands.max import do_max_filer
from commands.mean_square_error import do_mean_square_error
from commands.peak_mse import do_peak_mse
from commands.signal_to_noise_ratio import do_signal_to_noise
from commands.max_difference import do_max_difference
from commands.snr import do_snr
from commands.psnr import do_psnr

COMMANDS = {
    "--brightness": do_brightness,
    "--help": do_help,
    "--contrast": do_contrast,
    "--hflip": do_horizontal_flip,
    "--negative": do_negative,
    "--vflip": do_vertical_flip,
    "--dflip": do_diagonal_flip,
    "--adaptive": do_adaptive_noise_filter,
    "--shrink": do_shrinking,
    "--enlarge": do_enlargement,
    "--min": do_min_filer,
    "--max": do_max_filer,
}

SIMILARITY = {
    "--mse": do_mean_square_error,
    "--pmse": do_peak_mse,
    "--snr": do_snr,
    "--psnr": do_psnr,
    "--md": do_max_difference
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

    if command in SIMILARITY:
        original = load_image(args.get('-original'))
        other = load_image(args.get('-other'))
        value = SIMILARITY[command](original, other)
        print(str(value))

    else:
        input_path = args.get('-input')
        output_path = args.get('-output')

        im = load_image(input_path)
        try:
            newIm = COMMANDS[command](im, args)
            save_image(output_path, newIm)

        except KeyError:
            print("Command not found.\n")

    print("")
