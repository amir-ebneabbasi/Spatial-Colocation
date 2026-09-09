# Spatial Co-location Utilities

This repository provides a suite of Python tools for retrieving biologically informative brain maps, parcellating them, and linking them to neuroimaging phenotypes such as case–control differences or disease progression. It incorporates spatial permutation (spin test) to account for spatial autocorrelation.

## 📁 Functions Overview

### 1. `fetch_cyto_cortical_layers`

Downloads and processes BigBrain's cytoarchitectonic data.

**Features:**

* Downloads surface, parcellation, and layer profile data
* Computes ROI-wise mean and standard deviation
* Extracts cortical thickness across 6 layers

### 2. `fetch_neuroquery_maps`

Generates meta-analytic brain maps using NeuroQuery for a list of terms.

**Features:**

* Fetches terms from Cognitive Atlas (optional)
* Uses pretrained NeuroQuery model
* Saves NIfTI maps for each term
* Logs failed terms

### 3. `fetch_neurotransmitter_maps`

Retrieves PET receptor‑density volumes from Hansen et al. 2022 for downstream parcellation via `parcellate_volumetric_maps`.

### 4. `fetch_enigma`

Loads all ENIGMA cortical summary‑statistics CSVs across disorders, age groups, and subgroup contrasts.

### 5. `parcellate_volumetric_maps`

Parcellates volumetric NIfTI maps into atlas-defined regions using `neuromaps`.

### 6. `generate_spins`

Generates spatially constrained null permutations of cortical parcels using their spherical coordinates. It independently rotates the left and right hemispheres while preserving hemispheric symmetry, then reassigns rotated parcels to the original parcels using either the `Hungarian` algorithm or the `Vasa` method.

### 7. `spin_test`

Performs spatial permutation testing (spin test) to assess correlations between neuroimaging phenotypes and biological maps.

**Features:**

* Computes empirical Pearson correlations
* Generates null distributions via spin permutations
* Saves results (empirical, null and spin p-values)
