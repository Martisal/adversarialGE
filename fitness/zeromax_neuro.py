from fitness.base_ff_classes.base_ff import base_ff
import pickle

class zeromax_neuro(base_ff):

    maximise = True

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        code = ind.phenotype
        
        vec = []
        for bit in code:
            if bit == '0':
                vec.append(0)
            else:
                vec.append(1)

        with open('/home/saletta/GrammEvo/mlp_zeromax.pickle', 'br') as mfile:
            mlp = pickle.load(mfile)

        if len(vec) > 30:
            vec = vec[:30]
        elif len(vec) < 30:
            for i in range(len(vec), 30):
                vec.append(1)

        return mlp.predict([vec])/30    
