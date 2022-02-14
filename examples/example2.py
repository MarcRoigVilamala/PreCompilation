from problog.logic import Term, Constant

from preCompilation.PreCompilation import PreCompilationArguments, PreCompilation, Query, InputClause


class FeedbackClause(InputClause):
    def get_clause_format(self):
        return '{probability}::{identifier}({timestamp}).\n'

    def for_mock_model(self):
        return self.to_problog_with(probability=self.zero_probability())


class FeedbackQuery(Query):
    def get_query_format(self):
        return '\nquery({identifier}({timestamp})).'

    def update_result_timestamp(self, result, timestamp_difference):
        return Term(result.functor, Constant(result.args[0].functor + timestamp_difference))

    def generate_feedback(self, evaluation, timestamp_difference):
        return [
            FeedbackClause(
                identifier=clause.functor,
                timestamp=int(clause.args[0]) + timestamp_difference,
                probability=prob,
            )
            for clause, prob in evaluation.items()
        ]


def generate_feedback_precompilation(filename='example2.pl'):
    with open(filename, 'r') as f:
        problog_code = ''.join([l for l in f])

    input_clauses = [FeedbackClause('atTime', 0), FeedbackClause('increase', 1), FeedbackClause('decrease', 1)]

    queries = [
        FeedbackQuery('atTime', 1),
    ]

    precomp_args = PreCompilationArguments(
        input_clauses=input_clauses,
        queries=queries
    )

    return PreCompilation(precomp_args, problog_code)


if __name__ == '__main__':
    precomp = generate_feedback_precompilation()

    results = precomp.perform_queries(
        queries=[
            # Timestamp 0
            FeedbackQuery('atTime', 0),
            # Timestamp 1
            FeedbackQuery('atTime', 1),
            # Timestamp 2
            FeedbackQuery('atTime', 2),
            # Timestamp 3
            FeedbackQuery('atTime', 3),
            # Timestamp 4
            FeedbackQuery('atTime', 4),
        ],
        input_events=[
            # Timestamp 0
            FeedbackClause('increase', 0, 0.4),
            # Timestamp 1
            # Timestamp 2
            FeedbackClause('increase', 2, 0.2),
            # Timestamp 3
            FeedbackClause('decrease', 3, 0.5),
            # Timestamp 4
            FeedbackClause('increase', 4, 0.3),
            FeedbackClause('decrease', 4, 0.6),
        ],
        use_feedback=True
    )

    for k, v in results.items():
        print('{} -> {}'.format(k, v))

    print()

    results = precomp.perform_queries(
        queries=[
            # Timestamp 0
            FeedbackQuery('atTime', 0),
            # Timestamp 1
            FeedbackQuery('atTime', 1),
            # Timestamp 2
            FeedbackQuery('atTime', 2),
            # Timestamp 3
            FeedbackQuery('atTime', 3),
            # Timestamp 4
            FeedbackQuery('atTime', 4),
        ],
        input_events=[
            # Timestamp 0
            FeedbackClause('increase', 0, 0.4),
            # Timestamp 1
            # Timestamp 2
            FeedbackClause('increase', 2, 0.2),
            # Timestamp 3
            FeedbackClause('decrease', 3, 0.5),
            # Timestamp 4
            FeedbackClause('increase', 4, 0.3),
            FeedbackClause('decrease', 4, 0.6),
        ],
        use_feedback=False
    )

    for k, v in results.items():
        print('{} -> {}'.format(k, v))

    print()

    results = precomp.perform_queries(
        queries=[
            # Timestamp 0
            FeedbackQuery('atTime', 0),
            # Timestamp 1
            FeedbackQuery('atTime', 1),
            # Timestamp 2
            FeedbackQuery('atTime', 2),
        ],
        input_events=[
            # Timestamp 0
            # Timestamp 1
            FeedbackClause('increase', 1, 0.7),
            # Timestamp 2
            FeedbackClause('decrease', 2, 0.9),
        ],
        use_feedback=True
    )

    for k, v in results.items():
        print('{} -> {}'.format(k, v))

