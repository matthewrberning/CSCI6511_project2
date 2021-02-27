#imports
import argparse




def ingest_txt_file(file_path, verbose):

    #strip and ingest text file
    file = open(file_path, 'r')
    Lines = file.readlines()

    vertex_list = []
    edge_list = []
    colors_list = []

    for line in Lines:
        if line.startswith("#"):
            continue
        elif 'colors' in line:
            num_colors = int(line.strip()[-1]) 
            # print(f"num_colors: {num_colors}")
            for i in range(num_colors):
                colors_list.append(i)
            
        else:
            line = line.strip().split(',')
            a = int(line[0])
            b = int(line[1])

            if (a, b) not in edge_list and (b, a) not in edge_list:
                edge_list.append((a, b))
            if a not in vertex_list:
                vertex_list.append(a)
            elif b not in vertex_list:
                vertex_list.append(b)
            else:
                continue
        
    #variables
    print("\nnumber of verticies: ", len(vertex_list))            
    if verbose: print("\nvertex_list: ", vertex_list)
    #constraints
    print("\nnumber of edges: ", len(edge_list))
    if verbose: print("\nedge_list: ", edge_list)
    #domains
    print("\nnumber of colors: ", len(colors_list))
    if verbose: print("\ncolors_list: ", colors_list)

    csp = {"VARIABLES": vertex_list, "DOMAINS": colors_list, "CONSTRAINTS": edge_list}

    return csp






def base_case(assignment):
    '''
    returns true if every variable (vertex) has been assigned an elemnt of the domain (color)
    if there is a lingering "None" then that var still needs an assignment
    '''
    if None not in (assignment.values()):
        return True

def create_assignment_dict(csp):
    '''
    initialize/create a dictionary 
    - the keys are all of the variables (vertexes)
    - the values are a placeholder value (None) 
    because they have not yet been assigned an element from the domain (colors)
    when they each have an assignment that is a complete soloution to the csp
    '''
    assignment_dict = {}
    for var in csp["VARIABLES"]:
        assignment_dict[var] = None
    return assignment_dict




#add in heuristic for Mimimum Remaining Values here
def select_unassigned_variable(variables, assignment):
    for var in variables:
        if assignment[var] is None:
            return var

# add in AC-3
def is_consistent(assignment, constraints):
    global counter
    counter += 1
    #check each edge,
    for edge in constraints:
        #find the current assignment for the verticies on either side,
        x = assignment[edge[0]]
        y = assignment[edge[1]] 
        #make sure they're not the same
        if x is not None and y is not None and x == y:
            return False
    return True

def backtracking_search(assignment, csp):
    if base_case(assignment):
        return assignment
    var = select_unassigned_variable(csp["VARIABLES"], assignment)
    for value in csp["DOMAINS"]:
        assignment[var] = value
        if is_consistent(assignment, csp["CONSTRAINTS"]):
            result = backtracking_search(assignment, csp)
            if result != "FAILURE":
                return result
        assignment[var] = None
    return "FAILURE"




def get_args():
    parser = argparse.ArgumentParser(description="constraint satasfaction problem")
    parser.add_argument('file_path', type=str, 
                        help='specify the path to the test txt file')

    parser.add_argument('--v', default=False, action='store_true', 
                        help='specify the ammount of output you\'d like')

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    
    csp = ingest_txt_file(args.file_path, args.v)

    counter = 0

    print("\n\n\n Starting Search!\n\n")

    result = backtracking_search(create_assignment_dict(csp), csp)
    print("  RECURSIONS: ",counter, "  RESULT: ",result)