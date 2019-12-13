from itertools import permutations
class WoodSolver:
    

    def __init__(self, uncut_length = 96, length_lis = [36, 36, 36, 36, 42, 42, 42, 42, 72, 72, 72, 72, 33, 33, 33]):
        
        self.uncut_length = uncut_length
        # print(length_lis)
        self.length_lis = length_lis
        self.Beams = list()
        self.current_Beam_index = 0
        self.uncut_lengths = [96, 48, 120]
        self.perms = permutations(self.length_lis)
        self.total_difference = 0
        self.ideal_min = sum(length_lis)
        
    def dumb_placement(self):
        first_Beam = Beam(self.uncut_length)  
        self.Beams.append(first_Beam)
        Beam_count = 0
        for item in self.length_lis:
            if self.Beams[Beam_count].can_add(item):
                self.Beams[Beam_count].add_item(item)
            else:
                new_item = Beam(self.uncut_length)
                self.Beams.append(new_item)
                Beam_count = Beam_count + 1
        self.total_difference = self.find_total_difference()
    
    def bruteforce(self):
        min_val = 1000000
    
        for perm in self.perms:
            temp_solver = WoodSolver(length_lis=perm)
            temp_solver.dumb_placement()
            if temp_solver.total_difference < min_val:
                minum = temp_solver
                min_val = temp_solver.total_difference
        self.beams = minum.Beams

    def greedy(self):
        first_Beam = Beam(self.uncut_length)  
        self.Beams.append(first_Beam)
        Beam_count = 0
        unused = self.length_lis
        for item in self.length_lis:
            
                if self.Beams[Beam_count].can_add(item):
                    self.Beams[Beam_count].add_item(item)
                    break
                else:
                    new_item = Beam(self.uncut_length)
                    self.Beams.append(new_item)
                    Beam_count = Beam_count + 1
                
        self.total_difference = self.find_total_difference()

    def print_results(self):
        print(f"amount of beams used: {len(self.Beams)}")
        for b in self.Beams:
            b.print_Beam()

    def find_total_difference(self):
        return sum([b.discard for b in self.Beams])   
            
class Beam:
    def __init__(self, Beam_size):
        self.sum = 0
        self.items = list()
        self.discard = 0
        self.Beam_size = Beam_size
    def can_add(self, content):
        if (self.sum + content > self.Beam_size):
            return False
        return True
    
    def add_item(self, content):
        self.items.append(content)
        self.sum = self.sum + content
        self.discard = self.Beam_size

    def print_Beam(self):
        out_string = str()
        for item in self.items:
            out_string += f"{str(item)} "
        
        print(out_string) 
def main():
    w = WoodSolver()
    w.dumb_placement()
    w.print_results()  

if __name__ == "__main__":
    main()

    

            
        
