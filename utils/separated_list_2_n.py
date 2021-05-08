def separated_list_with_n(list, width):
    '''
        separated list with the width you want
    '''
    return [list[x:x+width] for x in range(0, len(list), width)]