def make_plan(query: str, candidates: list[dict]) -> list[str]:
    return [
      'Identify relevant document classes and time/topic constraints',
      f'Inspect {len(candidates)} high-relevance evidence candidates in bounded batches',
      'Extract recurring facts/root causes and contradictions',
      'Aggregate only evidence-supported findings',
      'Validate citations and access policy before final response'
    ]
