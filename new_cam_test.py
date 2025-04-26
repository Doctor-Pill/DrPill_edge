import cv2

def test_camera(camera_index):
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"카메라 {camera_index} 열기에 실패했습니다.")
        return

    print(f"카메라 {camera_index}를 열었습니다. 'q'를 눌러 종료합니다.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break
        
        cv2.imshow(f"Camera {camera_index}", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("테스트할 카메라 번호를 입력하세요 (예: 0 또는 1)")
    cam_index = int(input("카메라 인덱스 입력: "))
    test_camera(cam_index)
