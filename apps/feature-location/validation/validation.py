from validation import mean_reciprocal_rank as MMR


def get_score(goldsets, results) -> int:
    return MMR.calculate(goldsets, results)
