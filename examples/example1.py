from problog.logic import Term, Constant

from preCompilation.PreCompilation import PreCompilationArguments, PreCompilation, Query, InputClause


class CoinInputClause(InputClause):
    def get_clause_format(self):
        return '{probability}::{identifier}({timestamp}).\n'

    def for_mock_model(self):
        return self.to_problog_with(probability=self.zero_probability())


class CoinQuery(Query):
    def get_query_format(self):
        return '\nquery({identifier}({timestamp})).'

    def update_result_timestamp(self, result, timestamp_difference):
        return Term(result.functor, Constant(result.args[0].functor + timestamp_difference))

    def generate_feedback(self, evaluation, timestamp_difference):
        # Not required since we are not using feedback
        pass


class OneArgumentQuery(Query):
    def __init__(self, identifier, timestamp, argument):
        super(OneArgumentQuery, self).__init__(identifier, timestamp)

        self.argument = argument

    @property
    def identifier(self):
        return '{}_{}'.format(
            super(OneArgumentQuery, self).identifier,
            self.argument
        )

    def get_query_format(self):
        return '\nquery({{identifier}}({{timestamp}}, {argument})).'.format(
            argument=self.argument
        )

    def update_result_timestamp(self, result, timestamp_difference):
        return Term(result.functor, Constant(result.args[0].functor + timestamp_difference), result.args[1])


DEFAULT_FILENAME = 'example1.pl'
DEFAULT_INPUT_CLAUSES = [CoinInputClause('heads1', 0), CoinInputClause('heads2', 0)]
DEFAULT_QUERIES = [
    CoinQuery('twoHeads', 0),
    CoinQuery('someHeads', 0),
    OneArgumentQuery('aHead', 0, 1),
    OneArgumentQuery('aHead', 0, 2),
]

QUERIES = [
    # Timestamp 0
    CoinQuery('twoHeads', 0),
    CoinQuery('someHeads', 0),
    OneArgumentQuery('aHead', 0, 1),
    OneArgumentQuery('aHead', 0, 2),
    # Timestamp 1
    CoinQuery('twoHeads', 1),
    CoinQuery('someHeads', 1),
    # Timestamp 2
    CoinQuery('twoHeads', 2),
    CoinQuery('someHeads', 2),
    # Timestamp 3
    CoinQuery('twoHeads', 3),
    CoinQuery('someHeads', 3),
    # Timestamp 4
    CoinQuery('twoHeads', 4),
    CoinQuery('someHeads', 4),
]

INPUT_EVENTS = [
    # Timestamp 0
    CoinInputClause('heads1', 0, 0.4),
    CoinInputClause('heads2', 0, 0.7),
    # Timestamp 1
    CoinInputClause('heads1', 1, 0.1),
    CoinInputClause('heads2', 1, 0.1),
    # Timestamp 2
    CoinInputClause('heads1', 2, 0.4),
    # Timestamp 3
    CoinInputClause('heads2', 3, 0.7),
    # Timestamp 4
]


def generate_precompilation(filename=DEFAULT_FILENAME, input_clauses=DEFAULT_INPUT_CLAUSES, queries=DEFAULT_QUERIES,
                            semiring=None):
    with open(filename, 'r') as f:
        problog_code = ''.join([l for l in f])

    precomp_args = PreCompilationArguments(
        input_clauses=input_clauses,
        queries=queries
    )

    return PreCompilation(precomp_args, problog_code, semiring=semiring)


if __name__ == '__main__':
    precomp = generate_precompilation()

    results = precomp.perform_queries(
        queries=QUERIES,
        input_events=INPUT_EVENTS,
    )

    for k, v in results.items():
        print('{} -> {}'.format(k, v))
