import sys
import time
from problog.program import PrologString
from problog import get_evaluatable
from examples.time_tests.time_test_independent_precomp import get_queries_indep, get_input_events_indep

MIN_QUERIES = 1
MAX_QUERIES = 250
STEP = 1


def join_list_of_lists_to_problog(from_list):
    return '\n'.join(
        [
            '\n'.join(
                [
                    i.to_problog()
                    for i in it_inp
                ]
            )
            for it_inp in from_list
        ]
    )


def calculate_for_n_queries_end(filename, n, get_input_events=get_input_events_indep, get_queries=get_queries_indep):
    with open(filename, 'r') as f:
        problog_code = ''.join([l for l in f])

    input_dict = get_input_events(n)
    queries_dict = get_queries(n)

    all_inputs = join_list_of_lists_to_problog(input_dict.values())
    all_queries = join_list_of_lists_to_problog(queries_dict.values())

    prolog_string = PrologString(
        '\n'.join([problog_code, all_inputs, all_queries])
    )

    res = get_evaluatable().create_from(prolog_string).evaluate()

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
        calculate_for_n_queries_end('../example1.pl', n_queries)
        end = time.time()

        print(
            '{},{}'.format(
                n_queries, end - start
            )
        )
