from examples.time_tests.test_outputs_independent import check_consistent
from examples.time_tests.time_test_independent_end import calculate_for_n_queries_end
from examples.time_tests.time_test_recursive_iterative import calculate_for_n_queries_recursive_iter
from examples.time_tests.time_test_recursive_iterative_improved import calculate_for_n_queries_recursive_iter_improved
from examples.time_tests.time_test_recursive_precomp import get_input_events_recursive, \
    calculate_for_n_queries_recursive_precomp
from examples.time_tests.time_test_recursive_end import get_queries_recursive

TEST_WITH_N_QUERIES = 250


if __name__ == '__main__':
    end_res = calculate_for_n_queries_end(
        '../example2.pl',
        TEST_WITH_N_QUERIES,
        get_input_events=get_input_events_recursive,
        get_queries=get_queries_recursive
    )
    iter_res = calculate_for_n_queries_recursive_iter('../example2.pl', TEST_WITH_N_QUERIES)
    iter_imp_res = calculate_for_n_queries_recursive_iter_improved('../example2_iter_imp.pl', TEST_WITH_N_QUERIES)
    precomp_res = calculate_for_n_queries_recursive_precomp('../example2.pl', TEST_WITH_N_QUERIES)

    print("End vs Iter")
    check_consistent(end_res, iter_res)

    print("End vs Precomp")
    check_consistent(end_res, precomp_res)

    print("Iter vs Precomp")
    check_consistent(iter_res, precomp_res)

    print("Iter vs IterImp")
    check_consistent(iter_res, iter_imp_res)
