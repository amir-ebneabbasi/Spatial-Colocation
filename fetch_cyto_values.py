def fetch_cyto_cortical_layers(
    out_dir="./cytoarchitectonics",
    github_base="https://raw.githubusercontent.com/kwagstyl/cortical_layers_tutorial/main/data/",
    save_csv=True,
    output_name="cyto_data.csv"
):

    import os
    import requests
    import nibabel as nb
    import numpy as np
    import pandas as pd
    from scipy import stats
    
    files = {
        "surf": "gray_left_327680.surf.gii",
        "parcellation": "HCP_left.txt",
        "labels": "HCP_labels.txt",
        "profiles": "profiles_left.npy",
        "thickness": "thicknesses_left.npy"
    }

    os.makedirs(out_dir, exist_ok=True)

    local_files = {}
    for key, fname in files.items():
        url = github_base + fname
        out_path = os.path.join(out_dir, fname)
        if not os.path.exists(out_path):
            response = requests.get(url)
            if response.status_code != 200:
                raise ValueError(f"Failed to download {fname}: HTTP {response.status_code}")
            with open(out_path, "wb") as f:
                f.write(response.content)
        local_files[key] = out_path

    surf = nb.load(local_files["surf"])
    vertices, faces = surf.darrays[0].data, surf.darrays[1].data
    parcellation = np.loadtxt(local_files["parcellation"], dtype=int)
    labels = np.loadtxt(local_files["labels"], dtype=str)
    profiles = np.load(local_files["profiles"])
    thickness = np.load(local_files["thickness"])

    roi_indices = [np.where(parcellation == i)[0] for i in range(len(labels))]

    roi_metrics = {
        'ROI': labels.tolist(),
        'Mean': [profiles[idx].mean() for idx in roi_indices],
        'Standard_Deviation': [profiles[idx].std() for idx in roi_indices]
    }

    for layer in range(6):
        roi_metrics[f'CT_layer_{layer+1}'] = [thickness[layer][idx].mean() for idx in roi_indices]

    df = pd.DataFrame(roi_metrics)

    if save_csv:
        out_path = os.path.join(out_dir, output_name)
        df.to_csv(out_path, index=False)

    return df
