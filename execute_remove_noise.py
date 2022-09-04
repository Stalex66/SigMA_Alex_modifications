from SigMA.SigMA import SigMA
from SigMA.velcoity_scale_factors import scale_samples
from miscellaneous.SessionManager import SessionManager
import time
import datetime
import numpy as np
import argparse
from NoiseRemoval.RemoveNoiseTransformed import remove_noise_sigma
from NoiseRemoval.ClusterSelection import nearest_neighbor_distribution
from execute_sigma import prepare_data
import re
import os
import copy
import pickle


def remove_noscocen(labels, isin_scocen, minsize=15):
    lcopy = copy.deepcopy(labels)
    for ul in np.unique(lcopy):
        if np.sum((lcopy == ul) & isin_scocen) < minsize:
            lcopy[lcopy == ul] = -1
    return lcopy


def get_parameters(fpath):
    beta, knn, nb_resampling = re.findall('scocen_extraction-beta_(.+)-knn_(.+)-nb_resampling_(.+)/', fpath)[0]
    return float(beta)/100, int(knn), int(nb_resampling)


def remove_noise(clusterer, data, labels):
    # Get radial velcity bounds
    rv = data.radial_velocity.values
    rv = rv[np.isfinite(rv)]
    rv_min, rv_max = np.percentile(rv, 1), np.percentile(rv, 99)
    # Labels shape
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
    # Timing
    delta_t = str(datetime.timedelta(seconds=time.time() - st)).split('.')[0]
    print(f'Done! [took {delta_t}]. Found {np.unique(clustering_res).size} clusters.')
    # ----- Return clustering restult -----
    return clustering_res, nearest_neighbors_arr, extra_infos


def main(data, cluster_features, dist_min, dist_max, isin_scocen):
    sm = SessionManager('sessions')
    sm.set_session_most_recent()
    beta, knn, nb_resampling = get_parameters(sm.session_dir)
    # Create clusterer object
    sigma_kwargs = dict(
        cluster_features=cluster_features,
        nb_resampling=0,
        max_knn_density=26,
        beta=beta,
        knn_initcluster_graph=knn
    )
    scale_factors = {
            'pos': {'features': ['v_a_lsr', 'v_d_lsr'], 'factor': scale_samples(dist_min, dist_max, 3)[1]}
    }
    clusterer = SigMA(
        data=data,
        scale_factors=scale_factors,
        **sigma_kwargs
    )
    clusterer.initialize_clustering(knn=25, saddle_point_candidate_threshold=40)
    clusterer.initialize_mode_neighbor_dict()
    # Get label files
    files = sm.files_in_session_dir()
    # Create new subdirectory
    now = datetime.datetime.now()
    sm.create_subdir('noise_removal_' + now.strftime("%Y-%m-%d-%H-%M-%S"))
    # Remove noise
    for fname in files:
        labels = np.load(fname)
        if isin_scocen is not None:
            labels = remove_noscocen(labels=labels, isin_scocen=isin_scocen)

        clustering_res, nearest_neighbors_arr, extra_infos = remove_noise(clusterer, data, labels)
        # Save reduced information
        fbase, fext = os.path.splitext(os.path.basename(fname))
        # Save result
        save_result = {
            'labels': clustering_res,
            'nearest_neighbors_arr': nearest_neighbors_arr,
            'extra_infos': extra_infos
        }
        # Pickle results
        with open(sm.get_fpath(fbase + '_noise_removed' + '.pickle'), 'wb') as handle:
            pickle.dump(save_result, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # nargs=?   ...0 or 1 arguments
    # const     ...if argument is provided but no value, e.g., program.py --beta, instead of, program.py --beta 0.99
    parser.add_argument("-f", "--data", type=str, help="Data path")
    parser.add_argument("-s", "--scocen", type=str, default='',
                        help="Sco-Cen data location")
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
    args = parser.parse_args()
    # Obtain data
    data, cluster_features = prepare_data(args.data)
    isin_scocen = None
    if os.path.isfile(args.scocen):
        isin_scocen = np.load(args.scocen)

    # Scale factors
    dist_min, dist_max = args.distance_min, args.distance_max
    dist_min_data = np.percentile(1000 / data.parallax, 5)
    dist_max_data = np.percentile(1000 / data.parallax, 95)
    if dist_min < dist_min_data:
        dist_min = dist_min_data
    if dist_max > dist_max_data:
        dist_max = dist_max_data

    main(data, cluster_features, dist_min, dist_max, isin_scocen)


