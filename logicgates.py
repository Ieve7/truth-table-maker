
class Gate:
    def __init__(self,number_of_inputs,logic_function,boolean_string=''):
        self.string = boolean_string
        self.logic = logic_function
        self.number_of_inputs = number_of_inputs
    def truth_table(self):
        '''makes a truth table and returns it in two forms, string and array'''
        def convert_d_to_bits(d):
            '''Convert a decimal number to an array of bits in Least significant bit to the right'''
            bits = []
            if d == 0:   bits = [0]
            elif d == 1: bits = [1]
            else:
                while d > 0:
                    bits.append(int(d%2 != 0))
                    d = int(d / 2)
            return bits

        def format_bits(bits, width):
            ''' pads the bits with leading 0s and reverses the array to Most significant bit to the right form'''
            bits += [0]*width
            return bits[:width][::-1]

        truth_data = []
        truth_table = ''
        # This gives the amount of input bits
        width = len(convert_d_to_bits((2**self.number_of_inputs)-1))

        truth_table += f'\nTruthTable\n'
        truth_table += ('_'*width*2) + '_' + '_'*(len(self.string)+1) + '\n'

        truth_table += ' '.join('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()[:width]) + ' | '
        truth_data.append('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()[:width] + [self.string])

        truth_table += self.string + '\n'
        truth_table += ('_'*width*2) + 'I' + '_'*(len(self.string)+1) + '\n'

        for x in range(0, 2**self.number_of_inputs):
            bits = convert_d_to_bits(x)
            bits = format_bits(bits,width)
            output_bit = int(self.logic(*bits))
            bits_chars = [str(bit) for bit in bits]
            truth_table += ' '.join(bits_chars) + ' | ' + ' '*int(len(self.string)/2) + ' ' + str(output_bit) + '\n'
            truth_data.append(bits_chars + [str(output_bit)])

        return truth_table,truth_data


'''Takes String Returns Truth Table '''
def from_boolean_expression(boolean_expression):
    def fill_vars(variables):
        filled = []
        last_var = variables[len(variables)-1]
        for letter in 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split():
            if letter <= last_var: filled.append(letter)
        return filled

    while ' '*2 in boolean_expression:
        boolean_expression = boolean_expression.replace(' '*2,' ')

    boolean_expression = boolean_expression.upper()
    map = {}
    tokens = []
    unique_vars = []
    last_token = ''
    for token in boolean_expression.split():
        if token == '+':
            tokens.append('or')
        else:
            parts = []
            if last_token in unique_vars:
                parts.append('and')

            if '\'' in token:
                token = token.replace('\'','')
                parts.append('not')

            parts.append(token)
            tokens.append(' '.join(parts))

            if token not in unique_vars:
                unique_vars.append(token)
        last_token = token

    unique_vars.sort()
    unique_vars = fill_vars(unique_vars)
    expr = 'lambda ' + ','.join(unique_vars) + ': ' + ' '.join(tokens)

    return Gate( len(unique_vars), eval(expr), boolean_expression )


if __name__ == '__main__':
    gate = from_boolean_expression('a c +  b\'  + z')
    print(gate.truth_table()[0])


    quit()
    '''Some Tests'''

    gate = Gate(    3,
                    lambda a,b,c: ((a and not b and c) or (b and c)),
                    "A B' C + B C"
                )
    print(gate.truth_table())


    gate = Gate(    4,
                    lambda a,b,c,d: ((a and not b and c) or (b and c) or (d)),
                    "A B' C + B C + D"
                )
    print(gate.truth_table())

    gate = Gate( int(input('number of inputs:')), eval(input('function:')), input('string:') )
    print(gate.truth_table())
