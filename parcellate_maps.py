def parcellate_volumetric_maps(path, atlas_path, save_csv=True):

    import numpy as np
    from neuromaps.parcellate import Parcellater
    import os
    import glob

    maps = glob.glob(os.path.join(path, "*.gz"))
    parcellater = Parcellater(atlas_path, 'MNI152')

    parcellated = {}

    for map_file in maps:
        try:
            result = parcellater.fit_transform(map_file, 'MNI152', True)
            parcellated[map_file] = result

            if save_csv:
                name = os.path.basename(map_file).split('.')[0]
                output_file = os.path.join(path, f"{name}.csv")
                np.savetxt(output_file, result, delimiter=',')

            print(f"Parcellated and saved: {os.path.basename(map_file)}")

        except Exception as e:
            print(f"Error processing {map_file}: {e}")

    return parcellated