import sys
import time

from examples.example2 import FeedbackQuery
from examples.time_tests.time_test_independent_iterative import perform_queries_iterative
from examples.time_tests.time_test_recursive_precomp import get_query_recursive, get_input_events_recursive

MIN_QUERIES = 1
MAX_QUERIES = 100
STEP = 1


def calculate_for_n_queries_recursive_iter(filename, n):
    with open(filename, 'r') as f:
        problog_code = ''.join([l for l in f])

    queries_dict = get_query_recursive(n)
    input_dict = get_input_events_recursive(n)

    res = {}
    feedback = None
    for i in range(n):
        query = queries_dict[i]
        inputs = input_dict[i]
        if feedback:
            inputs += feedback

        current_res = perform_queries_iterative(
            problog_code, [query], inputs
        )

        feedback = query.generate_feedback(current_res, 0)

        res.update(current_res)

    return res


if __name__ == '__main__':
    if len(sys.argv) == 2:
        max_queries = int(sys.argv[1])
    elif len(sys.argv) == 1:
        max_queries = MAX_QUERIES
    else:
        raise Exception("Unexptected number of command line arguments")

    for n_queries in range(MIN_QUERIES, max_queries, STEP):
        start = time.time()
        calculate_for_n_queries_recursive_iter('../example2.pl', n_queries)
        end = time.time()

        print(
            '{},{}'.format(
                n_queries, end - start
            )
        )
