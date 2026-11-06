# Conclusion

## Answer to the project question

**No. Neither estimator dominates the other under all conditions.** The Bayes estimator has the lower MSE in some regions of (p, n) and the MLE has the lower MSE in others. This matches the conclusion in Casella & Berger, Example 7.3.5, and our simulation confirms it quantitatively.

## What we found

**1. The simulation matches the theory.**
The simulated MSEs agree with the textbook's exact formulas. Over the 48 (p, n) pairs the largest relative error is 1.9% for the MLE and 0.9% for the Bayes estimator, and the mean error is about 0.4% and 0.3%. This is the size expected from Monte Carlo noise with M = 100,000. For each n, the Bayes MSE varies by less than 1.5% of its mean across the six values of p, so it is flat in p. The MLE's MSE follows the parabola p(1−p)/n. The textbook's Figure 7.3.1 is reproduced in our Figure A.

**2. The two estimators win in different places.**
The MLE is unbiased but its variance is largest at p = 0.5. The Bayes estimator shrinks toward 0.5. That shrinkage cuts the variance a lot when p is near 0.5, but it creates a bias that grows as p moves away from 0.5 (for example +0.163 at n = 4 and p = 0.01). Because the Bayes MSE is a constant and the MLE MSE is a parabola, the two curves cross at exactly two points, symmetric around 0.5:

$$p_\pm = \frac12 \pm \frac12\,\frac{\sqrt{2\sqrt n + 1}}{\sqrt n + 1}$$

The Bayes estimator wins for p between p₋ and p₊, and the MLE wins outside that interval. Our simulation agrees with this prediction in all 48 grid cells (0 mismatches).

| n | p₋ | p₊ | Width of Bayes-wins interval |
| --- | --- | --- | --- |
| 4 | 0.127 | 0.873 | 0.745 |
| 10 | 0.175 | 0.825 | 0.650 |
| 50 | 0.259 | 0.741 | 0.482 |
| 100 | 0.292 | 0.708 | 0.416 |
| 400 | 0.348 | 0.652 | 0.305 |
| 1000 | 0.377 | 0.623 | 0.246 |

**3. The size of the gain depends on where p is.**
- At p = 0.5 the ratio MSE(Bayes) / MSE(MLE) equals (√n / (√n + 1))². Bayes needs only 44% of the MLE's MSE at n = 4, but still 94% at n = 1000.
- Near the edges the MLE wins by a large factor. At p = 0.01 the Bayes MSE is 11 times the MLE's at n = 4 and 24 times at n = 1000.

So the Bayes estimator gains at most a factor of about 2.3 (at n = 4) and can lose by a factor of 20 or more. The advantage is bounded. The loss is not.

**4. Sample size matters.**
- **Small n (for example 4 to 10).** Bayes wins over most of the range of p. The MLE only wins when p is below about 0.13 to 0.18 (or above 0.82 to 0.87).
- **Large n.** The Bayes-wins interval narrows towards p = 0.5 (width 0.305 at n = 400, 0.140 at n = 10,000). It shrinks slowly, roughly like n^(−1/4). Even so, both MSEs fall like 1/n, so the practical difference between the two estimators becomes very small.

## Which estimator should you use?

This follows the textbook's guidance:

- If n is small and you have no strong belief that p is near 0 or 1, use the Bayes estimator.
- If n is large, or you have a strong belief that p is near 0 or 1, use the MLE. The exception is when you think p is very close to 0.5.

There is one sense in which the Bayes estimator is uniformly better. Its worst-case MSE over all p, n/(4(n+√n)²), is smaller than the MLE's worst-case MSE, 1/(4n), for every n. The ratio is (1 + 1/√n)², so the gap is a factor of 2.25 at n = 4 and 1.06 at n = 1000. This is the point of choosing α = β = √(n/4): it makes the risk constant, which is the best protection against the worst case. But it is a worst-case criterion, not a pointwise one, so it does not contradict the answer above.

## Limitations

- **Monte Carlo noise.** Each MSE is an estimate from M = 100,000 replications. Cells close to a crossover, such as p = 0.3 at n = 100 (ratio 0.986), are within noise of a tie, so the winner there is not reliable from the simulation alone. The exact formulas settle those cases.
- **Coarse grid.** The main grid has only six values of p and eight values of n. The dense p grid (used for Figure A) covers n = 4 and n = 400 only.
- **Only MSE.** MSE is one criterion among several. Other criteria, such as unbiasedness, loss functions other than squared error, or interval coverage, could rank the estimators differently.
- **The prior depends on n.** The Beta(√(n/4), √(n/4)) prior is chosen to make the MSE flat, so it changes with n. It is a device to equalise risk, not a belief about p that someone held before seeing the data.

## Possible extensions

- Compare with the Jeffreys prior Beta(1/2, 1/2) and the uniform prior Beta(1, 1), whose MSEs are not flat in p.
- Add confidence bands to the simulated MSEs to show the Monte Carlo error explicitly.
- Check the worst-case MSE of each estimator against n by simulation.
