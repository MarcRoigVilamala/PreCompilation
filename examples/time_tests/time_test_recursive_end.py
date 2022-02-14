import sys
import time

from examples.time_tests.time_test_independent_end import calculate_for_n_queries_end
from examples.time_tests.time_test_recursive_precomp import get_input_events_recursive, get_query_recursive

MIN_QUERIES = 1
MAX_QUERIES = 250
STEP = 1


def get_queries_recursive(number_queries):
    return {
        i: [q]
        for i, q in get_query_recursive(number_queries).items()
    }


if __name__ == '__main__':
    if len(sys.argv) == 2:
        max_queries = int(sys.argv[1])
    elif len(sys.argv) == 1:
        max_queries = MAX_QUERIES
    else:
        raise Exception("Unexptected number of command line arguments")

    for n_queries in range(MIN_QUERIES, max_queries, STEP):
        start = time.time()
        calculate_for_n_queries_end(
            '../example2.pl',
            n_queries,
            get_input_events=get_input_events_recursive,
            get_queries=get_queries_recursive
        )
        end = time.time()

        print(
            '{},{}'.format(
                n_queries, end - start
            )
        )
