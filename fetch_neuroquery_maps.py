def fetch_neuroquery_maps(
    terms=None,
    use_cognitive_atlas=False,
    data_dir="./neuroquery_maps",
    encoder=None,
    verbose=True
):

    import os
    import requests
    import pandas as pd
    import nibabel as nib
    from neuroquery import fetch_neuroquery_model, NeuroQueryModel

    if use_cognitive_atlas:
        url = "https://cognitiveatlas.org/api/v-alpha/concept"
        response = requests.get(url)

        if response.status_code != 200:
            raise RuntimeError(f"Cognitive Atlas API failed: {response.status_code}")

        df = pd.DataFrame(response.json())

        if "name" not in df.columns:
            raise ValueError("No 'name' column in Cognitive Atlas response")

        terms = df["name"].dropna().tolist()

        if verbose:
            print(f"Loaded {len(terms)} terms from Cognitive Atlas")

    if not terms:
        raise ValueError("No terms provided and Cognitive Atlas not enabled")
    
    os.makedirs(data_dir, exist_ok=True)

    if encoder is None:
        encoder = NeuroQueryModel.from_data_dir(fetch_neuroquery_model())

    saved_files = []
    failed_terms = []

    for term in terms:
        try:
            brain_map = encoder(term)["z_map"]

            safe_term = term.replace(" ", "_").replace("/", "_")
            path = os.path.join(data_dir, f"{safe_term}.nii.gz")

            nib.save(brain_map, path)
            saved_files.append(path)

            if verbose:
                print(f"Saved: {term}")

        except Exception as e:
            failed_terms.append((term, str(e)))

            if verbose:
                print(f"Failed: {term} → {e}")

    return saved_files, failed_terms, terms
