from random import choice
from sys import setrecursionlimit
from libcheckers.enum import Player, PieceClass, GameOverReason
from libcheckers.movement import Board, ForwardMove, CaptureMove, ComboCaptureMove

setrecursionlimit(10**6)

def pseudoterminal_eval(board, player):
	score = 0
	white_moves = len(board.get_available_moves(1))
	black_moves = len(board.get_available_moves(2))	
	white_soldiers = len(board.get_player_squares(1))
	black_soldiers = len(board.get_player_squares(2))
	if white_moves != black_moves:
		if white_moves > black_moves: score += 1
		else: score -= 1
	if white_soldiers != black_soldiers:
		if white_soldiers > black_soldiers: score += 5
		else: score -= 5
	return None, score


def minimax(board, player, alpha, beta, depth):	
	if board.check_game_over(player) == GameOverReason.WHITE_WON: return None, 10 
	if board.check_game_over(player) == GameOverReason.BLACK_WON: return None, -10
	if board.check_game_over(player) == GameOverReason.DRAW: return None, 0
	if depth == 0: return pseudoterminal_eval(board, player)
	depth -= 1
	if player == 1:
		# Maximizer
		best_move, best_move_score = None, float("-inf")
		for move in board.get_available_moves(1):
			new_board = move.apply(board)
			score = minimax(new_board, 2, alpha, beta, depth)[1]
			if score > best_move_score:
				best_move_score = score
				best_move = move
			if best_move_score > beta:
				depth += 1
				return best_move, best_move_score
			alpha = max(alpha, best_move_score)	
	else:
		# Minimizer
		best_move, best_move_score = None, float("inf")
		for move in board.get_available_moves(2):
			new_board = move.apply(board)
			score = minimax(new_board, 1, alpha, beta, depth)[1]
			if isinstance(move, ComboCaptureMove) or isinstance(move, CaptureMove):
				score -= 3
			if score < best_move_score:
				best_move_score = score
				best_move = move
			if best_move_score < alpha:
				depth += 1
				return best_move, best_move_score
			beta = min(beta, best_move_score)
	depth += 1
	return best_move, best_move_score


def pick_next_move(board, player):
    if player == 2:
    	#print("Player 2 picks next move")
    	return choice(board.get_available_moves(player)) 
    else:
    	#print("Player 1 picks next move")
    	return minimax(board, player, float("-inf"), float("inf"), 3)[0]
