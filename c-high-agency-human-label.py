import openai
import streamlit as st
import time
import re  # Import regular expressions

st.subheader("")

from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    default_headers={"OpenAI-Beta": "assistants=v2"}
)
# openai.base_url = "https://api.openai.com/v1/assistants"
openai.default_headers = {"OpenAI-Beta": "assistants=v2"}

# # client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"}, api_key=st.secrets["OPENAI_API_KEY"])
assistant_id = st.secrets["c-high-agency-human-label"]
print(assistant_id)
speed = 200

min_duration = 4
max_duration = 10
human_speed = 80
page2_stay = 6
import random

partner_names = ['星辰','暖阳下的猫','梦之尘','听雨','JM','Mars','海','蓝色星期五']

if 'partner_names' not in st.session_state:
    st.session_state.partner_names = None
# random select a partner name

if not st.session_state.partner_names:
    partner_name = random.choice(partner_names)
    st.session_state.partner_names = partner_name
    
partner_name = st.session_state.partner_names

if "session_end" not in st.session_state:
    st.session_state.session_end = False

from streamlit_image_select import image_select
# Avatar selection
avatars = [
    "https://ooo.0x0.ooo/2024/06/03/OJGv0r.png",  # Replace these URLs with your actual avatar image 
    "https://ooo.0x0.ooo/2024/06/03/OJGm1G.png",
    "https://ooo.0x0.ooo/2024/06/03/OJGpH1.png",
    "https://ooo.0x0.ooo/2024/06/03/OJGZKc.png",
    # "animal_avatar/animal_avatar_5.png",
]


partner_avatars = ['https://ooo.0x0.ooo/2024/06/03/OJGQMg.png',
'https://ooo.0x0.ooo/2024/06/03/OJGcXK.png',
'https://ooo.0x0.ooo/2024/06/03/OJGE0l.png',
'https://ooo.0x0.ooo/2024/06/03/OJGS7B.png',
'https://ooo.0x0.ooo/2024/06/03/OJG0Hs.png',
'https://ooo.0x0.ooo/2024/06/03/OJGsza.png',]

if 'partner_avatar' not in st.session_state:
    st.session_state.partner_avatar = None

if not st.session_state.partner_avatar:
    st.session_state.partner_avatar = random.choice(partner_avatars)

partner_avatar = st.session_state.partner_avatar

if "instruction_displayed" not in st.session_state:
    st.session_state.instruction_displayed = False
    
if "thread_id" not in st.session_state:
    try:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        print(f"Created thread with ID: {thread.id}")
    except Exception as e:
        print(f"Error creating thread: {e}")
        # If the first attempt fails, try recreating the client with explicit headers
        new_client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"],
            default_headers={"OpenAI-Beta": "assistants=v2"}
        )
        thread = new_client.beta.threads.create()
        st.session_state.thread_id = thread.id

if "show_thread_id" not in st.session_state:
    st.session_state.show_thread_id = False

if 'first_message_sent' not in st.session_state:
    st.session_state.first_message_sent = False
if 'message_lock' not in st.session_state:
    st.session_state.message_lock = False


    
if 'duration' not in st.session_state:
    st.session_state.duration = 0
    
if 'first_input_time' not in st.session_state:
    st.session_state.first_input_time = None

print(f'session duration: {st.session_state.duration}')

if st.session_state.first_input_time:
    print(f'time till now {(time.time() - st.session_state.first_input_time) / 60}')

if "page" not in st.session_state:
    st.session_state.page = 0

def next_page(): 
    st.empty()
    st.session_state.page += 1
    st.empty()
content = st.empty()

if 'user_avatar' not in st.session_state:
    st.session_state.user_avatar = avatars[0]
if 'user_name' not in st.session_state:
    st.session_state.user_name = "你"


if st.session_state.page == 1:
    st.empty()
    # create an ampty placeholder
    avatar_placeholder = st.empty()
    avatar_placeholder.markdown("#### 头像设置成功！")
    
    
    # with st.spinner("#### 正在匹配聊天搭档..."):
    #     time.sleep(3)
    # # st.success("头像设置成功，现在可以开始聊天了！正在匹配聊天搭档...")
    # # sleep for 2 seconds
    # # time.sleep(2)
    # insert gap 
    st.empty()
    st.empty()
    st.empty()
    st.empty()
    st.empty()
    st.empty()
    st.empty()
    
    match_placeholder = st.empty()
    match_placeholder.markdown("\n\n\n\n\n\n\n\n\n\n  ##### :red[正在为你匹配其他实验被试......]", unsafe_allow_html=True)
    progress_text = ":orange[:hourglass:]"
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        # random progress
        import random
        sleep_time = random.uniform(0.01, 0.1)
        time.sleep(sleep_time)
        my_bar.progress(percent_complete + 1, text=progress_text)
    sucess_placeholder = st.empty()
    sucess_placeholder.success(f"搭档已匹配成功！请和他共同完成实验任务。")
    
    
    
    
    
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.markdown("\n")
        matched_info_placeholder = st.empty()
        matched_info_placeholder.markdown(f" \n 为你匹配到的搭档是 :blue[{partner_name}]", unsafe_allow_html=True)
    with col2:
        matched_avatar_placeholder = st.empty()
        matched_avatar_placeholder.image(partner_avatar, width=50)
        
    with st.spinner("正在为你开启对话..."):
        time.sleep(page2_stay)
    
    # time.sleep(3)
    
    st.empty()
    my_bar.empty()
    avatar_placeholder.empty()
    match_placeholder.empty()
    sucess_placeholder.empty()
    match_placeholder.empty()
    matched_info_placeholder.empty()
    matched_avatar_placeholder.empty()
    next_page()
    
    

if st.session_state.page == 0:
# Avatar selection component
    st.title("欢迎来到聊天室")
    
    st.markdown("#### 请先选择一个头像")
    selected_index = image_select(
        label="",
        images=avatars,
        return_value="index"
    )
    st.session_state.user_avatar = avatars[selected_index]
    st.markdown("\n \n \n")
    st.markdown("#### 请输入你的昵称")
    text_input = st.text_input(
        "👇",
    )
    if text_input:
        st.session_state.user_name = text_input
    # pass on user_avatar to the next page
        
   
    
    if st.button("确定", on_click=next_page, type = "primary", use_container_width=True):
        # show sucess and then navigate to the next page
        st.success("头像已选择")



elif st.session_state.page == 2:
    
    user_avatar = st.session_state.user_avatar
    
    # def a delay display function

        

    




        
    # Automatically send a "hello" message when the chat begins

    # This is where we create a placeholder for the countdown timer
    st.sidebar.markdown("你们的任务是设计一个浙江大学紫金港校区的交通优化方案。方案应包括以下三个方面：\n "
        "1. :blue[**问题识别**]：当前校园交通系统中存在的主要问题。\n"
        "2. :blue[**解决方案设计**]：提出切实可行的解决方案，解决识别出的主要问题。\n"
        "3. :blue[**实施计划**]：包括优先级排序、时间表和预算估算等。\n \n"
        "你们有5至10分钟的时间进行讨论，并得出一个优化方案。\n \n 讨论结束后，请将你们的方案提交至聊天界面下方的文本框中。", unsafe_allow_html=True)



    st.sidebar.markdown("#### 请输入“:red[你好]”开启你们的讨论！👋 \n \n 请先开启对话以获取对话编号 \n")
    thred_id_placeholder = st.sidebar.empty()
    timer_placeholder = st.sidebar.empty()
    # timer_placeholder.markdown(f"##### 请先开启对话 ",unsafe_allow_html=True)

    def refresh_timer():
        if st.session_state.first_input_time:
            st.session_state.duration = (time.time() - st.session_state.first_input_time) / 60
            remaining_time = max_duration - st.session_state.duration
            thread_id_remaining = min_duration - st.session_state.duration
            
            def format_time(minutes):
                # convert minutes (is a float) to xx min xx sec
                minutes_new = int(minutes)
                seconds = int((minutes - int(minutes)) * 60)
                return f"{minutes_new} 分钟 {seconds} 秒"
            
            if remaining_time > 0:
                timer_placeholder.markdown(
                    f"##### 对话会在<strong><span style='color: #8B0000;'> {format_time(remaining_time)} </span></strong>之后结束。\n",
                    unsafe_allow_html=True)
                
            if thread_id_remaining <= 0:
                st.session_state.show_thread_id = True
                # st.sidebar.info(st.session_state.thread_id)
                


    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    st.empty()
    st.empty()
    st.empty()
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar=user_avatar):
                # st.markdown(message["content"]) 
                user_input = message["content"]
                user_name = st.session_state.user_name
                st.markdown("<span style='color: red;'>" + user_name + "：</span>" + user_input, unsafe_allow_html=True)
                
        else:
            with st.chat_message(message["role"],avatar=partner_avatar):
                # st.markdown(message["content"], unsafe_allow_html=True)
                
                partner_input = message["content"]
                st.markdown("<span style='color: red;'>" + partner_name + "：</span>" + partner_input, unsafe_allow_html=True)
                
                


            

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("style.css")





    def update_typing_animation(placeholder, current_dots):
        """
        Updates the placeholder with the next stage of the typing animation.

        Args:
        placeholder (streamlit.empty): The placeholder object to update with the animation.
        current_dots (int): Current number of dots in the animation.
        """
        num_dots = (current_dots % 6) + 1  # Cycle through 1 to 3 dots
        placeholder.markdown("对方正在输入" + "." * num_dots)
        return num_dots
    

            
            



    # Handling message input and response
    max_messages = 40  # 10 iterations of conversation (user + assistant)

    min_messages = 0


    if (not st.session_state.first_input_time) or (st.session_state.first_input_time and time.time() - st.session_state.first_input_time <= max_duration * 60):
        
        # if first_input_time is not None, check if the user has been inactive for more than 1 minute
        if st.session_state.first_input_time:
            if time.time() - st.session_state.first_input_time > min_duration * 60:
                st.session_state.show_thread_id = True
                # st.sidebar.info(st.session_state.thread_id)
                
            
        # Initialize the timer once outside the main interaction loop
        refresh_timer()
        user_input = st.chat_input("")
        

            
                
        if user_input and not st.session_state.instruction_displayed:
            st.session_state.instruction_displayed = True
        
        if not st.session_state.instruction_displayed:
            time.sleep(2)
            st.toast('请输入“:red[你好]”开启你们的讨论！',icon="👋")
            time.sleep(3)
            st.toast('请输入“:red[你好]”开启你们的讨论！',icon="👋")
            time.sleep(3)
            st.toast('请输入“:red[你好]”开启你们的讨论！',icon="👋")
            time.sleep(3)
            st.toast('请输入“:red[你好]”开启你们的讨论！',icon="👋")
            time.sleep(3)
            st.toast('请输入“:red[你好]”开启你们的讨论！',icon="👋")
            time.sleep(3)                
        
        
        if user_input:
            
                
            if not st.session_state.first_input_time:
                st.session_state.first_input_time = time.time()

            
            # st.sidebar.caption("请复制thread_id")
            # st.session_state.first_message_sent = True
            st.session_state.messages.append({"role": "user", "content": user_input})
            # st.rerun()

            with st.chat_message("user", avatar=user_avatar):
                # st.markdown(user_input)
                # user_input = message["content"]
                user_name = st.session_state.user_name
                st.markdown("<span style='color: red;'>" + user_name + "：</span>" + user_input, unsafe_allow_html=True)

            with st.chat_message("assistant",avatar=partner_avatar):
                message_placeholder = st.empty()
                waiting_message = st.empty()  # Create a new placeholder for the waiting message
                dots = 0

            
                import time
                max_attempts = 2
                attempt = 0
                while attempt < max_attempts:
                    try:
                        update_typing_animation(waiting_message, 5)  # Update typing animation
                        message = client.beta.threads.messages.create(
                            thread_id=st.session_state.thread_id,
                            role="user",
                            content=user_input
                        )
                        run = client.beta.threads.runs.create(
                            thread_id=st.session_state.thread_id,
                            assistant_id=assistant_id
                        )
                        # Wait until run is complete
                        while True:
                            run_status = client.beta.threads.runs.retrieve(
                                thread_id=st.session_state.thread_id,
                                run_id=run.id
                            )
                            if run_status.status == "completed":
                                finish_time = time.time()
                                break
                            dots = update_typing_animation(waiting_message, dots)  # Update typing animation
                            time.sleep(0.3) 
                        # Retrieve and display messages
                        messages = client.beta.threads.messages.list(
                            thread_id=st.session_state.thread_id
                        )
                        full_response = messages.data[0].content[0].text.value
                        
                        def delay_display(text):
                            # calculate the number of characters in the text
                            # get number of chinese characters
                            # return delay time in seconds
                            char_length = len(text)
                            print(f'char_length: {char_length}')
                            delay = char_length / human_speed * 60
                            return delay
                        
                        wait_deplay = delay_display(full_response)
                        print(f'wait_deplay: {wait_deplay}')
                        
                        def display_typing(placeholder, duration, gap):
                            # display typing message for a certain duration
                            interval = int(duration / (1/gap)) + 1
                            for i in range(interval):
                                num_dots = (i % 6) + 1  # Cycle through 1 to 3 dots
                                placeholder.markdown("对方正在输入" + "." * num_dots)
                                time.sleep(gap)
                                placeholder.empty()
                        
                        display_typing(waiting_message, int(wait_deplay), 0.5)
                            
                        
                        
                        
                        waiting_message.empty()
                        
                        
                        
                        
                        
                        message_placeholder.markdown("<span style='color: red;'>" + partner_name + "：</span>" + full_response, unsafe_allow_html=True)
                        break
                    
                    
                    except Exception as e:
                        print(e)
                        attempt += 1
                        if attempt < max_attempts:
                            print(f"An error occurred. Retrying in 5 seconds...")
                            time.sleep(5)
                        else:
                            error_message_html = """
                                <div style='display: inline-block; border:2px solid red; padding: 4px; border-radius: 5px; margin-bottom: 20px; color: red;'>
                                    <strong>网络错误:</strong> 请重试。
                                </div>
                                """
                            full_response = error_message_html
                            waiting_message.empty()
                            message_placeholder.markdown(full_response, unsafe_allow_html=True)

    #------------------------------------------------------------------------------------------------------------------------------#


                


                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
        st.empty()
        st.empty()

    else:
        # st.sidebar.info(st.session_state.thread_id)
        if user_input := st.chat_input("", disabled=True):
            st.info("时间已到。请从侧边栏复制对话编号。将对话编号粘贴到下面的文本框中。")
            st.session_state.session_end = True

        # if user_input:= st.chat_input(""):
        #     with st.chat_message("user"):
        #         st.markdown(user_input)
            

        
        #     with st.chat_message("assistant"):
        #         message_placeholder = st.empty()
        #         message_placeholder.info(
        #             "此聊天机器人的对话上限已达到。请从侧边栏复制thread_ID。将thread_ID粘贴到下面的文本框中。"
        #         )
        # st.chat_input(disabled=True)


    while True:
        if st.session_state.show_thread_id:
            thred_id_placeholder.info(st.session_state.thread_id)
        if st.session_state.session_end:
            st.session_state.show_thread_id = False
            break
        refresh_timer()
        time.sleep(0.6)  # Adjust this value as necessary for your use case