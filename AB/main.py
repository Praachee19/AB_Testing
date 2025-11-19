import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="A/B Testing Dashboard", layout="wide")

st.title("A/B Testing on Landing Page Performance")
st.write("This app evaluates whether the new landing page performs better than the old one by comparing conversion rates using a z test.")

# -------------------------------------------------------
# Required Format Display
# -------------------------------------------------------
st.header("1. Upload A/B Test Dataset")

st.subheader("Required CSV Format")

required_columns = ["user_id", "group", "landing_page", "converted"]
st.write("Your file must contain the following columns:")
st.code(required_columns)

sample_df = pd.DataFrame({
    "user_id": [111111, 111112, 111113, 111114],
    "group": ["control", "control", "treatment", "treatment"],
    "landing_page": ["old_page", "old_page", "new_page", "new_page"],
    "converted": [0, 1, 0, 1]
})

st.write("Sample valid data:")
st.dataframe(sample_df)

csv_template = sample_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV Template",
    data=csv_template,
    file_name="ab_test_template.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader("Upload ab_data.csv", type=["csv"])

if uploaded_file is None:
    st.stop()

# -------------------------------------------------------
# Load and Validate Data
# -------------------------------------------------------
data = pd.read_csv(uploaded_file)

st.subheader("Raw Data Preview")
st.dataframe(data.head())

missing_cols = [col for col in required_columns if col not in data.columns]
if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

# -------------------------------------------------------
# Data Cleaning
# -------------------------------------------------------
st.header("2. Data Cleaning")

initial_shape = data.shape
data = data.drop_duplicates(subset="user_id", keep=False)
final_shape = data.shape

st.write(f"Initial shape: {initial_shape}")
st.write(f"Shape after removing duplicate users: {final_shape}")

# -------------------------------------------------------
# Conversion Rates
# -------------------------------------------------------
st.header("3. Conversion Rates")

group_stats = data.groupby("group")["converted"].agg(["count", "sum"])
group_stats["conversion_rate"] = group_stats["sum"] / group_stats["count"]

st.subheader("Conversion Rate by Group")
st.dataframe(group_stats)

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=data["group"], y=data["converted"], ax=ax)
ax.set_title("Conversion Rate by Group")
st.pyplot(fig)

# -------------------------------------------------------
# Z Test
# -------------------------------------------------------
st.header("4. Z Test for Difference in Conversion Rates")

control = group_stats.loc["control"]
treatment = group_stats.loc["treatment"]

count = np.array([control["sum"], treatment["sum"]])
nobs = np.array([control["count"], treatment["count"]])

z_stat, p_value = sm.stats.proportions_ztest(count, nobs, alternative="two-sided")

st.write(f"Z statistic: {z_stat:.4f}")
st.write(f"P value: {p_value:.4f}")

alpha = 0.10

if p_value < alpha:
    st.success("Statistically significant difference at the 10 percent level. The groups behave differently.")
else:
    st.warning("No statistically significant difference. You cannot conclude the new page is better.")

# -------------------------------------------------------
# Simulation Block
# -------------------------------------------------------
st.header("5. Simulate 70 Percent Conversion for Treatment Group")

simulate = st.checkbox("Simulate treatment group with 70 percent conversion rate")

if simulate:
    simulated = data.copy()
    t_rows = simulated[simulated["group"] == "treatment"]
    
    total_t = t_rows.shape[0]
    target_conv = int(0.70 * total_t)

    current_conv = t_rows[t_rows["converted"] == 1].shape[0]
    to_flip = target_conv - current_conv

    if to_flip > 0:
        zero_indices = t_rows[t_rows["converted"] == 0].index
        flip_indices = np.random.choice(zero_indices, size=min(to_flip, len(zero_indices)), replace=False)
        simulated.loc[flip_indices, "converted"] = 1

    sim_group_stats = simulated.groupby("group")["converted"].agg(["count", "sum"])
    sim_group_stats["conversion_rate"] = sim_group_stats["sum"] / sim_group_stats["count"]

    st.subheader("Simulated Conversion Rates")
    st.dataframe(sim_group_stats)

    sim_count = np.array([sim_group_stats.loc["control"]["sum"],
                          sim_group_stats.loc["treatment"]["sum"]])
    
    sim_nobs = np.array([sim_group_stats.loc["control"]["count"],
                         sim_group_stats.loc["treatment"]["count"]])

    sim_z, sim_p = sm.stats.proportions_ztest(sim_count, sim_nobs, alternative="two-sided")

    st.write(f"Simulated Z statistic: {sim_z:.4f}")
    st.write(f"Simulated P value: {sim_p:.4f}")

    if sim_p < alpha:
        st.success("After applying 70 percent conversion, the difference becomes statistically significant.")
    else:
        st.warning("Even after forcing 70 percent conversion, significance is not reached.")

st.markdown("---")
st.write("End of A/B Testing Dashboard")

