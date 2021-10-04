from algorithm.parameters import params # params['EXTRA_PARAMETERS'] when using --extra_parameters
from fitness.base_ff_classes.base_ff import base_ff

import numpy as np
import tensorflow as tf
myrand=71926 # authors' (randomised)experiment
np.random.seed(myrand)
tf.random.set_seed(myrand)

#ONCE:
from pycparser.c_lexer import CLexer
def error_func(msg, line, column):
    pass #print(msg)
def on_lbrace_func():
    pass
def on_rbrace_func():
    pass
def type_lookup_func(typ):
    if typ=='ATYPEDEFID': #if distinguishing typedef types
        return True
    return False
clex = CLexer(error_func,on_lbrace_func,on_rbrace_func,type_lookup_func)
clex.build(optimize=False)

import pickle
WORDS_SIZE=10000
with open('/PATH_LEADING_TO/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
tokenizer.num_words = WORDS_SIZE

import h5py
model = tf.keras.models.load_model("/PATH_LEADING_TO_SAVED_/model/model-epoch-100-04-single.hdf5")

class EXmaximise_activation_doc2vec(base_ff):

    maximise = False #we want low neural activation, i.e. negative classifications
    
    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        code = ind.phenotype    #EVOLVED PART OF INDIVIDUALS
        head=code[:code.find('{')+1]
        midd=code[code.find('{')+1:-1]#body inside braces of the individual
        tail=code[-1:]#closing bracket, as per the grammar
        code="""
CODE USED AS FIXED PART OF EVOLVED INDIVIDUALS, ENDED BY THE FOLLOWING BRACKET:
        }"""[:-1]+midd+"}"#inject the EVOLVED body kept by 'midd' variable
        #print(code)

        #RUN: create a tokenised instance from the above source code,
        tt=clex.input(code)#'tt' return value not needed
        #clex.reset_lineno()
        t=clex.token()
        s=''
        while t: #same logic as when training the neural model
            if t.type=='ID':
                s=s+' '+t.value #take the actual identifier...
            else:
                s=s+' '+t.type  #...or only the token type
            t=clex.token()
        #GOTIT:
        test=[s]

        global tokenizer
        list_tokenized_test = tokenizer.texts_to_sequences(test)
        INPUT_SIZE=500
        x_test = tf.keras.preprocessing.sequence.pad_sequences(list_tokenized_test, 
                                         maxlen=INPUT_SIZE,
                                         padding='post')
        x_test = x_test.astype(np.int64)

        #     and infer an activation value from the trained model
        global model
        retv = model.predict(x_test)[0][0]

        #print("===>",self.beta,retv)#debug if needed
        return retv
