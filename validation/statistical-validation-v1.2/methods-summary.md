# Statistical Validation v1.2 Methods Summary

v1.2 adds two conservative checks on top of the wave-005 descriptive validation layer:

- fixed-family multiple-comparison correction across shared perturbation axes;
- one deterministic conventional stylometry baseline based on character n-gram cosine distance.

The correction family uses Euclidean distance as the primary metric for six shared benchmark/campaign axes.
Both Holm-Bonferroni and Benjamini-Hochberg adjusted values are reported.

No claim wording is upgraded by this layer.
