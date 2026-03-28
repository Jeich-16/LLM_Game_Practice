# LLM_Game_Practice
LLM Game 만들기 실습

<br/><br/>

## Russian Roulette 🔫
#### ┌ RuSsian Roulette-based psychological thriLLer game ┐
---

<br/><br/>

## 📋 개요
![123](https://github.com/user-attachments/assets/f4bba011-4abc-4ef4-a42e-82925ba70b92)
> itch.io | Steam 에서 출시된 게임 'Buckshot Roulette'
> [출처](https://namu.wiki/w/Buckshot%20Roulette)<br/><br/>
> 본 게임은 Russian Roulette 게임 기반 심리 스릴러 게임으로,<br/>
> Russian Roulette 규칙에 LLM의 추론 능력과 페르소나를 결합한 1:1 턴제 전략 게임입니다.<br/>
> 단순한 확률 게임을 넘어, AI의 도발과 심리적 압박 속에서 긴장감 넘치는 대결을 제공합니다.

<br/><br/>

## 적용 기술 Stack
|   기술   | 내용            | 모델 |
|:--------:|:-----------------:|:-----------------:|
| 웹 인터페이스 | 게임 상태 UI 구현 실시간 반영 | streamlit |
| LLM Framework | 프롬프트 엔지니어링 및 모델 연동 | LangChain<br/>gpt-4.1-mini |
| TTS | AI 모델의 답변 텍스트를 자연스러운 음성으로 변환 | gpt-4o-mini-tts |

<br/><br/>

## Workflow
> 게임 상태 초기화<br/>
- 6발의 탄창에 무작위로 실탄 장전<br/>
> 유저의 선제 진행<br/>
- Action(격발 / 아이템 사용)과 Who?(본인 혹은 상대) 또는 What?(아이템) 선택 후 '행동하기' 버튼 클릭
- '상황 새로고침' 버튼을 클릭하여 탄환 결과에 따른 게임 상태 업데이트
> AI SaLLy에게 턴이 넘어갈 경우 AI SaLLy가 현재 상태에 따라 추론 후 행동 진행<br/>
- AI SaLLy가 생성하는 텍스트가 출력되고 TTS로 음성 변환
> 둘 중 한 명의 체력이 0이 되면 게임 종료<br/>

<br/><br/>

---

## 진행 화면
<img width="450" height="auto" alt="1" src="https://github.com/user-attachments/assets/95d2aa92-839b-4e5a-a129-dd71c9a84735" /><br/>↑ 게임 이름과 소개<br/><br/>
<img width="450" height="auto" alt="2" src="https://github.com/user-attachments/assets/03771791-b05b-41d7-8c51-f6f2fc40e44b" /><br/>↑ 게임 메시지 박스와 행동 탭<br/><br/>
<img width="450" height="auto" alt="3" src="https://github.com/user-attachments/assets/1e817c2f-03bf-44da-b334-10998da651da" /><br/>↑ 참가자 정보<br/><br/>
<img width="450" height="auto" alt="4" src="https://github.com/user-attachments/assets/bfdec7eb-460a-40fe-b368-7d26a2b78365" /><br/>↑ 상대 AI에게 턴이 넘어간 경우<br/><br/>
<img width="450" height="auto" alt="5" src="https://github.com/user-attachments/assets/2b906c6c-b16a-4276-8c2a-eb0563b73592" /><br/>↑ 상대 AI의 행동 개시 및 멘트 출력(텍스트 & 음성)<br/><br/>
<img width="450" height="auto" alt="6" src="https://github.com/user-attachments/assets/66501ca1-7922-454b-bdb8-8d420bfd00f5" /><br/>↑ 아이템 사용<br/><br/>


<br/><br/>

## 한계 및 개선점
- LangGraph 구조 구축<br/>
- 1:n 대결 구도<br/>
- 유기적인 Gameflow 표현을 위한 UI 개선<br/>
- 전략 요소(아이템 등) 추가<br/>
- 시각화 요소 Develop<br/>
