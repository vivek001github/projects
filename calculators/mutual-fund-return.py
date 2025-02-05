import streamlit as st
from babel.numbers import format_currency, format_number
import matplotlib.pyplot as plt

def calculate_returns(principal, rate_of_return, time_period):
    future_value = principal * ((1 + (rate_of_return / 100)) ** time_period)
    est_returns = future_value - principal
    return future_value, est_returns

def format_currency_without_fraction(amount, currency_symbol='₹', locale='en_IN'):
    amount_int = int(amount)
    return f"{currency_symbol}{format_number(amount_int, locale=locale)}"

def plot_pie_chart(total_investment, est_returns):
    labels = ['Invested Amount', 'Estimated Returns']
    sizes = [total_investment, est_returns]
    colors = ['#ADD8E6', '#4169E1']

    fig, ax = plt.subplots(figsize=(8, 8))  # Increase the size of the figure
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig

def main():
    st.title("Mutual Fund Return Calculator")

    # Create two columns: one for inputs and one for the pie chart
    col1, col2 = st.columns([3, 2])

    with col1:
        st.header("Enter Investment Details")

        # Sliders for user inputs
        total_investment = st.slider(
            "Total Investment (₹)",
            min_value=1000,
            max_value=1000000,
            value=25000,
            step=1000,
            format="₹%d"
        )
        st.write(f"Total Investment: {format_currency_without_fraction(total_investment)}")

        expected_return_rate = st.slider(
            "Expected Return Rate (p.a.)",
            min_value=0.0,
            max_value=15.0,
            value=5.4,
            step=0.1,
            format="%1.1f%%"
        )
        st.write(f"Expected Return Rate: {expected_return_rate}%")

        time_period = st.slider(
            "Time Period (Years)",
            min_value=1,
            max_value=30,
            value=6,
            format="%d years"
        )
        st.write(f"Time Period: {time_period} years")

        # Calculate results
        total_value, est_returns = calculate_returns(total_investment, expected_return_rate, time_period)

        total_value_formatted = format_currency_without_fraction(total_value)
        est_returns_formatted = format_currency_without_fraction(est_returns)

        st.write("**Investment Calculator Results:**")
        st.write(f"Invested Amount: {format_currency_without_fraction(total_investment)}")
        st.write(f"Estimated Returns: {est_returns_formatted}")
        st.write(f"Total Value: {total_value_formatted}")

    with col2:
        # Add some space before the chart
        st.write("### Pie Chart")
        st.markdown("<br><br>", unsafe_allow_html=True)  # Add vertical space
        
        # Plot and display pie chart
        fig = plot_pie_chart(total_investment, est_returns)
        st.pyplot(fig)

    # Button for investing
    st.button("INVEST NOW")

if __name__ == "__main__":
    main()
