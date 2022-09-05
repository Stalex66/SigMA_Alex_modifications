import time
import datetime
import math
import numpy as np
import pandas as pd
import argparse
import os
import pickle

from SigMA.SigMA import SigMA
from miscellaneous.SessionManager import SessionManager
from SigMA.velcoity_scale_factors import scale_samples
from NoiseRemoval.RemoveNoiseTransformed import remove_noise_sigma
from NoiseRemoval.ClusterSelection import nearest_neighbor_distribution


def filter_cluster(labels, isin_filter, minsize=15):
    for ul in np.unique(labels):
        if np.sum((labels == ul) & isin_filter) < minsize:
            labels[labels == ul] = -1
    return labels


def prepare_data(fname):
    # Extract data
    df = pd.read_csv(fname)
    # Define column names (following Gaia data guidelines)
    error_features = [
        'ra', 'dec', 'parallax', 'pmra', 'pmdec',
        'ra_error', 'dec_error', 'parallax_error', 'pmra_error', 'pmdec_error']
    # Correlations
    correlations_features = [
        'ra_dec_corr', 'ra_parallax_corr', 'ra_pmra_corr', 'ra_pmdec_corr',
        'dec_parallax_corr', 'dec_pmra_corr', 'dec_pmdec_corr',
        'parallax_pmra_corr', 'parallax_pmdec_corr', 'pmra_pmdec_corr'
    ]
    # Custer specific features
    cluster_features = ['X', 'Y', 'Z', 'v_a_lsr', 'v_d_lsr']
    # Additional features
    add_features = ['source_id', 'phot_bp_mean_mag', 'phot_rp_mean_mag', 'phot_g_mean_mag', 'cluster_age',
                    'radial_velocity', 'radial_velocity_error']
    # all columns together
    all_columns = error_features + correlations_features + cluster_features + add_features
    data = df[all_columns]
    data['g_rp'] = data['phot_g_mean_mag'] - data['phot_rp_mean_mag']
    data['mag_abs_g'] = data['phot_g_mean_mag'] + 5 * data['parallax'].apply(math.log10) - 10
    return data, cluster_features


def main(data, isin_file, cluster_features, alpha, beta, knn_init_graph, nb_resampling, knn_list, scale_factors_list):
    # Determine radial velocity bounds
    rv = data.radial_velocity.values
    rv = rv[np.isfinite(rv)]
    rv_min, rv_max = np.percentile(rv, 1), np.percentile(rv, 99)

    # first create session manager and session directory
    sm = SessionManager('sessions')
    sm.create_dir(f'extraction-beta_{int(beta * 100)}-knn_{knn_init_graph}-nb_resampling_{nb_resampling}')
    # Define SigMA kwargs
    sigma_kwargs = dict(
        cluster_features=cluster_features,
        nb_resampling=nb_resampling,
        max_knn_density=int(np.max(knn_list)+1),
        beta=beta,
        knn_initcluster_graph=knn_init_graph
    )
    # Create cluster solution
    for i, sf in enumerate(scale_factors_list):
        # Scaling factor
        scale_factors = {
            'pos': {'features': ['v_a_lsr', 'v_d_lsr'], 'factor': sf}
        }
        # Initializing sigma class for given scale factor
        clusterer = SigMA(
            data=data,
            scale_factors=scale_factors,
            **sigma_kwargs
        )
        # loop through family of smoothed density fields
        for j, knn in enumerate(knn_list):
            # -------- Clustering --------
            print(f'Clustering with {knn} nn density estimation...')
            st = time.time()
            labels = clusterer.fit(alpha=alpha, knn=knn, saddle_point_candidate_threshold=40)
            # --- remove unwanted clusters
            if isin_file is not None:
                labels = filter_cluster(labels=labels, isin_filter=isin_file)
            # --- timeing
            delta_t = str(datetime.timedelta(seconds=time.time() - st)).split('.')[0]
            print(f'Done! [took {delta_t}]')
            # ------- Removing noise ------
            print('Removing noise...')
            clustering_res = -np.ones(data.shape[0], dtype=np.int32)
            nearest_neighbors_arr = []
            extra_infos = {}
            st = time.time()
            z = 0
            for unique_id in np.unique(labels):
                # print(f'Removing noise from cluster {all_columns}')
                cluster_member_arr, contamination_completeness, rv_info, is_good_cluster = remove_noise_sigma(
                    data_full=data,
                    cluster_bool_arr=labels == unique_id,
                    te_obj=clusterer,
                    pos_cols=['X', 'Y', 'Z'],
                    nb_neigh_density=20,
                    rv_min=rv_min, rv_max=rv_max,
                    ra_col='ra', dec_col='dec', plx_col='parallax', pmra_col='pmra', pmdec_col='pmdec',
                    rv_col='radial_velocity', rv_err_col='radial_velocity_error', uvw_cols=None,  # ['u', 'v', 'w'],
                    adjacency_mtrx=clusterer.A,
                    radius=10,
                    min_cluster_size=15
                )
                if is_good_cluster and (np.sum(cluster_member_arr) > 15):
                    # Test if the distribution can be a cluster --> check for density in
                    nearest_neighbors_arr.append(nearest_neighbor_distribution(clusterer.X[cluster_member_arr], 7))
                    # Save clustering result
                    clustering_res[cluster_member_arr] = z
                    # store extra infos
                    extra_infos[z] = {
                        'contamination_completeness': contamination_completeness,
                        'rv_info': rv_info
                    }
                    # Increment counter
                    z += 1
            print(f'Done! [took {time.time() - st:.2f}sec]. Found {np.unique(clustering_res).size} clusters.')
            # ----- Save clustering -----
            save_result = {
                'labels': clustering_res,
                'nearest_neighbors_arr': nearest_neighbors_arr,
                'extra_infos': extra_infos
            }
            with open(sm.get_fpath(f'labels-knn_{knn}-scalef_{sf:.3f}.pickle'), 'wb') as handle:
                pickle.dump(save_result, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # nargs=?   ...0 or 1 arguments
    # const     ...if argument is provided but no value, e.g., program.py --beta, instead of, program.py --beta 0.99
    parser.add_argument("-i", "--data", type=str, help="Data path/input")
    parser.add_argument(
        "-b", "--beta",
        type=float, nargs='?', const=0.99, default=0.99,
        help="beta parameter in beta skeleton"
    )
    parser.add_argument(
        "-g", "--graph_knn",
        type=int, nargs='?', const=40, default=40,
        help="Maximal number of neighbors in initial beta skeleton graph"
    )
    parser.add_argument(
        "-n", "--nb_resampling",
        type=int, nargs='?', const=30, default=30,
        help="Number of resampled data sets (for modality test)"
    )
    parser.add_argument(
        "-a", "--alpha",
        type=float, nargs='?', const=0.05, default=0.05,
        help="Significance level alpha"
    )
    parser.add_argument(
        '-k0', '--knn_min',
        type=int, nargs='?', const=18, default=18,
        help="Minimum k in nearest neighbor density estimator"
    )
    parser.add_argument(
        '-k1', '--knn_max',
        type=int, nargs='?', const=35, default=35,
        help="Maximum k in nearest neighbor density estimator"
    )
    parser.add_argument(
        '-kd', '--knn_delta',
        type=int, nargs='?', const=2, default=2,
        help="Scale space step size of k in nearest neighbor density estimator"
    )
    parser.add_argument(
        '-d0', '--distance_min',
        type=float, nargs='?', const=-1.0, default=-1.0,
        help="Minimum distance for scale factor determination"
    )
    parser.add_argument(
        '-d1', '--distance_max',
        type=float, nargs='?', const=-1.0, default=-1.0,
        help="Maximum distance for scale factor determination"
    )
    parser.add_argument(
        '-dd', '--distance_samples',
        type=int, nargs='?', const=10, default=10,
        help="Number of scale factors to draw."
    )
    parser.add_argument("-f", "--filter", type=str, default='',
                        help="Boolean mask focussing on specific data entries to cluster")

    args = parser.parse_args()
    # Obtain data
    data, cluster_features = prepare_data(args.data)
    isin_file = None
    if os.path.isfile(args.filter):
        isin_file = np.load(args.filter)

    # Steps in scale space (knn density estimation)
    knn_list = np.arange(args.knn_min, args.knn_max + args.knn_delta, args.knn_delta)
    # Scale factors
    dist_min, dist_max, dist_samples = args.distance_min, args.distance_max, args.distance_samples
    dist_min_data = np.percentile(1000 / data.parallax, 5)
    dist_max_data = np.percentile(1000 / data.parallax, 95)
    if dist_min < dist_min_data:
        dist_min = dist_min_data
    if dist_max > dist_max_data:
        dist_max = dist_max_data
    # Get scale factors
    scale_factors_list = scale_samples(min_dist=dist_min, max_dist=dist_max, n_samples=dist_samples)

    # Execute main
    main(data=data,
         isin_file=isin_file,
         cluster_features=cluster_features,
         alpha=args.alpha,
         beta=args.beta,
         knn_init_graph=args.graph_knn,
         nb_resampling=args.nb_resampling,
         knn_list=knn_list,
         scale_factors_list=scale_factors_list
         )

