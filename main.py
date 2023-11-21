TOKEN = "YOUR_TOKEN"
from telebot import TeleBot, types
import model_train
bot = TeleBot(TOKEN)
X_test_of_user = {}


@bot.message_handler(commands=['hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi " + message.from_user.first_name + "!")


@bot.message_handler(commands=['start'])
def start(message):
    age_markup = create_age_markup()
    bot.send_message(message.chat.id, "Choose your age:", reply_markup=age_markup)
    gender_markup = create_gender_markup()
    bot.send_message(message.chat.id, "Choose your gender:", reply_markup=gender_markup)
    bmi_markup = create_bmi_markup()
    bot.send_message(message.chat.id, "Choose your Body Mass Index:", reply_markup=bmi_markup)
    children_markup = create_children_markup()
    bot.send_message(message.chat.id, "State the number of children you have:", reply_markup=children_markup)
    smoker_markup = create_smoker_markup()
    bot.send_message(message.chat.id, "Do you smoke?:", reply_markup=smoker_markup)
    region_markup = create_region_markup()
    bot.send_message(message.chat.id, "Choose your region:", reply_markup=region_markup)


# __________markup for smoker____________________
def create_smoker_markup():
    smoker_options = ["No", "Yes"]
    markup = types.InlineKeyboardMarkup()

    for smoker in smoker_options:
        markup.add(types.InlineKeyboardButton(str(smoker), callback_data=f"smoker_{smoker}"))

    return markup


# _________markup for region_____________________
def create_region_markup():
    region_options = ['southwest', 'southeast', 'northwest', 'northeast']
    markup = types.InlineKeyboardMarkup()

    for region in region_options:
        markup.add(types.InlineKeyboardButton(str(region), callback_data=f"region_{region}"))
    return markup


# _________markup for children__________________
def create_children_markup():
    children_options = [0, 1, 2, 3, 4, 5, "More"]
    markup = types.InlineKeyboardMarkup()

    for children in children_options:
        markup.add(types.InlineKeyboardButton(str(children), callback_data=f"children_{children}"))
    return markup


# _________markup for bmi________________________
def create_bmi_markup():
    bmi_options = list(range(15, 53))
    markup = types.InlineKeyboardMarkup()

    for bmi in bmi_options:
        markup.add(types.InlineKeyboardButton(str(bmi), callback_data=f"bmi_{bmi}"))

    return markup


# _________markup for gender_____________________
def create_gender_markup():
    gender_options = ["Male", "Female"]
    markup = types.InlineKeyboardMarkup()

    for gender in gender_options:
        markup.add(types.InlineKeyboardButton(str(gender), callback_data=f"gender_{gender}"))

    return markup


# __________markup for ages _______________________-
def create_age_markup():
    age_options = list(range(1, 101))
    markup = types.InlineKeyboardMarkup()

    for age in age_options:
        markup.add(types.InlineKeyboardButton(str(age), callback_data=f"age_{age}"))

    return markup


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    query_data = call.data.split('_')
    category = query_data[0]
    selected_value = query_data[1]

    if category == "smoker":
        X_test_of_user["smoker"] = 1 if selected_value == "Yes" else 0
    elif category == "region":
        X_test_of_user["region"] = {"southwest": 3, "southeast": 2, "northwest": 1, "northeast": 0}.get(selected_value, 0)
    elif category == "children":
        X_test_of_user["children"] = 5 if selected_value == "More" else int(selected_value)
    elif category == "bmi":
        X_test_of_user["bmi"] = float(selected_value)
    elif category == "gender":
        X_test_of_user["gender"] = 0 if selected_value == "Female" else 1
    elif category == "age":
        X_test_of_user["age"] = float(selected_value)

    print(f"Selected {category}: {selected_value}")
    bot.answer_callback_query(call.id, f"You selected {category}: {selected_value}")
    print(X_test_of_user)
    if len(X_test_of_user)==6:

        bot.send_message(chat_id=call.from_user.id, text="Your request is in progress")
        arr = [[X_test_of_user['age'],X_test_of_user['gender'],X_test_of_user['bmi'],X_test_of_user['children'],X_test_of_user['smoker'],X_test_of_user['region']]]
        bot.send_message(chat_id=call.from_user.id, text=f"Your charge will {model_train.returnCharges(arr)}")

if __name__ == "__main__":
    bot.polling()


