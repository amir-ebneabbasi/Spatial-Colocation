# This code is sourced from the original R implementation by František Váša and has been converted to Python.

def rotate_parcellation(coord_l, coord_r, nrot=1000, method="hungarian"):

    import numpy as np
    from scipy.optimize import linear_sum_assignment
    
    coord_l = np.array(coord_l, dtype=float)
    coord_r = np.array(coord_r, dtype=float)

    # Transpose coordinates to be of dimension nROI x 3 if provided as 3 x nROI
    if not (coord_l.shape[1] == 3 and coord_r.shape[1] == 3):
        if coord_l.shape[0] == 3 and coord_r.shape[0] == 3:
            print("transposing coordinates to be of dimension nROI x 3")
            coord_l = coord_l.T
            coord_r = coord_r.T

    nroi_l = coord_l.shape[0]
    nroi_r = coord_r.shape[0]
    nroi = nroi_l + nroi_r

    # Array to hold permutation IDs (1-based to match original output)
    perm_id = np.zeros((nroi, nrot), dtype=int)
    r = 0
    c = 0

    I1 = np.diag([1.0, 1.0, 1.0])
    I1[0, 0] = -1.0

    while r < nrot:
        # Uniform random orthogonal matrix generation
        A = np.random.normal(loc=0.0, scale=1.0, size=(3, 3))
        qrdec_q, qrdec_r = np.linalg.qr(A)

        TL = qrdec_q @ np.diag(np.sign(np.diag(qrdec_r)))
        if np.linalg.det(TL) < 0:
            TL[:, 0] = -TL[:, 0]

        TR = I1 @ TL @ I1
        coord_l_rot = coord_l @ TL
        coord_r_rot = coord_r @ TR

        # Compute Euclidean distance matrices
        dist_l = np.linalg.norm(
            coord_l[:, np.newaxis, :] - coord_l_rot[np.newaxis, :, :], axis=2
        )
        dist_r = np.linalg.norm(
            coord_r[:, np.newaxis, :] - coord_r_rot[np.newaxis, :, :], axis=2
        )

        if method == "vasa":
            # Vasa method assignment
            temp_dist_l = dist_l.copy().astype(float)
            rot_l, ref_l = [], []
            for _ in range(nroi_l):
                row_mins = np.nanmin(temp_dist_l, axis=1)
                ref_ix = np.where(row_mins == np.nanmax(row_mins))[0][0]
                rot_ix = np.where(
                    temp_dist_l[ref_ix, :]
                    == np.nanmin(temp_dist_l[ref_ix, :])
                )[0][0]

                ref_l.append(ref_ix)
                rot_l.append(rot_ix)

                temp_dist_l[:, rot_ix] = np.nan
                temp_dist_l[ref_ix, :] = 0.0

            temp_dist_r = dist_r.copy().astype(float)
            rot_r, ref_r = [], []
            for _ in range(nroi_r):
                row_mins = np.nanmin(temp_dist_r, axis=1)
                ref_ix = np.where(row_mins == np.nanmax(row_mins))[0][0]
                rot_ix = np.where(
                    temp_dist_r[ref_ix, :]
                    == np.nanmin(temp_dist_r[ref_ix, :])
                )[0][0]

                ref_r.append(ref_ix)
                rot_r.append(rot_ix)

                temp_dist_r[:, rot_ix] = np.nan
                temp_dist_r[ref_ix, :] = 0.0

            ref_l = np.array(ref_l)
            rot_l = np.array(rot_l)
            ref_r = np.array(ref_r)
            rot_r = np.array(rot_r)

        elif method == "hungarian":
            # Hungarian algorithm via scipy
            _, rot_l = linear_sum_assignment(dist_l)
            ref_l = np.arange(nroi_l)

            _, rot_r = linear_sum_assignment(dist_r)
            ref_r = np.arange(nroi_r)

        else:
            raise ValueError(
                f"'{method}' is not an accepted permutation method; valid options are 'vasa' or 'hungarian'"
            )

        # 0-indexed to 1-indexed conversion logic for output matching
        ref_lr = np.concatenate([ref_l, nroi_l + ref_r])
        rot_lr = np.concatenate([rot_l, nroi_l + rot_r])

        sort_idx = np.argsort(ref_lr)
        rot_lr_sort = rot_lr[sort_idx] + 1  # Convert to 1-based indexing

        if not np.array_equal(np.sort(rot_lr_sort), np.arange(1, nroi + 1)):
            raise RuntimeError("permutation error")

        if not np.array_equal(rot_lr_sort, np.arange(1, nroi + 1)):
            perm_id[:, r] = rot_lr_sort
            r += 1
        else:
            c += 1
            print(f"map to itself n. {c}")

        if r % 10 == 0:
            print(f"permutation {r} of {nrot}")

    return perm_id


# ==============================================================================
# How to run in Python
# ==============================================================================
# import pandas as pd

# Load coordinates
# data = pd.read_csv("path/to/HCP_sphere.csv", header=None).values

# Split data into left and right hemispheres (e.g., 180 per hemisphere)
# coord_l = data[:180, :]
# coord_r = data[180:360, :]

# Run permutation generator
# perm_id = rotate_parcellation(coord_l, coord_r, nrot=1000, method='hungarian')

# Save to CSV
# pd.DataFrame(perm_id).to_csv("path/to/output/HCP_hungarian.csv", index=False, header=False)
