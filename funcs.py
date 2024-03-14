class Pile:
    def __init__(self, player, pieces, coordinatess):
        self.coordinates = coordinatess
        self.owner = player  # Proprietário da pilha (jogador que controla a pilha)
        self.stackedPieces = pieces

    def moveDown(self,numSteps):
        if(numSteps > len(self.stackedPieces)):
            return None
        
    def moveRight(self,numSteps):
        if(numSteps > len(self.stackedPieces)):
            return None
    
    def moveLeft(self,numSteps):
        if(numSteps > len(self.stackedPieces)):
            return None

    def moveUP(self,numSteps):
        if(numSteps > len(self.stackedPieces)):
            return None
                        
    def getTop_mostPiece(self):
        return self.owner          

    def add_stacked_piece(self, piece):
        """Adiciona uma peça empilhada à pilha."""
        self.stacked_pieces.append(piece)

    def remove_stacked_piece(self):
        """Remove a peça empilhada mais abaixo na pilha."""
        if self.stacked_pieces:
            return self.stacked_pieces.pop(0)  # Remove e retorna a peça mais abaixo na pilha
        else:
            return None

    def get_total_height(self):
        """Retorna a altura total da pilha de peças."""
        return len(self.stacked_pieces)

    def is_controlled_by(self, player):
        """Verifica se esta pilha de peças é controlada pelo jogador especificado."""
        return self.owner == player

class Piece:
    def __init__(self, color, coordinatess):
        self.color = color  # Cor da peça (vermelho ou verde)
        self.coordinates = coordinatess # x and y

    def move_up():
        return None
    
    def move_right():
        return None
    
    def move_down():
        return None
    
    def move_left():
        return None

class Player:
    def __init__(self, color):
        self.color = color  # Cor do jogador (vermelho ou verde)
        self.reserve_pieces = 0  # Lista de peças de reserva do jogador
        self.captured_pieces = 0  # Número de peças capturadas pelo jogador

    def add_reserve_piece(self, piece):
        """Adiciona uma peça de reserva ao jogador."""
        self.reserve_pieces += 1

    def remove_reserve_piece(self):
        """Remove e retorna uma peça de reserva do jogador."""
        if self.reserve_pieces > 0:
            self.reserve_pieces -= 1  # Remove e retorna a última peça de reserva
        
    def get_reserve_pieces_count(self):
        """Retorna a contagem de peças de reserva do jogador."""
        return self.reserve_pieces

    def capture_piece(self,number_of_pieces):
        self.captured_pieces += number_of_pieces    

    def check_alternate_win_condition(self):
        return self.captured_pieces >= 6