# Caro AI in Python- Minimax và Alpha-Beta pruning
 
## Giới thiệu
Dự án này là chương trình AI chơi cờ Caro sử dụng giao diện đồ họa với Tkinter, cho phép người chơi đấu cờ với AI hoặc nhờ AI đưa ra nước đi với trạng thái bàn cờ có sẵn. AI sử dụng 2 thuật toán **Minimax** và **Alpha-Beta pruning** với cùng độ sâu tìm kiếm và hàm đánh giá. Chương trình hiển thị nước đi được chọn, giá trị đánh giá, số trạng thái duyệt và thời gian tính toán

## Tổng quan
**Bàn cờ**: 9x9, người chơi nào có chuỗi 4 quân liên tiếp là thắng, không xét luật chặn 2 đầu
Người chơi(đi trước): X, AI(đi sau): O

**AI**: sử dụng thuật toán Minimax hoặc Alpha-Beta với độ sâu tìm kiếm tùy chỉnh

**Giao diện**: Sử dụng thư viện Tkinter để xây dựng, click chuột để đánh cờ, cho phép tải bàn cờ từ file .txt, cho phép đề xuất nước đi được tính toán bởi AI

## Yêu cầu
**Python**: 3.6 trở lên

**Thư viện**: 'tkinter', 'math', 'copy', 'time', 'typing' đã có sẵn khi cài đặt python
## Cấu trúc thư mục
```text
Caro_AI/
├── main.py              # Entry point & game loop
├── requirements.txt
├── game/
│   ├── constants.py     # Hằng số toàn cục
│   └── game_logic.py    # Trạng thái game
├── AI/
│   ├── evaluation.py    # Hàm trạng thái, đánh giá
│   └── ai_algorithm.py  # Minimax, Alpha-Beta
└── UI/
    ├── main.py          # Khởi chạy UI
    └── gui.py           # Triển khai bàn cờ
```

## Tính năng
**Chơi trực tiếp** với AI: nhấp chuột đặt quân X, AI đáp trả bằng quân O

**Chọn thuật toán** : chọn thuật toán để AI sử dụng, có hiệu lực ngay nước đi tiếp theo

**Tải bàn cờ** : đưa trạng thái bàn cờ, AI sẽ đưa ra gợi ý nước đi tiếp theo tốt nhất

**So sánh thuật toán**: chạy đồng thời cả 2 thuật toán trên trạng thái hiện tại và hiển thị kết quả để so sánh

**Điều chỉnh độ khó** : chọn độ khó ở thanh spinbox, giá trị cao thì độ khó cao hơn

## Thiết kế
**Evaluation** sử dụng chung cho Minimax và Alpha-Beta trong AI-algorithm

**gui** nhận tác vụ vẽ bàn cờ, vẽ nước đi, đưa ra thông tin trạng thái

**main** trình khởi chạy AI

## License
Dự án phát triển nhằm mục đích học tập và thử nghiệm, mọi người đều có thể sử dụng, chia sẻ

## Tác giả
Nguyễn Văn Phúc 

Nguyễn Phùng Phước

Trần Hoàng Phương
