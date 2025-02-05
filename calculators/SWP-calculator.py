import streamlit as st
from babel.numbers import format_currency, format_number

def calculate_swp(total_investment, withdrawal_per_month, return_rate, time_period):
    monthly_rate = return_rate / 12 / 100
    total_withdrawal = 0
    current_value = total_investment
    
    for month in range(int(time_period * 12)):
        current_value += current_value * monthly_rate
        current_value -= withdrawal_per_month
        total_withdrawal += withdrawal_per_month
        
        if current_value <= 0:
            break

    return current_value, total_withdrawal

def format_currency_without_fraction(amount, currency_symbol='₹', locale='en_IN'):
    amount_int = int(amount)
    return f"{currency_symbol}{format_number(amount_int, locale=locale)}"

def main():
    st.title("SWP (Systematic Withdrawal Plan) Calculator")

    # Create a single column for inputs and results
    st.header("Enter Investment Details")

    # Full-width sliders
    total_investment = st.slider(
        "Total Investment (₹)",
        min_value=10000,
        max_value=1000000,
        value=120000,
        step=1000,
        format="₹%d",
        help="Total amount of investment"
    )
    withdrawal_per_month = st.slider(
        "Withdrawal per Month (₹)",
        min_value=1000,
        max_value=50000,
        value=2500,
        step=500,
        format="₹%d",
        help="Monthly withdrawal amount"
    )
    return_rate = st.slider(
        "Expected Return Rate (p.a.)",
        min_value=0.0,
        max_value=15.0,
        value=2.3,
        step=0.1,
        format="%1.1f%%",
        help="Annual return rate on the investment"
    )
    time_period = st.slider(
        "Time Period (Years)",
        min_value=1,
        max_value=30,
        value=2,
        format="%d years",
        help="Duration of the investment"
    )

    # Calculate SWP
    final_value, total_withdrawal = calculate_swp(total_investment, withdrawal_per_month, return_rate, time_period)
    
    # Display results
    final_value_formatted = format_currency_without_fraction(final_value)
    total_withdrawal_formatted = format_currency_without_fraction(total_withdrawal)
    
    st.write(f"### Total Investment: {format_currency_without_fraction(total_investment)}")
    st.write(f"### Total Withdrawal: {total_withdrawal_formatted}")
    st.write(f"### Final Value: {final_value_formatted}")

    if final_value <= 0:
        st.write("### Warning: Your investment may be exhausted before the end of the time period.")

if __name__ == "__main__":
    main()
