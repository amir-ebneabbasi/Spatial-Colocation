import os
import requests

def fetch_neurotransmitter_maps(
    data_dir="./neurotransmitter_maps",
    repo_api_url="https://api.github.com/repos/justinehansen/hansen_receptors-1/contents/data/PET_nifti_images",
    overwrite=False,
    verbose=True
):

    os.makedirs(data_dir, exist_ok=True)

    response = requests.get(repo_api_url)

    if response.status_code != 200:
        raise RuntimeError(f"GitHub API failed: {response.status_code}")

    files = response.json()

    filenames = [
        f["name"]
        for f in files
        if f["type"] == "file"
        and (f["name"].endswith(".nii") or f["name"].endswith(".nii.gz"))
    ]

    if verbose:
        print(f"Found {len(filenames)} NIfTI files")

    downloaded = []
    skipped = []
    failed = []

    for f in files:
        name = f["name"]

        if name not in filenames:
            continue

        out_path = os.path.join(data_dir, name)

        if os.path.exists(out_path) and not overwrite:
            skipped.append(name)
            if verbose:
                print(f"Skipped: {name}")
            continue

        try:
            r = requests.get(f["download_url"])

            if r.status_code == 200:
                with open(out_path, "wb") as file:
                    file.write(r.content)

                downloaded.append(out_path)

                if verbose:
                    print(f"Downloaded: {name}")
            else:
                failed.append((name, r.status_code))
                if verbose:
                    print(f"Failed: {name} ({r.status_code})")

        except Exception as e:
            failed.append((name, str(e)))
            if verbose:
                print(f"Error: {name} → {e}")

    return downloaded, skipped, failed, filenames