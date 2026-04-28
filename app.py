import streamlit as st
st.title("PriceSeer 👑 ")

#input the original price
original_price = st.number_input("Please input the original price: ")

#select the size
size_input = st.selectbox("Please select the size(0 = small, 1 = medium, 2 = large): ",[0, 1, 2])

#select the Scarcity
scarcity_input = st.selectbox("Please select the scarcity(0 = common, 1 = Regional, 2 = Discontinued): ", [0,1,2])

#select the demand of this product
demand_input = st.slider("Please select the popularity level: ",min_value= 0,max_value= 2,value= 1)

#select the situation of product(drop&new)
drop_and_new_input = st.selectbox("Is this a recently released, brand-new, unused item?: ",["Yes","No"])

#select the exposure level on social media
promotion_input = st.selectbox("Please select the exposure level: ",[True,False])


if promotion_input == True:
    promotion_input = 1
else:
    promotion_input = 0

if drop_and_new_input == "Yes":
    drop_and_new_input = 1
else:
    drop_and_new_input = 0

#change the type of data
size_input = int(size_input)
demand_input = int(demand_input)
drop_and_new_input = int(drop_and_new_input)
promotion_input = int(promotion_input)
scarcity_input = int(scarcity_input)

#feedback
if st.button("Start to predict the future price"):
    if scarcity_input == 0:
       final_predict_price = original_price * 0.8 + (size_input + demand_input * 4 + drop_and_new_input * 3 + promotion_input * 2)
    elif scarcity_input == 1:
       final_predict_price = original_price * 0.9 + (size_input + demand_input * 4 + drop_and_new_input * 3 + promotion_input * 2)
    else:
       final_predict_price = original_price + (size_input  + demand_input * 4 + drop_and_new_input * 3 + promotion_input * 2)

    if original_price <= 0:
        st.error("Sorry,Price must be positive!")
    else:
        if final_predict_price > original_price:
            st.success("Purchase Now 🔥!")
            st.write("final predict price is: ", final_predict_price)
        else:
            st.write("Emm,maybe later 😭")
            st.write("Final predict price is: ",final_predict_price)
