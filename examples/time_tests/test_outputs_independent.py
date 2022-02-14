from examples.time_tests.time_test_independent_end import calculate_for_n_queries_end
from examples.time_tests.time_test_independent_iterative import calculate_for_n_queries_indep_iter
from examples.time_tests.time_test_independent_precomp import calculate_for_n_queries_indep_precomp

TEST_WITH_N_QUERIES = 500


def check_consistent(res1, res2):
    assert res1.keys() == res2.keys()

    max_difference = 0.0
    max_key = None
    for k in res1.keys():
        diff = abs(res1[k] - res2[k])
        if diff > max_difference:
            max_difference = diff
            max_key = k

    if max_key:
        print("The maximum difference is {} with the key {}".format(max_difference, max_key))
    else:
        print("All values are equal")


if __name__ == '__main__':
    end_res = calculate_for_n_queries_end('../example1.pl', TEST_WITH_N_QUERIES)
    iter_res = calculate_for_n_queries_indep_iter('../example1.pl', TEST_WITH_N_QUERIES)
    precomp_res = calculate_for_n_queries_indep_precomp(TEST_WITH_N_QUERIES)

    print("End vs Iter")
    check_consistent(end_res, iter_res)

    print("End vs Precomp")
    check_consistent(end_res, precomp_res)

    print("Iter vs Precomp")
    check_consistent(iter_res, precomp_res)
