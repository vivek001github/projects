import streamlit as st

# Streamlit app layout
st.title("GST Calculator")

# Option to choose if the amount is including or excluding GST
gst_option = st.radio("Select an option:", ('Excluding GST', 'Including GST'))

# Slider for the total amount
amount = st.slider("Total amount", min_value=100, max_value=100000, value=5000, step=100)

# Dropdown for selecting GST rate
gst_rate = st.selectbox("Tax slab", (0.25, 1, 3, 5, 12, 18, 28))

# Calculating GST based on the selection
if gst_option == 'Excluding GST':
    gst_amount = (amount * gst_rate) / 100
    post_gst_amount = amount + gst_amount
else:
    gst_amount = amount - (amount * (100 / (100 + gst_rate)))
    post_gst_amount = amount

# Displaying the calculated GST and the total amount post-GST
st.write(f"**Total GST:** ₹{gst_amount:,.0f}")
st.write(f"**Post-GST amount:** ₹{post_gst_amount:,.0f}")
