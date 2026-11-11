"""Aggregate model-audit calculations; never return held-out survey rows."""

import pandas as pd


MODELS = ('ML', 'DL', 'QML')


def summarize_prediction_rows(rows):
    labels = rows[[f'{name}_prediction' for name in MODELS]]
    truth = rows['LUNG_CANCER']
    unanimous = labels.nunique(axis=1) == 1
    errors = labels.ne(truth, axis=0)
    agreement = {
        'unanimous_count': int(unanimous.sum()),
        'disagreement_count': int((~unanimous).sum()),
        'any_model_wrong_count': int(errors.any(axis=1).sum()),
        'all_models_wrong_count': int(errors.all(axis=1).sum()),
        'pairwise_disagreement': {
            f'{left}_{right}': int((rows[f'{left}_prediction'] != rows[f'{right}_prediction']).sum())
            for left, right in (('ML', 'DL'), ('ML', 'QML'), ('DL', 'QML'))
        },
    }

    age_group = pd.Series(['under 60' if age < 60 else '60 or older' for age in rows['AGE']], index=rows.index)
    slices = []
    for dimension, values, groups in (
        ('Gender code', rows['GENDER'], ('F', 'M')),
        ('Age', age_group, ('under 60', '60 or older')),
    ):
        for group in groups:
            subset = rows.loc[values == group]
            count = len(subset)
            slices.append({
                'dimension': dimension, 'group': group, 'count': count,
                'NO': int((subset['LUNG_CANCER'] == 'NO').sum()),
                'YES': int((subset['LUNG_CANCER'] == 'YES').sum()),
                'accuracy': {
                    name: float((subset[f'{name}_prediction'] == subset['LUNG_CANCER']).mean()) if count else None
                    for name in MODELS
                },
            })
    return {'agreement': agreement, 'slices': slices}
