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
from commands.psnr import do_psnr
from commands.histogram import do_histogram
from commands.hhyper import do_hhyper
from commands.sedghesharp_optimized import do_sedghesharp_opt
from commands.image_characteristics.cmean import do_cmean
from commands.image_characteristics.cvariance import do_cvariance
from commands.image_characteristics.cstdev import do_cstdev
from commands.image_characteristics.cvarcoi import do_cvarcoi
from commands.image_characteristics.cvarcoii import do_cvarcoii
from commands.image_characteristics.casyco import do_casyco
from commands.image_characteristics.cflattening import do_cflattening
from commands.sedghesharp import do_sedghesharp
from commands.kirsh_operator import do_kirsh_operator
from commands.mask_filter import do_mask_filter
from commands.image_characteristics.centropy import do_centropy
from commands.morphological.dilation import do_dilation
from structural_elements import STRUCT_ELEMENTS
from commands.morphological.erosion import do_erosion
from commands.morphological.opening import do_opening
from commands. morphological.closing import do_closing
from commands.morphological.HMT_transformation import do_hmt
from commands.region_growing import do_region_growing
from commands.m4 import do_m4
from commands.morphological.dilation_optimized import do_dilation_optimized
from commands.morphological.erosion_optimized import do_erosion_optimized
from commands.fourier_ops.do_high_cut import do_high_cut
from commands.fourier_ops.do_low_cut import do_low_cut
from commands.fourier_ops.do_fft_vis import do_fft_vis
from commands.fourier_ops.do_band_cut import do_band_cut
from commands.fourier_ops.do_directional_highpass import do_dir_highpass
from commands.fourier_ops.do_phase_modifying import do_phase_modifying

"""
TASK VARIANTS:
Task 1: (all B, all G, N5, all E)
Task 2: (H5, all C, S2, O4)
Task 3: (M4, all R)
Task 4 (T2, all F)
"""
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
    "--histogram": do_histogram,
    "--hhyper": do_hhyper,
    "--sedgesharp": do_sedghesharp,
    "--okirsf" : do_kirsh_operator,
    "--maskfltr": do_mask_filter,
    "--sedgesharpopt": do_sedghesharp_opt,
    "--m4": do_m4,
    "--reggrow": do_region_growing,
    "--highcut": do_high_cut,
    "--lowcut": do_low_cut,
    "--fftvis": do_fft_vis,
    "--bandcut": do_band_cut,
    "--dir_highpass": do_dir_highpass,
    "--phase_mod": do_phase_modifying
}

SIMILARITY = {
    "--mse": do_mean_square_error,
    "--pmse": do_peak_mse,
    "--snr": do_signal_to_noise,
    "--psnr": do_psnr,
    "--md": do_max_difference
}
CHARACTERISTICS = {
    "--cmean": do_cmean,
    "--cvariance": do_cvariance,
    "--cstdev": do_cstdev,
    "--cvarcoi": do_cvarcoi,
    "--cvarcoii": do_cvarcoii,
    "--casyco": do_casyco,
    "--cflattening": do_cflattening,
    "--centropy": do_centropy
}
MORPHOLOGY = {
    "--dilation": do_dilation,
    "--erosion": do_erosion,
    "--opening": do_opening,
    "--closing": do_closing,
    "--hmt": do_hmt,
    "--dilationo": do_dilation_optimized,
    "--erosiono": do_erosion_optimized
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
        print(str(round(value,4)))

    if command in CHARACTERISTICS:
        image = load_image(args.get('-input'))
        result = CHARACTERISTICS[command](image, args)
        print(result)
        
    else:
        input_path = args.get('-input')
        output_path = args.get('-output')
        
        im = load_image(input_path)

        if command in MORPHOLOGY:
            struct_name = args.get('-struct')
            if struct_name in STRUCT_ELEMENTS:
                struct = STRUCT_ELEMENTS[struct_name]
                newIm = MORPHOLOGY[command](im, struct, args)
                save_image(output_path, newIm)
            else: 
                print(f"Error: Structural element '{struct_name} not found in structural_elements.py")
        else:
            try:
                newIm = COMMANDS[command](im, args)
                if (output_path is not None):
                    save_image(output_path, newIm)

            except KeyError:
                print("Command not found.\n")

    


