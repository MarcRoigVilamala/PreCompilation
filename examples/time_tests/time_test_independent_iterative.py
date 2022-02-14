import sys
import time
from problog.program import PrologString
from problog import get_evaluatable
from examples.time_tests.time_test_independent_precomp import get_queries_indep, get_input_events_indep

MIN_QUERIES = 1
MAX_QUERIES = 250
STEP = 1


def perform_queries_iterative(problog_code, queries, inputs):
    inputs_str = '\n'.join(map(lambda x: x.to_problog(), inputs))
    queries_str = '\n'.join(map(lambda x: x.to_problog(), queries))

    prolog_string = PrologString(
        '\n'.join([problog_code, inputs_str, queries_str])
    )

    return get_evaluatable().create_from(prolog_string).evaluate()


def calculate_for_n_queries_indep_iter(filename, n):
    with open(filename, 'r') as f:
        problog_code = ''.join([l for l in f])

    queries_dict = get_queries_indep(n)
    input_dict = get_input_events_indep(n)

    res = {}
    for i in range(n):
        res.update(
            perform_queries_iterative(
                problog_code,
                queries_dict[i],
                input_dict[i]
            )
        )

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
        calculate_for_n_queries_indep_iter('../example1.pl', n_queries)
        end = time.time()

        print(
            '{},{}'.format(
                n_queries, end - start
            )
        )
