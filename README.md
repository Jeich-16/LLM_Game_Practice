# LLM_Game_Practice
LLM Game 만들기 실습

<br/><br/>

## Russian Roulette 🔫
#### ┌ RuSsian Roulette-based psychological thriLLer game ┐
---

<br/><br/>

## 📋 개요
![123](https://github.com/user-attachments/assets/d8f8698d-5b08-4c04-a92c-ab41805fa22b)
[출처](https://namu.wiki/w/Buckshot%20Roulette)
> itch.io | Steam 에서 출시된 게임 <Buckshot Roulette><br/><br/>
> 본 게임은 Russian Roulette 게임 기반 심리 스릴러 게임으로,<br/>
> Russian Roulette 규칙에 LLM의 추론 능력과 페르소나를 결합한 1:1 턴제 전략 게임입니다.<br/>
> 단순한 확률 게임을 넘어, AI의 도발과 심리적 압박 속에서 긴장감 넘치는 대결을 제공합니다.

<br/><br/>

## 적용 기술 Stack
|   기술   | 내용            | 모델 |
|:--------:|:-----------------:|:-----------------:|
| 웹 인터페이스 | 게임 상태 UI 구현 실시간 반영 | streamlit |
| LLM Framework | 프롬프트 엔지니어링 및 모델 연동 | LangChain |
| TTS | AI 모델의 답변 텍스트를 자연스러운 음성으로 변환 | gpt-4o-mini-tts |

<br/><br/>

## Workflow
> 게임 상태 초기화<br/>
- 6발의 탄창에 무작위로 실탄 장전<br/>
> 유저의 선제 진행<br/>
- Action(격발)과 Who?(본인 혹은 상대) 선택 후 '행동하기' 버튼 클릭
- '상황 새로고침' 버튼 클릭 후 탄환 결과에 따른 게임 상태 업데이트
> AI SaLLy에게 턴이 넘어갈 경우 AI SaLLy가 현재 상태에 따라 추론 후 행동 진행<br/>
- AI SaLLy가 생성하는 텍스트가 출력되고 TTS로 음성 변환
> 둘 중 한 명의 체력이 0이 되면 게임 종료<br/>

<br/><br/>

---

<!-- ## 진행 결과
<img width="450" height="auto" alt="01" src="https://github.com/user-attachments/assets/d2da10a0-e661-4d7c-87be-d4dbc658693d" />  
<img width="450" height="auto" alt="02" src="https://github.com/user-attachments/assets/8c3425b9-798b-437f-8877-1c9f2ebfd834" /><br/><br/>
<img width="450" height="auto" alt="03" src="https://github.com/user-attachments/assets/3b1d39f6-3f5a-48e9-a373-17b12e88f664" />  
<img width="450" height="auto" alt="04" src="https://github.com/user-attachments/assets/60a94a53-bdb6-4387-a4ce-c986690025ed" /><br/><br/> -->

<br/><br/>

## 한계 및 개선점
> 격발 외에 아이템 사용 액션 추가
- 전략적으로 아이템 활용 가능
> 격발 등의 행동 효과음 추가
- 효과음 음성 파일 확보 필요
> 시각화 요소 Develop
> LangGraph 구조 구축
