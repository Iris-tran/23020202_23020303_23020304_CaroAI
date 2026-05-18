import tkinter as tk
from tkinter import messagebox, filedialog
import math
import copy
import time
from constants import BOARD_SIZE, CELL_SIZE, BOARD_PADDING, WINDOW_WIDTH, WINDOW_HEIGHT, EMPTY, PLAYER_X, AI_O, MAX_DEPTH
from game_logic import check_win, is_draw
from AI_algorithm import minimax, alphabeta

class GameBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Cờ Caro - AI đề xuất nước đi")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_turn = PLAYER_X
        self.game_over = False
        self.suggestion_move = None
        self.ai_algorithm = "alphabeta"
        self.ai_player = AI_O
        self.last_ai_move = None   # Lưu nước đi cuối của AI

        # Canvas vẽ bàn cờ - đặt ở trên cùng
        self.canvas = tk.Canvas(root, bg="#EDEAE6")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.draw_board()

        # Khung điều khiển ở dưới cùng, chiều cao cố định
        self.control_frame = tk.Frame(root, bg="#f0f0f0", height=140)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.control_frame.pack_propagate(False)  # Giữ nguyên chiều cao

        # Bố trí các dòng bên trong control_frame bằng grid
        # Hàng 0: Thuật toán
        row0 = tk.Frame(self.control_frame, bg="#f0f0f0")
        row0.pack(pady=5)
        tk.Label(row0, text="Thuật toán AI:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.btn_minimax = tk.Button(row0, text="Minimax", command=lambda: self.set_algorithm("minimax"),
                                     bg="#FF9800", fg="white", width=10)
        self.btn_minimax.pack(side=tk.LEFT, padx=5)
        self.btn_alphabeta = tk.Button(row0, text="Alpha-Beta", command=lambda: self.set_algorithm("alphabeta"),
                                       bg="#9C27B0", fg="white", width=10)
        self.btn_alphabeta.pack(side=tk.LEFT, padx=5)

        # Hàng 1: Chức năng
        row1 = tk.Frame(self.control_frame, bg="#f0f0f0")
        row1.pack(pady=5)
        load_btn = tk.Button(row1, text="Tải trạng thái từ file", command=self.load_state_from_file, bg="#2196F3", fg="white")
        load_btn.pack(side=tk.LEFT, padx=5)
        suggest_btn = tk.Button(row1, text="Đề xuất nước đi (AI)", command=self.suggest_move, bg="#4CAF50", fg="white")
        suggest_btn.pack(side=tk.LEFT, padx=5)
        compare_btn = tk.Button(row1, text="So sánh Minimax vs Alpha-Beta(cho nước AI vừa đi)", command=self.compare_algorithms, bg="#FF5722", fg="white")
        compare_btn.pack(side=tk.LEFT, padx=5)
        newgame_btn = tk.Button(row1, text="Ván mới", command=self.new_game, bg="#607D8B", fg="white")
        newgame_btn.pack(side=tk.LEFT, padx=5)

        # Hàng 2: Trạng thái
        row2 = tk.Frame(self.control_frame, bg="#f0f0f0")
        row2.pack(pady=5)
        self.status_label = tk.Label(row2, text="Lượt của bạn (X)", bg="#f0f0f0", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=10)

        # Hàng 3: Độ sâu và mô tả
        row3 = tk.Frame(self.control_frame, bg="#f0f0f0")
        row3.pack(pady=5)
        tk.Label(row3, text="Độ sâu tìm kiếm:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.depth_var = tk.IntVar(value=MAX_DEPTH)
        self.depth_spinbox = tk.Spinbox(row3, from_=1, to=5, width=5, textvariable=self.depth_var, command=self.change_depth)
        self.depth_spinbox.pack(side=tk.LEFT, padx=5)
        self.depth_desc_label = tk.Label(row3, text=self.get_depth_description(MAX_DEPTH), bg="#f0f0f0", font=("Arial", 9, "italic"), fg="blue")
        self.depth_desc_label.pack(side=tk.LEFT, padx=10)

        self.canvas.bind("<Button-1>", self.on_click)
        self.update_button_highlight()

    def set_algorithm(self, algorithm):
        self.ai_algorithm = algorithm
        self.update_button_highlight()
        self.status_label.config(text=f"Đã chuyển sang {algorithm.upper()}")
        print(f"[AI] Thuật toán hiện tại: {algorithm.upper()}")

    def update_button_highlight(self):
        if self.ai_algorithm == "minimax":
            self.btn_minimax.config(bg="#FF5722", relief=tk.SUNKEN)
            self.btn_alphabeta.config(bg="#9C27B0", relief=tk.RAISED)
        else:
            self.btn_alphabeta.config(bg="#E91E63", relief=tk.SUNKEN)
            self.btn_minimax.config(bg="#FF9800", relief=tk.RAISED)

    def draw_board(self):
        """Vẽ bàn cờ và quân cờ, nước đi cuối, kèm theo gợi ý nếu có."""
        self.canvas.delete("all")
        # Vẽ lưới
        for i in range(BOARD_SIZE+1):
            start = BOARD_PADDING
            end = BOARD_PADDING + (BOARD_SIZE)*CELL_SIZE
            self.canvas.create_line(start, BOARD_PADDING + i*CELL_SIZE, end, BOARD_PADDING + i*CELL_SIZE, fill="black")
            self.canvas.create_line(BOARD_PADDING + i*CELL_SIZE, start, BOARD_PADDING + i*CELL_SIZE, end, fill="black")
        # Vẽ quân cờ
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] != EMPTY:
                    # Tâm ô vuông
                    x = BOARD_PADDING + j*CELL_SIZE + CELL_SIZE//2
                    y = BOARD_PADDING + i*CELL_SIZE + CELL_SIZE//2
                    color = "blue" if self.board[i][j] == PLAYER_X else "red"
                    self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="black", width=2)
                    self.canvas.create_text(x, y, text=self.board[i][j], font=("Arial", 18, "bold"), fill="white")
        # Vẽ gợi ý (viền xanh quanh ô đề xuất)
        if self.suggestion_move:
            i, j = self.suggestion_move
            x = BOARD_PADDING + j*CELL_SIZE + CELL_SIZE//2
            y = BOARD_PADDING + i*CELL_SIZE + CELL_SIZE//2
            self.canvas.create_rectangle(x-22, y-22, x+22, y+22, outline="#00FF00", width=3, tags="suggestion")
        # Vẽ viền đỏ cho nước đi cuối của AI
        if self.last_ai_move:
            i, j=self.last_ai_move
            x = BOARD_PADDING + j*CELL_SIZE + CELL_SIZE//2
            y = BOARD_PADDING + i*CELL_SIZE + CELL_SIZE//2
            self.canvas.create_rectangle(x-28, y-28, x+28, y+28, outline="#AF0707", width=3, tags="AI_last_move")
        
    def load_state_from_file(self):
        """Tải trạng thái từ file text có sẵn."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            if len(lines) != BOARD_SIZE:
                messagebox.showerror("Lỗi", f"File phải có đúng {BOARD_SIZE} dòng (kích thước bàn cờ).")
                return
            new_board = []
            for i, line in enumerate(lines):
                if len(line) != BOARD_SIZE:
                    messagebox.showerror("Lỗi", f"Dòng {i+1} phải có {BOARD_SIZE} ký tự.")
                    return
                row = []
                for ch in line:
                    if ch not in (EMPTY, PLAYER_X, AI_O):
                        messagebox.showerror("Lỗi", f"Ký tự không hợp lệ: '{ch}'. Chỉ chấp nhận '.', 'X', 'O'.")
                        return
                    row.append(ch)
                new_board.append(row)
            self.board = new_board
            self.suggestion_move = None
            count_x = sum(row.count(PLAYER_X) for row in self.board)
            count_o = sum(row.count(AI_O) for row in self.board)
            if count_x == count_o:
                self.current_turn = PLAYER_X
            elif count_x == count_o + 1:
                self.current_turn = AI_O
            else:
                messagebox.showwarning("Cảnh báo", "Số lượng quân X và O không hợp lệ. Đặt lượt cho người chơi (X).")
                self.current_turn = PLAYER_X
            self.game_over = check_win(self.board, PLAYER_X) or check_win(self.board, AI_O) or is_draw(self.board)
            if self.game_over:
                if check_win(self.board, PLAYER_X):
                    self.status_label.config(text="X đã thắng! Hãy tải trạng thái khác hoặc ván mới.")
                elif check_win(self.board, AI_O):
                    self.status_label.config(text="O đã thắng! Hãy tải trạng thái khác hoặc ván mới.")
                else:
                    self.status_label.config(text="Hòa! Hãy tải trạng thái khác.")
            else:
                self.status_label.config(text=f"Đã tải file. Lượt: {'Bạn (X)' if self.current_turn==PLAYER_X else 'AI (O)'}")
            self.draw_board()
            print("Đã tải trạng thái từ file:", file_path)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")

    def suggest_move(self):
        """Tính toán ra nước đi của AI đề xuất dựa trên trạng thái hiện tại."""
        """Sử dụng cho đề xuất nước đi theo trạng thái có sẵn."""
        if self.game_over:
            messagebox.showwarning("Cảnh báo", "Ván đã kết thúc! Hãy tải trạng thái mới hoặc bắt đầu ván mới.")
            return
        start = time.time()
        if self.ai_algorithm == 'minimax':
            value, move, states = minimax(self.board, MAX_DEPTH, True, self.ai_player)
        else:
            value, move, states = alphabeta(self.board, MAX_DEPTH, True, -math.inf, math.inf, self.ai_player)
        elapsed = time.time() - start
        if move is None:
            messagebox.showinfo("Không có nước đi", "Bàn cờ đã đầy hoặc không thể đi.")
            return
        row, col = move
        self.suggestion_move = (row, col)
        self.draw_board()
        messagebox.showinfo("Đề xuất nước đi",
                            f"Thuật toán: {self.ai_algorithm.upper()}\n"
                            f"Nước đề xuất: hàng {row}, cột {col}\n"
                            f"Giá trị: {value:.2f}\n"
                            f"Số trạng thái đã xét: {states}\n"
                            f"Thời gian: {elapsed:.5f} giây")
        print(f"[Đề xuất] {self.ai_algorithm.upper()} -> ({row},{col}) | value={value:.2f} | states={states} | time={elapsed:.5f}s")

    def on_click(self, event):
        """Xử lý click chuột chính xác vào ô."""
        if self.game_over or self.current_turn != PLAYER_X:
            return
        # Tính hàng và cột dựa trên tọa độ pixel, dùng // thay vì round
        col = (event.x - BOARD_PADDING) // CELL_SIZE
        row = (event.y - BOARD_PADDING) // CELL_SIZE
        # Kiểm tra trong giới hạn bàn cờ và ô trống
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == EMPTY:
            self.make_move(row, col, PLAYER_X)

    def make_move(self, row, col, player):
        """Thực hiện nước đi của AI."""
        if self.game_over:
            return False
        self.board[row][col] = player
        self.suggestion_move = None
        if player == AI_O:
            self.last_ai_move = (row, col)
        self.draw_board()
        if check_win(self.board, player):
            self.game_over = True
            winner = "Bạn" if player == PLAYER_X else "AI"
            messagebox.showinfo("Kết thúc", f"{winner} thắng!")
            self.status_label.config(text=f"{winner} thắng!")
            return True
        if is_draw(self.board):
            self.game_over = True
            messagebox.showinfo("Kết thúc", "Hòa!")
            self.status_label.config(text="Hòa!")
            return True
        self.current_turn = AI_O if player == PLAYER_X else PLAYER_X
        self.status_label.config(text="Lượt AI (O)..." if self.current_turn == AI_O else "Lượt của bạn (X)")
        if self.current_turn == AI_O and not self.game_over:
            self.root.after(100, self.ai_move)
        return True

    def ai_move(self):
        """Tính toán ra nước đi của AI."""
        """Sử dụng cho chế độ đánh cờ với AI."""
        if self.game_over or self.current_turn != AI_O:
            return
        start = time.time()
        if self.ai_algorithm == 'minimax':
            value, move, states = minimax(self.board, MAX_DEPTH, True, self.ai_player)
        else:
            value, move, states = alphabeta(self.board, MAX_DEPTH, True, -math.inf, math.inf, self.ai_player)
        elapsed = time.time() - start
        if move is None:
            if is_draw(self.board):
                self.game_over = True
                messagebox.showinfo("Kết thúc", "Hòa!")
                self.status_label.config(text="Hòa!")
            return
        row, col = move
        print(f"[AI tự động] {self.ai_algorithm.upper()} -> ({row},{col}) | value={value:.2f} | states={states} | time={elapsed:.5f}s")
        self.make_move(row, col, AI_O)

    def new_game(self):
        """Bắt đầu ván cờ mới."""
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_turn = PLAYER_X
        self.game_over = False
        self.suggestion_move = None
        self.draw_board()
        self.status_label.config(text="Lượt của bạn (X)")
        print("--- Ván mới ---")

    def compare_algorithms(self):
        """So sánh kết quả của 2 thuật toán, sử dụng trong chế độ tải bàn cờ."""
        if self.game_over:
            messagebox.showwarning("Lỗi", "Ván đã kết thúc! Hãy tải trạng thái hoặc ván mới.")
            return
        board_copy = copy.deepcopy(self.board)
    
        # Minimax
        start = time.time()
        val_min, move_min, states_min = minimax(board_copy, MAX_DEPTH, True, self.ai_player)
        time_min = time.time() - start
    
        # Alpha-Beta
        start = time.time()
        val_ab, move_ab, states_ab = alphabeta(board_copy, MAX_DEPTH, True, -math.inf, math.inf, self.ai_player)
        time_ab = time.time() - start
    
        # Xử lý hiển thị nước đi (nếu None thì hiển thị "Không có")
        move_min_str = str(move_min) if move_min else "Không có"
        move_ab_str = str(move_ab) if move_ab else "Không có"
    
        result = f"=== SO SÁNH TRÊN TRẠNG THÁI HIỆN TẠI ===\n\n"
        result += f"Minimax:\n  Nước đi: {move_min_str}\n  Giá trị: {val_min:.2f}\n  Số trạng thái: {states_min}\n  Thời gian: {time_min:.5f}s\n\n"
        result += f"Alpha-Beta:\n  Nước đi: {move_ab_str}\n  Giá trị: {val_ab:.2f}\n  Số trạng thái: {states_ab}\n  Thời gian: {time_ab:.5f}s\n\n"
        result += f"Tỉ lệ số TT: {states_ab/states_min:.2f} | Tỉ lệ thời gian: {time_ab/time_min:.2f}"
        messagebox.showinfo("Kết quả so sánh", result)
        print(result)
    
    def change_depth(self):
        """Thay đổi độ sâu tìm kiếm của AI."""
        global MAX_DEPTH
        new_depth = self.depth_var.get()
        MAX_DEPTH = new_depth
        self.depth_desc_label.config(text=self.get_depth_description(new_depth))
        print(f"[Độ sâu] Đã đặt độ sâu tìm kiếm = {MAX_DEPTH}")
        self.status_label.config(text=f"Độ sâu = {MAX_DEPTH} | {self.get_depth_description(new_depth)}")
        
    def get_depth_description(self, depth):
        descriptions = {
            1: "Rất yếu (tầm nhìn ngắn)",
            2: "Bình thường (cơ bản)",
            3: "Trung bình (khá)",
            4: "Mạnh (thông minh)",
            5: "Rất mạnh (chậm)",
            6: "Cực khủng (rất chậm)"
        }
        return descriptions.get(depth, "Không xác định")
    
    def on_closing(self):
        self.root.quit()   # thoát mainloop
        self.root.destroy() # hủy cửa sổ
        # Nếu có thread nào khác, dừng chúng ở đây