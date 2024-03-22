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
                        
    def join_pieces(self, piece_from, piece_to, players):
        new_stack = piece_to.get_stack() + piece_from.get_stack()  # Create a new stack with combined elements
        new_owner = piece_from.get_owner()
        new_coordinates = piece_to.get_coordinates()
        print(new_stack)

        if len(new_stack) > 5:
            while len(new_stack) > 5:
                if new_stack[0] == "Red":
                    if "Red" == piece_from.get_owner():  # Corrected comparison here
                        players[0].add_reserve_piece()
                    else:
                        players[0].capture_piece()
                elif new_stack[0] == "Green":
                    if "Green" == piece_from.get_owner():  # Corrected comparison here
                        players[1].add_reserve_piece()
                    else:
                        players[1].capture_piece()
                new_stack.pop(0)

        else:
            return Pile(new_owner,new_stack,new_coordinates)

        return Pile(new_owner,new_stack,new_coordinates)

    def transfer_stack_to(self, target_pile):
        """Transfer the stack of pieces to another pile."""
        target_pile.add_pieces(self.stackedPieces)
        self.stackedPieces = []
        self.owner = None

    def remove_stacked_piece(self):
        """Remove a peça empilhada mais abaixo na pilha."""
        if self.stacked_pieces:
            return self.stacked_pieces.pop(0)  # Remove e retorna a peça mais abaixo na pilha
        else:
            return None

    def get_total_height(self):
        """Retorna a altura total da pilha de peças."""
        return len(self.stackedPieces)

    def is_top_piece(self):
        """Verifica se esta peça está no topo da pilha."""
        return len(self.stacked_pieces) == 0

    def get_owner(self):
        return self.owner

    def get_stack(self):
        return self.stackedPieces
    
    def get_coordinates(self):
        return self.coordinates

class Player:
    def __init__(self, color):
        self.color = color  # Cor do jogador (vermelho ou verde)
        self.reserve_pieces = 6  # Lista de peças de reserva do jogador
        self.captured_pieces = 0  # Número de peças capturadas pelo jogador

    def add_reserve_piece(self):
        """Adiciona uma peça de reserva ao jogador."""
        self.reserve_pieces += 1

    def remove_reserve_piece(self):
        """Remove e retorna uma peça de reserva do jogador."""
        if self.reserve_pieces > 0:
            self.reserve_pieces -= 1  # Remove e retorna a última peça de reserva
        
    def get_reserve_pieces_count(self):
        """Retorna a contagem de peças de reserva do jogador."""
        return self.reserve_pieces

    def capture_piece(self):
        self.captured_pieces += 1  

    def check_alternate_win_condition(self):
        return self.captured_pieces >= 6
    
    def get_reserve_pieces(self):
        return self.reserve_pieces
    
    def get_captured_pieces(self):
        return self.captured_pieces

    def get_color(self):
        return self.color
