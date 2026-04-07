import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import math
import os

def spin_test(spins_path, data_path, maps_path, output_dir, output_prefix):

    spins = pd.read_csv(spins_path)
    data = pd.read_csv(data_path)
    maps = pd.read_csv(maps_path)

    if data.columns[0] != 'ROI' or maps.columns[0] != 'ROI':
        raise ValueError("The first column of both 'data' and 'maps' must be named 'ROI'.")

    if data['ROI'].nunique() != maps['ROI'].nunique():
        raise ValueError("The number of unique 'ROI' must be the same in 'data' and 'maps'.")

    region_labels = maps.iloc[:, 0]
    data = pd.merge(data, region_labels, on=['ROI'], how='inner')

    data_rois = set(data['ROI'])
    maps_rois = set(maps['ROI'])

    only_in_maps = maps_rois - data_rois
    only_in_data = data_rois - maps_rois

    if only_in_maps or only_in_data:
        print("ROIs in 'maps' but not in 'data':", sorted(only_in_maps))
        print("ROIs in 'data' but not in 'maps':", sorted(only_in_data))
        raise ValueError("Mismatch found between 'ROI' columns of 'data' and 'maps'. See printed ROIs for details.")
    
    roi_number = data['ROI'].nunique() + 1
    print(f"number of rows in the 'ROI' column + 1 = {roi_number}")

    empirical_corrs = {}
    null_corrs = {}
    p_values = {}

    for feature in data.columns[1:]:
        for metric in [empirical_corrs, null_corrs, p_values]:
            metric[feature] = {map: [] for map in maps.columns[1:]}

        for map in maps.columns[1:]:
            empirical_corr = stats.pearsonr(data[feature], maps[map]).statistic
            empirical_corrs[feature][map] = empirical_corr

        for col in spins.columns[:1000]:
            permuted_indices = [x - 1 for x in spins[col] if x < roi_number]
            feature_spun = data.iloc[permuted_indices][feature]

            for map in maps.columns[1:]:
                null_corr = stats.pearsonr(feature_spun, maps[map]).statistic
                null_corrs[feature][map].append(null_corr)

        for map in maps.columns[1:]:
            observed = empirical_corrs[feature][map]
            null_distribution = null_corrs[feature][map]
            p_value = sum(abs(chance) >= abs(observed) for chance in null_distribution) / len(null_distribution)
            p_values[feature][map] = p_value

    with pd.ExcelWriter(output_dir + f'{output_prefix}_empirical.xlsx') as writer:
        for feature, emp_results in empirical_corrs.items():
            results_df = pd.DataFrame(emp_results, index=[0])
            results_df.to_excel(writer, sheet_name=feature, index=False)

    with pd.ExcelWriter(output_dir + f'{output_prefix}_spun.xlsx') as writer:
        for feature, null_results in null_corrs.items():
            results_df = pd.DataFrame(null_results)
            results_df.to_excel(writer, sheet_name=feature, index=False)

    with pd.ExcelWriter(output_dir + f'{output_prefix}_pvalues.xlsx') as writer:
        for feature, pval_results in p_values.items():
            results_df = pd.DataFrame(pval_results, index=[0])
            results_df.to_excel(writer, sheet_name=feature, index=False)

    print("Calculations completed and saved!")
