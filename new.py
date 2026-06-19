import math
import streamlit as st
import pandas as pd
from functools import lru_cache
import timeit

st.title("Jellycat PriceSeer 🐰👑 ")

def set_up_and_down_rate(scarity):
    if scarity == 0:
        return 1.01, 0.99
    elif scarity == 1:
        return 1.03, 0.97
    else:
        return 1.05, 0.95

def compute_expected_value(start_price, up, down, days=7):
    @lru_cache(maxsize=None)
    def tree(days_left, up_count):
        if days_left == 0:
            return start_price * (up ** up_count) * (down ** (days - up_count))
        return 0.5 * tree(days_left - 1, up_count + 1) + \
               0.5 * tree(days_left - 1, up_count)
    result = tree(days, 0)
    tree.cache_clear()
    return result

def brute_force(start_price, up, down, days=7):
    def tree(days_left, up_count):
        if days_left == 0:
            return start_price * (up ** up_count) * (down ** (days - up_count))
        return 0.5 * tree(days_left - 1, up_count + 1) + \
               0.5 * tree(days_left - 1, up_count)
    return tree(days, 0)

original_price = st.number_input("Please input the original price: ")
size_input = int(st.selectbox("Please select the size(0 = small, 1 = medium, 2 = large): ", [0, 1, 2]))
scarcity_input = int(st.selectbox("Please select the scarcity(0 = common, 1 = Regional, 2 = Discontinued): ", [0, 1, 2]))
demand_input = int(st.slider("Please select the popularity level: ", min_value=0, max_value=2, value=1))
drop_and_new_input = 1 if st.selectbox("Is this a recently released, brand-new, unused item?: ", ["Yes", "No"]) == "Yes" else 0
promotion_input = 1 if st.selectbox("Please select the exposure level: ", [True, False]) else 0

if st.button("Start to predict the future price"):
    if original_price <= 0:
        st.error("Sorry, Price must be positive!")
    else:
        # calculate predicted price
        bonus = size_input + demand_input * 4 + drop_and_new_input * 3 + promotion_input * 2
        if scarcity_input == 0:
            final_predict_price = original_price * 0.8 + bonus
        elif scarcity_input == 1:
            final_predict_price = original_price * 0.9 + bonus
        else:
            final_predict_price = original_price + bonus

        if final_predict_price > original_price:
            st.success("Purchase Now 🔥!")
        else:
            st.write("Emm, maybe later 😭")
        st.write("Final predict price is: ", final_predict_price)

        # calculated the expected value
        up, down = set_up_and_down_rate(scarcity_input)
        expected_value = compute_expected_value(final_predict_price, up, down)

        st.write("---")
        st.subheader("Final Prediction 👑")
        st.metric(label="Predicted Price in 7 Days", value=f"${round(expected_value, 2)}")

        if expected_value > original_price * 1.05:
            st.success("🔥 Purchase Now!")
        elif expected_value < original_price * 0.95:
            st.error("🛑 Emm, maybe later!")
        else:
            st.warning("⚖️ Hold!")

        # efficiency test
        import time

        start = time.time()
        for _ in range(1000):
            brute_force(final_predict_price, up, down)
        time_brute = (time.time() - start) / 1000

        start = time.time()
        for _ in range(1000):
            compute_expected_value(final_predict_price, up, down)
        time_memo = (time.time() - start) / 1000

        improvement = (time_brute - time_memo) / time_brute * 100

        st.write("---")
        st.subheader("⚡ Performance Benchmark")
        col1, col2, col3 = st.columns(3)
        col1.metric("Brute Force (avg 1000x)", f"{time_brute*1000:.4f}ms")
        col2.metric("With Memoization (avg 1000x)", f"{time_memo*1000:.4f}ms")
        col3.metric("Speedup", f"{improvement:.1f}%")