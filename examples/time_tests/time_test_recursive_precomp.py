import sys
import time

from examples.example2 import FeedbackQuery, FeedbackClause, generate_feedback_precompilation
from examples.time_tests.squirrel3 import squirrel3_boolean, squirrel3_0to1

MIN_QUERIES = 1
MAX_QUERIES = 1000
STEP = 1

WHICH_EVENT_SEED = 0
EVENT_LIKELYHOOD_SEED = 1


def get_query_recursive(number_queries):
    return {
        i: FeedbackQuery('atTime', i)
        for i in range(number_queries)
    }


def get_random_event_recursive(i):
    if squirrel3_boolean(i, WHICH_EVENT_SEED):
        return FeedbackClause('increase', i, squirrel3_0to1(i, EVENT_LIKELYHOOD_SEED))
    return FeedbackClause('decrease', i, squirrel3_0to1(i, EVENT_LIKELYHOOD_SEED))


def get_input_events_recursive(number_queries):
    return {
        i: [get_random_event_recursive(i)]
        for i in range(number_queries)
    }


def calculate_for_n_queries_recursive_precomp(filename, n):
    precomp = generate_feedback_precompilation(filename=filename)

    queries_dict = get_query_recursive(n)
    input_dict = get_input_events_recursive(n)

    res = {}
    feedback = None
    for i in range(n):
        query = queries_dict[i]
        inputs = input_dict[i]
        if feedback:
            inputs += feedback

        current_res = precomp.perform_queries(
            queries=[query],
            input_events=input_dict[i],
            use_feedback=True
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
        calculate_for_n_queries_recursive_precomp('../example2.pl', n_queries)
        end = time.time()

        print(
            '{},{}'.format(
                n_queries, end - start
            )
        )
