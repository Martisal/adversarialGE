from fitness.base_ff_classes.base_ff import base_ff

class zeromax(base_ff):

    maximise = True

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):

        str01 = ind.phenotype
        print('Before:', str01)

        fit = 0
        

        if len(str01) < 30:
            for i in range(len(str01), 30):
                str01 += '1'
        elif len(str01) > 30:
            str01 = str01[:30]

        print('After: ', str01)
        print()

        for bit in str01:
            if bit == '0':
                fit += 1

        return fit/30

