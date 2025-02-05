import streamlit as st
from babel.numbers import format_currency, format_number
import matplotlib.pyplot as plt

def calculate_sip(monthly_investment, annual_return_rate, years):
    monthly_return_rate = annual_return_rate / 12 / 100
    num_months = years * 12
    future_value = 0
    
    for _ in range(num_months):
        future_value = (future_value + monthly_investment) * (1 + monthly_return_rate)

    total_invested = monthly_investment * num_months
    estimated_returns = future_value - total_invested

    return total_invested, estimated_returns, future_value

def format_currency_without_fraction(amount, currency_symbol='₹', locale='en_IN'):
    amount_int = int(amount)
    return f"{currency_symbol}{format_number(amount_int, locale=locale)}"

def plot_pie_chart(total_invested, estimated_returns):
    labels = ['Total Invested', 'Estimated Returns']
    sizes = [total_invested, estimated_returns]
    colors = ['#ff9999', '#66b3ff']

    fig, ax = plt.subplots(figsize=(8, 8))  # Increase the size of the figure
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig

def main():
    st.title("SIP Calculator")

    # Create two columns: one for inputs and one for the pie chart
    col1, col2 = st.columns([3, 2])

    with col1:
        st.header("Enter Investment Details")

        # Sliders for user inputs
        monthly_investment = st.slider(
            "SIP Amount (₹)",
            min_value=500,
            max_value=100000,
            value=5000,
            format="₹%d"
        )
        st.write(f"Monthly Investment: {format_currency_without_fraction(monthly_investment)}")

        annual_return_rate = st.slider(
            "Annual Return Rate (%)",
            min_value=1,
            max_value=30,
            value=12,
            format="%d%%"
        )
        st.write(f"Annual Return Rate: {annual_return_rate}%")

        years = st.slider(
            "Investment Period (Years)",
            min_value=1,
            max_value=50,
            value=10,
            format="%d years"
        )
        st.write(f"Investment Period: {years} years")

        # Calculate results
        total_invested, estimated_returns, future_value = calculate_sip(monthly_investment, annual_return_rate, years)
        
        total_invested_formatted = format_currency_without_fraction(total_invested)
        estimated_returns_formatted = format_currency_without_fraction(estimated_returns)
        future_value_formatted = format_currency_without_fraction(future_value)

        st.write("**SIP Calculator Results:**")
        st.write(f"Total Invested Amount: {total_invested_formatted}")
        st.write(f"Estimated Returns: {estimated_returns_formatted}")
        st.write(f"Total Value: {future_value_formatted}")

    with col2:
        # Add some space before the chart
        st.write("### Pie Chart")
        st.markdown("<br><br>", unsafe_allow_html=True)  # Add vertical space
        
        # Plot and display pie chart
        fig = plot_pie_chart(total_invested, estimated_returns)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
