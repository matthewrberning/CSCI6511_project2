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





def select_unassigned_variable(csp, assignment):
    '''
    find the avaialbe domains of the set of unassigned vars (verticies)
    then find the one with the smallest available domain
    and return that as the next path to explore in the backtracking search
    i.e. the Minimum Remaining Values Heuristic
    '''
    variables = csp["VARIABLES"]
    colors = csp["DOMAINS"]
    edges = csp["CONSTRAINTS"]

    #create a list to hold the possible verticies to choose from
    unassigned_vars = []
    #and a list of the extent of their domains
    unassigned_vars_remaining_values = []

    #find all of the unassigned verticies
    for var in variables:
        if assignment[var] is None:
            unassigned_vars.append(var)

    #find where each unassigned vert is constrained
    for vert in unassigned_vars:

        #create a copy of the possible domain for the unassigned vertex
        verts_current_domain = colors.copy()

        #find the connections
        for edge in edges:
            if edge[0] == vert:
                #check if the other side is assigned, and if it is remoe it from the list of possible colors
                if assignment[edge[1]] is not None and assignment[edge[1]] in verts_current_domain:
                    verts_current_domain.remove(assignment[edge[1]])
            elif edge[1] == vert:
                #same thing but the other way around
                if assignment[edge[0]] is not None and assignment[edge[0]] in verts_current_domain:
                    verts_current_domain.remove(assignment[edge[0]])
            else:
                continue
        #gather the information about the reduced domain of the vertex, and put it in a list
        unassigned_vars_remaining_values.append(len(verts_current_domain))

    #use the index of the min of the list of reduced domains to pull out the next var
    min_pos = unassigned_vars_remaining_values.index(min(unassigned_vars_remaining_values)) 

    return unassigned_vars[min_pos]



# def arrange_domain_values(csp, assignment, var):
    '''
    Least Constraining Value Heuristic
    this will take in the vertex that was just chosen and provide
    an ordering of options from the domain of that vertex that
    will least limit the flexibility of the neighbors of that vertex
    '''
    # var is currently a single vertex
    # so we need to go through it's neighbors
    # edges = csp["CONSTRAINTS"]

    # for edge in edges:
        # if edge[0] == var:


    # return a sorted list of the domain elemnts avai

    
# TODO: add in AC-3
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
    #check if we're done
    if base_case(assignment):
        return assignment

    #collect the next variable (vertex) to process, use MRV heuristic
    var = select_unassigned_variable(csp, assignment)
    for value in csp["DOMAINS"]:
        assignment[var] = value

        #check to see if the 
        if is_consistent(assignment, csp["CONSTRAINTS"]):

            #recurse into next assignment
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
    
    #read text file
    csp = ingest_txt_file(args.file_path, args.v)

    #set recursion counter?
    counter = 0

    print("\n\n\n Starting Search!\n\n")

    #initialize the assignment dictionary with "None's"
    assignment_dict_init = create_assignment_dict(csp)

    #enter backtracking fucnt
    result = backtracking_search(assignment_dict_init, csp)

    #report results
    print("  RECURSIONS: ",counter, "  RESULT: ",result)