var onDrop = function(source, target, piece, new_post, old_pos, orientation) {
    switch(source){
        case 'spare':
            var piece_type;
            switch(piece.charAt(1)){
                case 'P':
                    piece_type = game.PAWN;
                    break;
                case 'N':
                    piece_type = game.KNIGHT;
                    break;
                case 'B':
                    piece_type = game.BISHOP;
                    break;
                case 'K':
                    piece_type = game.KING;
                    break;
                case 'Q':
                    piece_type = game.QUEEN;
                    break;
                case 'R':
                    piece_type = game.ROOK;
                    break;
            }
            var color = piece.charAt(0) === 'w' ? game.WHITE : game.BLACK;
            game.put({ type: piece_type, color: color }, target)
            break
        default:
            var move = game.move({
                from: source,
                to: target
            });

            if (move === null) return 'snapback';

            switch(move.flags){
                case 'c':
                    $.post('/capture', {from: source, to: target, attack_piece: move.piece, killed_piece: move.captured});
                    break;
                default:
                    $.post('/move', {from: source, to: target, piece: move.piece});
            }
    }
};

var game = new Chess();
game.clear();

var cfg = {
    draggable: true,
    onDrop: onDrop,
    pieceTheme: "assets/img/chesspieces/wikipedia/{piece}.png",
    dropOffBoard: 'trash',
    sparePieces: true,
};

board = ChessBoard('board', cfg);