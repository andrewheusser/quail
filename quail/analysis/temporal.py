import numpy as np

# temporal clustering analysis
def temporal_helper(pres_slice, rec_slice, permute=False, n_perms=1000):
    """
    Computes temporal clustering score

    Parameters
    ----------
    pres_slice : Pandas Dataframe
        chunk of presentation data to be analyzed
    rec_slice : Pandas Dataframe
        chunk of recall data to be analyzed

    Returns
    ----------
    score : float
        a number representing temporal clustering

    """

    # initialize temporal clustering list
    temporal_clustering = []

    # define distance function for temporal clustering
    dist_funcs = {
        'temporal' : 'lambda a, b : np.abs(a-b)'
    }

    # define features (just positions for temporal clustering)
    f = [{'temporal' : i} for i in range(pres_slice.list_length+1)]

    # loop over lists
    for p, r in zip(pres_slice.as_matrix(), rec_slice.as_matrix()):

        # turn arrays into lists
        p = list(p)
        r = list([ri for ri in list(r) if isinstance(ri, str)])

        if len(r)>1:

            # compute distances
            distances = compute_distances(p, f, dist_funcs, dist_funcs_dict)

            # add optional bootstrapping
            if permute:
                temporal_clustering.append(permute_fingerprint_serial(p, r, f, distances, n_perms=n_perms))
            else:
                temporal_clustering.append(compute_feature_weights(p, r, f, distances))
        else:
            temporal_clustering.append([np.nan]*len(list(f[0].keys())))

    # return average over rows
    return np.nanmean(temporal_clustering, axis=0)