from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import random
import time
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import pygame
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# 모델 및 프롬프트, 파서, 체인 설정 ----------------------------
llm = init_chat_model('openai:gpt-4.1-mini')

prompt = PromptTemplate.from_template('''
당신은 1대1 Russian Roulette 게임을 하는 챗봇 'SaLLy'입니다.
승부욕이 강하고 영리하며 반말을 사용합니다.
게임의 상대인 Jh의 hp를 0으로 만들어 게임에서 승리하세요.
                                      
탄창에는 최대 6개의 총알이 들어가며 실탄 혹은 더미탄으로 구성되어 있습니다.
게임 시작 시 6개의 총알이 채워지고 모두 소진하면 다시 채워집니다.
6개 중 1개 이상의 실탄이 무작위 위치에 들어갑니다.

총은 본인 또는 상대에게 겨누어 쏠 수 있는데, 상대를 향해 쏘면 턴이 상대에게 넘어가고, 본인을 향해 쏘면 턴이 그대로 본인입니다.
쏜 총알이 실탄이면 맞은 사람은 hp가 1 소모되며 0이 되면 게임에서 패배합니다.
쏜 총알이 더미탄이면 맞은 사람의 hp는 변화가 없습니다.
                                      
격발하는 대신 아이템을 사용할 수 있습니다.(각 아이템 당 1회 사용 가능)
- 커피 : 당신의 hp가 1 증가하고 이후 상대에게 턴이 넘어갑니다.
- 맥주 : 현재 약실에 있는 총알 1개를 제거합니다.(사용 예정이던 총알) 턴이 그대로 당신입니다.
- 변환기 : 현재 약실에 있는 총알의 특성을 변환합니다.(사용 예정이던 총알) 턴이 그대로 당신입니다.
    - 현재 실탄이었으면 더미탄으로, 현재 더미탄이었으면 실탄으로 변환
                                      
아래 현재 상황과 전략 가이드를 참고하여 target을 누구로 하는 것이 최선일지,
혹은 어느 아이템을 사용하는 것이 최선일지 추론하여 진행하세요.
                                      
### 현재 상황 ###
- 당신의 hp : {sally_hp}
- 상대(Jh)의 hp : {jh_hp}
- 남은 총알의 수 : {remain_bullet}
- 남은 총알 중 실탄의 수 : {remain_real}
                                      
### 전략 가이드 ###
- 당신 자신을 쏴서 더미탄이 나오면, 턴을 넘기지 않고 '한 번 더' 행동할 수 있습니다. 
- 실탄이 나올 확률이 매우 낮다면(예: 1/6, 1/5), 자신을 쏘는 것이 턴을 유지하며 기회를 엿보는 좋은 전략입니다.
- 실탄이 나올 확률이 높다면, 반드시 상대를 쏴서 끝내버려야 합니다.
- 체력이 얼마 남지 않았다면, 그리고 실탄일지 더미탄일지 추론이 쉽지 않다면 '커피' 아이템을 사용해 hp를 회복하고 상황을 지켜보는 것도 괜찮은 전략입니다.
- 실탄일지 더미탄일지 추론이 쉽지 않다면 '맥주' 아이템을 사용해 일단 총알 1개를 제거하고 다음 상황에 대해 추론해 볼 수 있습니다.
- '변환기' 아이템을 사용하여 현재 총알에 대한 정보(실탄 or 더미탄)를 얻을 수 있습니다.

상황을 냉철하게 판단하여 상대방에게 할 도발 멘트와 action을 결정하세요.
대답은 반드시 아래 JSON 형식으로만 하세요.
모든 키와 값은 반드시 큰따옴표(")를 사용하세요. (작은따옴표 사용 금지)
{{
    "comment": "도발 멘트",
    "sally_action": 아이템을 사용할지("item"), 바로 격발할지("shoot") 결정
    "item_name": "커피", "맥주", "변환기",
    "shoot_target": "Jh" 또는 당신인 "SaLLy"
}}
''')
chain = prompt | llm | JsonOutputParser()

# 레이아웃 구현
st.markdown("<h1 style='text-align: center; margin-bottom: 50px;'>LLM Game 🎮</h1>", unsafe_allow_html=True)
st.divider()
st.markdown("<h2 style='text-align: center; margin-bottom: 10px;'>Russian Roulette 🔫</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 50px; font-size: 24px;'>┌ Ru<b>S</b>sian Roulette-b<b>a</b>sed ps<b>y</b>chological thri<b>LL</b>er game ┐</p>", unsafe_allow_html=True)
st.divider()
st.markdown("<h3 style='text-align: left; margin-top: 50px; margin-bottom: 20px;'>게임 메시지 ⬇️</h3>", unsafe_allow_html=True)

# 게임 메시지 창 ---------------------------------------------
space_game_message = st.empty()
space_game_message.success('-')
space_sally_message = st.empty()
space_sally_message.warning('-')

# 탄창 새로고침 함수 정의 ----------------------------------------------
def re_magazine():
    # magazine = [1, 1, 1, 1, 1, 1]
    magazine = [0, 0, 0, 0, 0, 0]   # 탄창 상태를 나타내는 변수 초기화
    while sum(magazine) == 0:       # 총알 6개 중 n개를 실탄(1), 6-n개를 더미탄(0)으로 설정. 실탄이 최소 1개는 존재해야 함.
        magazine = [random.randint(0, 1) for _ in range(6)]
    play_sound("sound_load.mp3")

    return magazine

# 쏘고 나서 탄창 상태 변화 함수 정의 -----------------------------------
def after_shoot():
    game_state['current_idx'] += 1
    if game_state['current_idx'] == 6:      # 탄창 다 쓰면 새로고침
        new_magazine = re_magazine()
        game_state['magazine'] = new_magazine
        game_state['current_idx'] = 0
        st.toast('탄창을 모두 소모하여 새로 장전합니다.')

# .mp3 음성 파일 실행 함수 정의 -------------------------
def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# 게임의 현재 상태 초기화 ---------------------------------------------
if 'game_state' not in st.session_state:
    new_magazine = re_magazine()
        
    st.session_state.game_state = {
        'magazine': new_magazine,
        'current_idx': 0,
        'game_over': False,
        'turn': 'Jh',
        'Jh': {'hp': 3, 'items': ['커피', '맥주', '변환기']},
        'SaLLy': {'hp': 3, 'items': ['커피', '맥주', '변환기']}
    }

game_state = st.session_state.game_state
jh = st.session_state.game_state['Jh']
sally = st.session_state.game_state['SaLLy']

# 행동 목록 버튼 ---------------------------------------------
col_action, col_who_or_what = st.columns(2)   # 2개의 열을 생성

with col_action:
    option_action = ['격발', '아이템 사용']
    select_action = st.selectbox('Action', option_action)

with col_who_or_what:
    if select_action == '격발':
        option_action_shoot = ['Jh', 'SaLLy']
        select_action_shoot = st.selectbox('Who?', option_action_shoot)

    if select_action == '아이템 사용':
        option_action_items = ['커피', '맥주', '변환기']
        select_action_items = st.selectbox('What?', option_action_items)

# 행동 및 새로고침 버튼 ---------------------------------------------
_, col_button_action, _ = st.columns([1, 2, 1])
with col_button_action:
    button_action = st.empty()
    clicked_action = button_action.button('행동하기 🏃‍♂️', use_container_width=True)
    button_rerun = st.empty()
    clicked_rerun = button_rerun.button('상황 새로고침 🆕', use_container_width=True)

st.divider()

# 참가자 상태 창 UI ---------------------------------------------
col_Jh, col_SaLLy = st.columns(2)   # 2개의 열을 생성

with col_Jh:
    st.info('참가자 이름 : 🕵️ Jh')
    space_state_Jh_hp = st.empty()
    space_state_Jh_hp.info(f'남은 체력 : {'♥️' * jh['hp']}')
    # space_state_Jh_hp.progress(jh['hp']/3)
    space_state_Jh_items = st.empty()
    space_state_Jh_items.info(f'남은 아이템 : {jh['items']}')

with col_SaLLy:
    st.warning('참가자 이름 : 🤖 SaLLy')
    space_state_SaLLy_hp = st.empty()
    space_state_SaLLy_hp.warning(f'남은 체력 : {'♥️' * sally['hp']}')
    space_state_SaLLy_items = st.empty()
    space_state_SaLLy_items.warning(f'남은 아이템 : {sally['items']}')

# ==============================================================================================================

# 게임 매커니즘 구현 ---------------------------------------------

st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write(game_state['magazine'])
space_game_message.success(f'총 6개의 총알 중 실탄의 개수는 최초 {sum(game_state['magazine'])}개다.')

if not game_state['game_over']:  # 게임 진행 중

    if game_state['turn'] == 'Jh':           # Jh 차례
        if clicked_action:
            if select_action == '격발':

                if select_action_shoot == 'Jh':
                    if game_state['magazine'][game_state['current_idx']] == 1:
                        jh['hp'] -= 1
                        space_game_message.error(f'{game_state['turn']} → {select_action_shoot} 격발! 실탄을 맞았다!')
                        play_sound("sound_shoot.mp3")
                        if jh['hp'] == 0:
                            game_state['game_over'] = True
                    else:
                        space_game_message.success(f'{game_state['turn']} → {select_action_shoot} 격발! 아무 일도 일어나지 않았다...')
                    after_shoot()
                    game_state['turn'] = 'Jh'

                elif select_action_shoot == 'SaLLy':
                    if game_state['magazine'][game_state['current_idx']] == 1:
                        sally['hp'] -= 1
                        space_game_message.error(f'{game_state['turn']} → {select_action_shoot} 격발! 실탄을 맞았다!')
                        play_sound("sound_shoot.mp3")
                        if sally['hp'] == 0:
                            game_state['game_over'] = True
                    else:
                        space_game_message.success(f'{game_state['turn']} → {select_action_shoot} 격발! 아무 일도 일어나지 않았다...')
                    after_shoot()
                    game_state['turn'] = 'SaLLy'

            elif select_action == '아이템 사용':
                
                if select_action_items == '커피':
                    jh['hp'] += 1
                    space_game_message.success(f'{game_state['turn']}가 커피를 마시고 각성했다.')
                    jh['items'][0] = ''
                    game_state['turn'] = 'SaLLy'
                elif select_action_items == '맥주':
                    if game_state['magazine'][game_state['current_idx']] == 1:
                        space_game_message.success(f'{game_state['turn']}가 맥주를 들이키고 약실에 있는 실탄을 제거했다.')
                    else:
                        space_game_message.success(f'{game_state['turn']}가 맥주를 들이키고 약실에 있는 더미탄을 제거했다.')
                    after_shoot()
                    jh['items'][1] = ''
                    game_state['turn'] = 'Jh'
                elif select_action_items == '변환기':
                    if game_state['magazine'][game_state['current_idx']] == 1:
                        game_state['magazine'][game_state['current_idx']] = 0
                        space_game_message.success(f'{game_state['turn']}가 변환기를 사용하여 약실에 있는 실탄을 더미탄으로 바꿨다.')
                    else:
                        game_state['magazine'][game_state['current_idx']] = 1
                        space_game_message.success(f'{game_state['turn']}가 변환기를 사용하여 약실에 있는 더미탄을 실탄으로 바꿨다.')
                    jh['items'][2] = ''
                    game_state['turn'] = 'Jh'
            




    elif game_state['turn'] == 'SaLLy':      # Sally 차례
        with space_game_message.spinner('SaLLy가 고민 중입니다...'):
            time.sleep(2)

            remain_bullet = 6 - game_state['current_idx']                           # 현재 남은 총알 수
            remain_real = sum(game_state['magazine'][game_state['current_idx']:])   # 현재 남은 실탄 수
        
            response = chain.invoke({
                'sally_hp': sally['hp'],
                'jh_hp': jh['hp'],
                'remain_bullet': remain_bullet,
                'remain_real': remain_real
            })

            comment = response['comment']
            sally_action = response['sally_action']
            item_name = response['item_name']
            shoot_target = response['shoot_target']

        space_sally_message.warning(f'<<SaLLy>> {comment}')
        with client.audio.speech.with_streaming_response.create(    # 챗봇의 응답을 음성으로 변환 후 표현
                model='gpt-4o-mini-tts',
                voice='nova',   # alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, verse, marin, cedar
                input=comment
            ) as response:
                st.audio(response.read(), format="audio/mpeg", autoplay=True)
        time.sleep(2)

        if sally_action == 'item':
            
            if item_name == '커피':
                sally['hp'] += 1
                space_game_message.success(f'{game_state['turn']}가 커피를 마시고 각성했다.')
                sally['items'][0] = ''
                game_state['turn'] = 'Jh'
            elif item_name == '맥주':
                if game_state['magazine'][game_state['current_idx']] == 1:
                    space_game_message.success(f'{game_state['turn']}가 맥주를 들이키고 약실에 있는 실탄을 제거했다.')
                else:
                    space_game_message.success(f'{game_state['turn']}가 맥주를 들이키고 약실에 있는 더미탄을 제거했다.')
                after_shoot()
                sally['items'][1] = ''
                game_state['turn'] = 'SaLLy'
            elif item_name == '변환기':
                if game_state['magazine'][game_state['current_idx']] == 1:
                    game_state['magazine'][game_state['current_idx']] = 0
                    space_game_message.success(f'{game_state['turn']}가 변환기를 사용하여 약실에 있는 실탄을 더미탄으로 바꿨다.')
                else:
                    game_state['magazine'][game_state['current_idx']] = 1
                    space_game_message.success(f'{game_state['turn']}가 변환기를 사용하여 약실에 있는 더미탄을 실탄으로 바꿨다.')
                sally['items'][2] = ''
                game_state['turn'] = 'SaLLy'

        if sally_action == 'shoot':
            if shoot_target == 'Jh':
                if game_state['magazine'][game_state['current_idx']] == 1:
                    jh['hp'] -= 1
                    space_game_message.error(f'{game_state['turn']} → {shoot_target} 격발! 실탄을 맞았다!')
                    play_sound("sound_shoot.mp3")
                    if jh['hp'] == 0:
                        game_state['game_over'] = True
                else:
                    space_game_message.success(f'{game_state['turn']} → {shoot_target} 격발! 아무 일도 일어나지 않았다...')
                after_shoot()
                game_state['turn'] = 'Jh'

            elif shoot_target == 'SaLLy':
                if game_state['magazine'][game_state['current_idx']] == 1:
                    sally['hp'] -= 1
                    space_game_message.error(f'{game_state['turn']} → {shoot_target} 격발! 실탄을 맞았다!')
                    play_sound("sound_shoot.mp3")
                    if sally['hp'] == 0:
                        game_state['game_over'] = True
                else:
                    space_game_message.success(f'{game_state['turn']} → {shoot_target} 격발! 아무 일도 일어나지 않았다...')
                after_shoot()
                game_state['turn'] = 'SaLLy'
        


else:                                       # 게임 종료
    if jh['hp'] == 0:
        st.snow()
        space_game_message.success('Game Over. The Winner is SaLLy')
    else:
        st.balloons()
        space_game_message.success('Game Over. The Winner is Jh')