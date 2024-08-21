import streamlit as st
from babel.numbers import format_currency, format_number
import matplotlib.pyplot as plt

def calculate_emi(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)
    emi = principal * monthly_rate * ((1 + monthly_rate) ** (tenure * 12)) / (((1 + monthly_rate) ** (tenure * 12)) - 1)
    return emi

def calculate_total_interest(principal, emi, tenure):
    total_payment = emi * tenure * 12
    total_interest = total_payment - principal
    return total_interest, total_payment

def format_currency_without_fraction(amount, currency_symbol='₹', locale='en_IN'):
    amount_int = int(amount)
    return f"{currency_symbol}{format_number(amount_int, locale=locale)}"

def plot_pie_chart(principal, total_interest):
    labels = ['Principal Amount', 'Interest Amount']
    sizes = [principal, total_interest]
    colors = ['#AED6F1', '#5DADE2']
    explode = (0.1, 0)  # Explode the 1st slice

    fig, ax = plt.subplots(figsize=(8, 8))  # Increase the size of the figure
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig

def main():
    st.title("EMI Calculator")

    # Create two columns: one for inputs and one for the pie chart
    col1, col2 = st.columns([3, 2])

    with col1:
        st.header("Enter Loan Details")

        # Sliders for user inputs
        principal = st.slider(
            "Loan Amount (₹)",
            min_value=100000,
            max_value=10000000,
            value=1000000,
            step=50000,
            format="₹%d"
        )
        st.write(f"Loan Amount: {format_currency_without_fraction(principal)}")

        rate = st.slider(
            "Rate of Interest (p.a.)",
            min_value=0.1,
            max_value=20.0,
            value=1.5,
            step=0.1,
            format="%1.1f%%"
        )
        st.write(f"Rate of Interest: {rate}%")

        tenure = st.slider(
            "Loan Tenure (Years)",
            min_value=1,
            max_value=30,
            value=4,
            step=1,
            format="%d years"
        )
        st.write(f"Loan Tenure: {tenure} years")

        # Calculate results
        emi = calculate_emi(principal, rate, tenure)
        total_interest, total_amount = calculate_total_interest(principal, emi, tenure)
        
        emi_formatted = format_currency_without_fraction(emi)
        principal_formatted = format_currency_without_fraction(principal)
        total_interest_formatted = format_currency_without_fraction(total_interest)
        total_amount_formatted = format_currency_without_fraction(total_amount)

        st.write("**EMI Calculator Results:**")
        st.write(f"Monthly EMI: {emi_formatted}")
        st.write(f"Principal Amount: {principal_formatted}")
        st.write(f"Total Interest: {total_interest_formatted}")
        st.write(f"Total Amount: {total_amount_formatted}")

    with col2:
        # Add some space before the chart
        st.write("### Pie Chart")
        st.markdown("<br><br>", unsafe_allow_html=True)  # Add vertical space
        
        # Plot and display pie chart
        fig = plot_pie_chart(principal, total_interest)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
