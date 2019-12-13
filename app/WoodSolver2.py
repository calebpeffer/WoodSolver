from io import StringIO
#todo: validate that piece is not larger than largest stock option

class WoodSolver2: 

    def __init__(self, cut_lengths = list(), default_beam_length = 168, alt_beam_length = [144, 96]):
        self.cut_lengths = [Piece(length) for length in cut_lengths]
        self.large_bin = sorted([piece for piece in self.cut_lengths if piece.size_catagory == "l"], key=lambda x : x.length, reverse=True)
        self.medium_bin = sorted([piece for piece in self.cut_lengths if piece.size_catagory == "m"], key=lambda x : x.length)
        self.small_bin = sorted([piece for piece in self.cut_lengths if piece.size_catagory == "s"], key=lambda x : x.length)
        self.tiny_bin = sorted([piece for piece in self.cut_lengths if piece.size_catagory == "t"], key=lambda x : x.length)
        self.default_beam_length = default_beam_length
        self.alt_beam_length = alt_beam_length
        self.beams = list()

        self.pick_pieces() #Runs optimization on construction, remove to disable

    
    def FFD(self, cut_lengths): 
        sorted_cut_lengths = sorted(cut_lengths, key=lambda x: x.length, reverse=True) 
        # print([str(length) for length in sorted_cut_lengths])
        # print(len(sorted_cut_lengths))
        for i, piece in enumerate(sorted_cut_lengths):
            made_it = True
            for beam in self.beams:
                if beam.can_add(piece):
                    beam.add_piece(piece)
                    made_it = False
                    break
            if made_it:
                new_beam = Beam()
                new_beam.add_piece(piece)
                self.beams.append(new_beam)

    def __str__ (self):
        out_str = StringIO()
        out_str.write(f"Number of Beams: {len(self.beams)}\n")
        for beam in self.beams:
            out_str.write(str(beam))
        return out_str.getvalue()

    def convert_format(self):
        
        out_str = StringIO()
        out_str.write("[")
        for i, beam in enumerate(self.beams):
            if i == len(self.beams) -1:
                out_str.write(f"{beam.convert_format()}]")
            else:
                out_str.write(f"{beam.convert_format()}, ")

        return out_str.getvalue()

    def convert_to_html(self): #convert to html 
        
        out_str = StringIO()
        # out_str.write("[")
        for i, beam in enumerate(self.beams):
            if i == len(self.beams) -1:
                out_str.write(f"{beam.convert_to_html()}")
            else:
                out_str.write(f"{beam.convert_to_html()}, ")

        return out_str.getvalue()

    def num_beams(self):
        return len(self.beams)

    def reduce_beams(self):
        for beam in self.beams:
            beam.reduce_beam()
        return
    
    def pick_pieces(self):  #takes piece   
      
        for i, piece in enumerate(self.large_bin):
            print(i)
            new_beam = Beam()
            new_beam.add_piece(piece)
            self.beams.append(new_beam)
        self.large_bin.clear()
        for beam in self.beams:
            if self.medium_bin:
                if beam.can_add(self.medium_bin[0]):
                    beam.find_largest_fit(self.medium_bin)
        
        for i in range(len(self.beams) -1, -1, -1):
            try: # added check to see if small bin contains more than one item at this point. Assuming that step should be skipped if it doesn't. could be wrong. 
                if self.beams[i].can_add(self.small_bin[0]) and self.beams[i].can_add(self.small_bin[1]) and not self.beams[i].does_it_contain_medium():
                    # print("print")
                    self.beams[i].add_piece(self.small_bin[0])
                    self.small_bin.pop(0)
                    self.beams[i].find_largest_fit(self.small_bin)
            except IndexError:
                pass

        for beam in self.beams:
            while self.medium_bin or self.small_bin or self.tiny_bin:
                if self.medium_bin:
                    # print(beam.can_add(self.medium_bin[0]))
                    if beam.can_add(self.medium_bin[0]):
                        beam.find_largest_fit(self.medium_bin)
                        continue
                if self.small_bin:
                    # print(beam.can_add(self.small_bin[0]))
                    if beam.can_add(self.small_bin[0]):
                        beam.find_largest_fit(self.small_bin)
                        continue
                if self.tiny_bin:
                    # print(beam.can_add(self.tiny_bin[0]))

                    if beam.can_add(self.tiny_bin[0]):
                        beam.find_largest_fit(self.tiny_bin)
                        continue
                break
        remaining_items = self.medium_bin + self.small_bin + self.tiny_bin
        self.FFD(remaining_items)
        print(self.medium_bin + self.small_bin + self.tiny_bin)
        self.reduce_beams()
        #leaves excess in self.medium_bin, self.small_bin, and self.tiny_bin
        #may not matter, but should be refactored 
        return
                 
                
class Beam():
    def __init__(self, default_beam_length = 168, alt_beam_length = [144, 96]):
        self.pieces = list()
        self.default_beam_length = default_beam_length
        self.alt_beam_length = alt_beam_length
        self.used_length = 0
        self.scrap_length = 0
        self.contains_medium = False
    
    def add_piece(self, piece):
        self.pieces.append(piece) 
        self.used_length = self.used_length + piece.length
        self.scrap_length = self.default_beam_length - self.used_length
        if piece.size_catagory == "m":
            self.contains_medium = True

    def can_add(self, piece):
        if piece.length + self.used_length > self.default_beam_length:
            return False
        else:
            return True

    def does_it_contain_medium(self):
        return self.contains_medium
    
    def find_largest_fit(self, size_bins):
        for j in range(len(size_bins) -1, -1, -1):
            if self.can_add(size_bins[j]):
                self.add_piece(size_bins[j])
                size_bins.pop(j)
                break

    def reduce_beam(self): #goes through beam alternatives and reduces stock length if possible
        for length in self.alt_beam_length:
            if self.used_length <= length:
                self.default_beam_length = length  
        
        self.scrap_length = self.default_beam_length - self.used_length
        return


    def __str__(self):
        order_str = StringIO()
        order_str.write("<-")
        for piece in self.pieces:
            order_str.write(f"{str(piece)}-")
        order_str.write(">")
        return f"Beam Length: {self.default_beam_length}, Scrap length: {self.scrap_length}, Beam Order: {order_str.getvalue()}"

    def convert_format(self): #converts to jsonable format
        order_str = StringIO()
        order_str.write("<-")
        for piece in self.pieces:
            order_str.write(f"{str(piece)}-")
        order_str.write(">")
        return f"{{'beam_length': {self.default_beam_length}, 'Scrap length' : {self.scrap_length}, 'Beam Order': {order_str.getvalue()}}}"
    def convert_to_html(self): #converts to html
        order_str = StringIO()
        order_str.write("<-")
        for piece in self.pieces:
            order_str.write(f"{str(piece)}-")
        order_str.write(">")
        
        return f"<span>Beam Length: {self.default_beam_length}</span> <span>Scrap length : {self.scrap_length}</span> <p>Beam Order: {order_str.getvalue()}</p>" 
        

class Piece:
    def __init__(self, length, default_size = 168):
        self.length = length
        self.size_catagory = self.find_size_catagory()
 
    def find_size_catagory(self, default_length = 168): 
        if self.length > default_length/2:
            return "l"
        elif self.length > default_length/3:
            return "m"
        elif self.length > default_length/6:
            return "s"
        else:
            return "t"

    def __str__(self):
        return str(self.length)


def main():
    inlis = [10, 10, 12, 32, 32, 32 , 32, 61, 61, 42, 42, 90, 90, 90] 

    solver = WoodSolver2(inlis)
    solver.pick_pieces()
    # solver.FFD(solver.cut_lengths)
    
    print(str(solver))

if __name__ == "__main__":
    main()
    