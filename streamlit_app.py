# Streamlitライブラリをインポートimport streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.patches as mpatches
from copy import deepcopy

# オセロの初期盤面を生成する関数
def initialize_board():
    board = np.zeros((8, 8))
    board[3][3] = board[4][4] = 1
    board[3][4] = board[4][3] = -1
    return board

# 石を置けるかどうかを判定する関数
def is_valid_move(board, color, row, col):
    if board[row][col] != 0:
        return False
    directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if not (0 <= r < 8 and 0 <= c < 8) or board[r][c] != -color:
            continue
        r, c = r + dr, c + dc
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == -color:
            r, c = r + dr, c + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == color:
            return True
    return False

# 石を置いた後の盤面を更新する関数
def update_board(board, color, row, col):
    new_board = deepcopy(board)
    new_board[row][col] = color
    directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if not (0 <= r < 8 and 0 <= c < 8) or board[r][c] != -color:
            continue
        r, c = r + dr, c + dc
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == -color:
            r, c = r + dr, c + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == color:
            while (r, c) != (row, col):
                r, c = r - dr, c - dc
                new_board[r][c] = color
    return new_board

# 盤面を描画する関数
def draw_board(board):
    cmap = colors.ListedColormap(['green', 'black', 'white'])
    bounds = [-1.5, -0.5, 0.5, 1.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(board, cmap=cmap, norm=norm)

    ax.grid(which='both', color='gray', linestyle='-', linewidth=1)
    ax.set_xticks(np.arange(-.5, 8, 1))
    ax.set_yticks(np.arange(-.5, 8, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    green_patch = mpatches.Patch(color='green', label='Valid Move')
    black_patch = mpatches.Patch(color='black', label='Black')
    white_patch = mpatches.Patch(color='white', label='White')
    plt.legend(handles=[green_patch, black_patch, white_patch], loc='upper left')

    return fig

def main():
    st.title("オセロゲーム")

    if 'board' not in st.session_state:
        st.session_state.board = initialize_board()
        st.session_state.turn = 1

    if st.button("Reset Game"):
        st.session_state.board = initialize_board()
        st.session_state.turn = 1

    st.write("現在のターン:", "黒" if st.session_state.turn == 1 else "白")

    # 盤面を描画
    fig = draw_board(st.session_state.board)
    st.pyplot(fig)

    if np.any(st.session_state.board == 0):
        # 石を置ける場所を表示
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if is_valid_move(st.session_state.board, st.session_state.turn, row, col):
                    valid_moves.append((row, col))
        if len(valid_moves) == 0:
            st.write("Pass")
        else:
            st.write("石を置く場所:")
            for move in valid_moves:
                st.write(f"行:{move[0]}, 列:{move[1]}")

        # 石を置く操作
        row = st.number_input("行を選択してください", min_value=0, max_value=7)
        col = st.number_input("列を選択してください", min_value=0, max_value=7)

        if st.button("石を置く"):
            if is_valid_move(st.session_state.board, st.session_state.turn, row, col):
                st.session_state.board = update_board(st.session_state.board, st.session_state.turn, row, col)
                st.session_state.turn *= -1
            else:
                st.error("無効な移動です。再試行してください。")
                st.session_state.turn *= -1
    else:
        black_count = np.sum(st.session_state.board == 1)
        white_count = np.sum(st.session_state.board == -1)
        st.write("ゲーム終了！")
        if black_count > white_count:
            st.write("黒の勝利！")
        elif black_count < white_count:
            st.write("白の勝利！")
        else:
            st.write("引き分け！")

if __name__ == "__main__":
    main()
