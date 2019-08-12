from problog.logic import Term, Constant

from preCompilation.PreCompilation import PreCompilationArguments, PreCompilation, Query, InputClause


class CoinInputClause(InputClause):
    def get_clause_format(self):
        return '{probability}::{identifier}({timestamp}).\n'

    def for_mock_model(self):
        return self.to_problog_with(probability=0.0)


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


if __name__ == '__main__':
    problog_code = '''
        twoHeads(T) :- heads1(T), heads2(T).
        
        someHeads(T) :- heads1(T).
        someHeads(T) :- heads2(T).
        
        aHead(T, 1) :- heads1(T), \\+heads2(T).
        aHead(T, 2) :- heads2(T), \\+heads1(T).
    '''

    input_clauses = [CoinInputClause('heads1', 0), CoinInputClause('heads2', 0)]

    queries = [
        CoinQuery('twoHeads', 0),
        CoinQuery('someHeads', 0),
        OneArgumentQuery('aHead', 0, 1),
        OneArgumentQuery('aHead', 0, 2),
    ]

    precomp_args = PreCompilationArguments(
        input_clauses=input_clauses,
        queries=queries
    )

    precomp = PreCompilation(precomp_args, problog_code)

    results = precomp.perform_queries(
        queries=[
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
        ],
        input_events=[
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
        ],
    )

    for k, v in results.items():
        print('{} -> {}'.format(k, v))
