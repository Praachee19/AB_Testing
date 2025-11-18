A/B Testing Project. Evaluating Landing Page Performance

This project explores whether a new landing page improves conversion rates compared to the existing design. Using a dataset of user interactions, the analysis follows a structured approach. Data cleaning, exploration, hypothesis testing and simulation of an improved conversion scenario. The objective is simple. Determine if the new page should replace the old one based on data driven evidence.

1. Understanding the Data

The dataset includes the following key variables.

user_id

group (control or treatment)

landing_page (old or new)

converted (1 or 0)

Initial checks confirm the data has no missing values. Duplicate users are removed to avoid bias. Group and page distribution indicate some mismatches which are expected in the raw Udacity dataset. These rows are retained only if they align with the correct group page mapping.

Conversion rates by group show the control group performs slightly better at baseline.

2. A/B Test. Old Page vs New Page

The hypothesis is tested using a two sided proportion z test.

Null hypothesis (H0)
There is no difference in conversion rates between the old and new page.

Alternative hypothesis (H1)
Conversion rates are different for the two pages.

Conversion rates before the test.

Control (old page): higher

Treatment (new page): lower

The z test returns:

A high p value

Insufficient evidence to reject the null hypothesis

This means the new page does not perform better than the old page. There is no statistical reason to roll it out.

3. Simulating a Scenario. Forcing 70 Percent Conversion in Treatment

To understand how the test behaves under a strong treatment uplift, the dataset is modified so that the treatment group converts at 70 percent.

Steps taken:

Copy the dataset

Calculate total treatment group users

Enforce 70 percent conversions by flipping zeroes to ones until the target is met

Re calculate conversion rates

Run the same z test again

The new treatment conversion rate becomes approximately 70 percent. A dramatic difference from the control group.

Results of the second z test show:

Very low p value

Strong evidence against the null hypothesis

Clear statistical significance

When the treatment group genuinely performs better, the test detects it immediately.

4. Final Interpretation

The original dataset shows:

The old page converts better

The new page does not provide benefit

The difference is not statistically significant

Rolling out the new page is not recommended

The simulated dataset shows:

When conversion truly improves, the statistical test picks up the change

The method is valid and sensitive

5. Conclusion

The A/B test results are clear.
The old page is performing better than the new page.
There is no statistical support for switching users to the new design.
Maintaining the current landing page is the correct decision.
