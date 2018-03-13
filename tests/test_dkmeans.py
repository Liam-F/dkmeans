#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 19:52:34 2017

@author: bbradt
"""

import numpy as np
import dkmeans.remote_computations as remote
import dkmeans.local_computations as local


DEFAULT_PARAMS = (2,   # m
                  2,   # n
                  2,   # k
                  3,   # s
                  11,  # N
                  )


def _k_cluster_labels(N, k):
    C = []
    for ki in range(k):
        C.extend([ki for i in range(int(N/k))])
    while len(C) < N:
        C.append(k - 1)
    return C


def test_remote_aggregate_clusters():
    m, n, k, s, _ = DEFAULT_PARAMS
    centroids = [[np.ones([m, n]) for ki in range(k)] for si in range(s)]
    expected = [np.ones([m, n]) for ki in range(k)]
    actual = remote.aggregate_clusters(centroids)
    assert all([np.array_equal(a, e) for a, e in zip(expected, actual)])

def test_remote_aggregate_sum():
    objects = [[np.array([0]), np.array([1])],
               [np.array([1]), np.array([0])]
               ]
    expected = [np.array([1]), np.array([1])]
    actual = remote.aggregate_sum(objects)
    np.testing.assert_array_equal(expected, actual)

def test_remote_closest_centroids():
    m, n, k, s, _ = DEFAULT_PARAMS
    centroids = [[np.ones([m, n])
                 for ki in range(k)] for si in range(s)]
    actual = remote.closest_centroids(centroids)
    expected = [(i, i+1) for i in range(0, k*s-1, 2)]
    if k*s % 2 != 0:
        expected.append((k*s-1, k*s-1))
    assert actual == expected


"""
def test_local_compute_mean():
    m, n, k, s, N = DEFAULT_PARAMS
    X = [np.ones([m, n]) for Ni in range(N)]
    C = _k_cluster_labels(N, k)
    expected = [np.ones([m, n]) for ki in range(k)]
    actual = local.compute_mean(X, C, k)
    np.testing.assert_array_equal(expected, actual)

def test_local_mean_step():
    m, n, k, s, N = DEFAULT_PARAMS
    C = _k_cluster_labels(N, k)
    X = [np.ones([m, n]) for Ni in range(N)]
    centroids = [[np.ones([m, n]) for ki in range(k)] for si in range(s)]
    local_means = local.compute_mean(X, C, k)
    expected = ([lmean for lmean in local_means], centroids)
    actual = local.mean_step(local_means, centroids)
    assert all([np.array_equal(a, e) for a, e in zip(expected, actual)]))

def test_local_compute_clustering():
    m, n, k, s, N = DEFAULT_PARAMS
    C = _k_cluster_labels(N, k)
    X = [np.ones([m, n])*C[Ni] for Ni in range(N)]
    centroids = [np.ones([m, n]) * ki for ki in range(k)]
    expected = (C, X)
    actual = local.compute_clustering(X, centroids)
    assert all([np.array_equal(a, e) for a, e in zip(expected, actual)]))
"""
