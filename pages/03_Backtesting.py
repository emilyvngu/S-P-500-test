import streamlit as st

def main():
    st.title("Constrained Minimum Variance Portfolio")

    st.header("1. Install Packages")
    with st.expander("Expand"):
        st.code("""
using Pkg
Pkg.add("JuMP")
Pkg.add("COSMO")
Pkg.add("MosekTools")
Pkg.add("Plots")
Pkg.add("CSV")
Pkg.add("DataFrames")
        """, language="julia")

    # --- Section 2: Import Libraries ---
    st.header("2. Import Libraries")
    st.code("""
using LinearAlgebra, JuMP, COSMO, MosekTools, Plots, CSV, DataFrames, Statistics
    """, language="julia")

    # --- Section 3: Load Data ---
    st.header("3. Load Data")
    st.markdown("Here we read in CSV files for mean returns, covariance, and time windows.")
    st.code('''
mean_list_df = CSV.read("/Users/emilynguyen/Desktop/mean_list.csv", DataFrame)
covariance_list = CSV.read("/Users/emilynguyen/Desktop/covariance_list.csv", DataFrame)
mean_list = [collect(row) for row in eachrow(mean_list_df)]

n_assets = size(mean_list_df, 2)
println("Number of assets: ", n_assets)

Ω_list = [reshape(collect(row), n_assets, n_assets) for row in eachrow(covariance_list)]
time_windows = CSV.read("/Users/emilynguyen/Desktop/time_windows.csv", DataFrame)[:, 1]
    ''', language="julia")

    # --- Section 4: Annualize Returns ---
    st.header("4. Annualize Returns & Covariance")
    st.markdown("""
    Each row in `mean_list` is a **monthly** log return, so we do:
    - `mean_list = exp.(m .* 12) .- 1` for log returns
    - `Ω_list = c .* 12` for covariance
    """)
    st.code('''
mean_list = [(exp.(m .*= 12) .- 1) for m in mean_list]
Ω_list = [c .*= 12 for c in Ω_list]
    ''', language="julia")

    # --- Section 5: Initialize Variables ---
    st.header("5. Initialize Portfolio")
    st.code('''
initial_investment = 1000.0
cumulative_wealth = [initial_investment]
current_weights = fill(1.0 / n_assets, n_assets)  # Equal weights
μ_target = 0.015
total_weight = 1.0
    ''', language="julia")

    # --- Section 6: Optimization Function ---
    st.header("6. Define the Optimization Model")
    st.code('''
function optimize_portfolio(μ, Ω, n_assets, μ_target, total_weight)
    model = Model(COSMO.Optimizer)
    @variable(model, w[1:n_assets] >= 0)
    @constraint(model, sum(w) == total_weight)
    @constraint(model, dot(w, μ) >= μ_target)
    @objective(model, Min, dot(w, Ω * w))

    optimize!(model)

    if termination_status(model) == MOI.OPTIMAL
        return value.(w)
    else
        error("Optimization failed")
    end
end
    ''', language="julia")

    # --- Section 7: Loop Over Windows ---
    st.header("7. Rolling Optimization & Wealth Calculation")
    st.code('''
for t in 1:(length(mean_list) - 1)
    try
        μ = mean_list[t]
        Ω = Ω_list[t]
        new_weights = optimize_portfolio(μ, Ω, n_assets, μ_target, total_weight)

        # Next window returns
        next_window_returns = mean_list[t + 1]
        portfolio_return = dot(new_weights, next_window_returns)

        # Update wealth
        new_wealth = cumulative_wealth[end] * exp(portfolio_return)
        push!(cumulative_wealth, new_wealth)

        current_weights = new_weights
    catch e
        println("Optimization failed at window $t: $e")
    end
end
    ''', language="julia")

    # --- Section 8: Plot ---
    st.header("8. Plot Results")
    st.code('''
plot(cumulative_wealth, 
     xlabel="Time", 
     ylabel="Cumulative Wealth", 
     title="Portfolio Wealth Over Time")
    ''', language="julia")

    

if __name__ == "__main__":
    main()
