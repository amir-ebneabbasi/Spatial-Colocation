# Spatial Co-location Utilities

This repository provides a suite of Python tools for retrieving biologically informative brain maps, parcellating them, and linking them to neuroimaging phenotypes such as case–control differences or disease progression. It incorporates spatial permutation (spin test) to account for spatial autocorrelation.

## 📁 Functions Overview

### 1. `fetch_cyto_cortical_layers`

Downloads and processes BigBrain's cytoarchitectonic data.

**Features:**

* Downloads surface, parcellation, and layer profile data
* Computes ROI-wise mean and standard deviation
* Extracts cortical thickness across 6 layers
* Optionally saves results as CSV

### 2. `fetch_neuroquery_maps`

Generates meta-analytic brain maps using NeuroQuery for a list of terms.

**Features:**

* Fetches terms from Cognitive Atlas (optional)
* Uses pretrained NeuroQuery model
* Saves NIfTI maps for each term
* Logs failed terms

### 3. `fetch_neurotransmitter_maps`

Downloads PET-based neurotransmitter maps.

### 4. `parcellate_volumetric_maps`

Parcellates volumetric NIfTI maps into atlas-defined regions using `neuromaps`.

### 5. `spin_test`

Performs spatial permutation testing (spin test) to assess correlations between neuroimaging phenotypes and biological maps.

**Features:**

* Computes empirical Pearson correlations
* Generates null distributions via spin permutations
* Saves results (empirical, null and spin p-values)
