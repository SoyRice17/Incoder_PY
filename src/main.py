from util import ConfigManager
import gui.gui_manager as gui

def init_app():
    """애플리케이션 초기화 및 실행"""
    try:
        app = gui.GuiManager()
        app.run()
    except Exception as e:
        print(f"애플리케이션 실행 중 오류 발생: {e}")
    finally:
        ConfigManager().save_config()

if __name__ == "__main__":
    init_app()

# 죄송합니다 하루만 날먹 하겠습니다.

### todo
## 인코딩 관련 개선사항
# 인코딩 진행률 GUI 업데이트 미작동
# 저해상도 영상 강제 리사이징 문제
# 선택된 코덱에 따른 적절한 인코딩 파라미터 최적화 필요
# - H.264: crf 23-28 권장
# - H.265: crf 28-32 권장
# - AV1: crf 30-34 권장
# - VP9: crf 31-35 권장

## GUI 레이아웃 개선사항
# 메인 윈도우 크기 조절 가능하도록 수정
# 리스트박스 크기 동적 조절 지원
# 프로그레스바 추가하여 작업 진행상황 표시

## 성능 최적화
# 대용량 파일 처리시 메모리 사용량 최적화
# 멀티스레딩 구현으로 UI 응답성 향상
# 파일 검색 알고리즘 개선

## 사용자 경험 개선
# 드래그 앤 드롭으로 파일 추가 기능
# 키보드 단축키 지원 (삭제, 저장 등)
# 작업 취소/복구 기능 추가

## 에러 처리
# 파일 접근 권한 오류 처리
# 잘못된 파일 형식 처리
# 네트워크 오류 처리 (원격 파일 접근시)

## 기능 추가
# 자동 저장 기능
# 설정 프리셋 저장/불러오기
# 로그 기록 시스템 구현
# 배치 프로세싱 지원

## 테스트
# 단위 테스트 작성
# 통합 테스트 구현
# 성능 테스트 시나리오 작성
