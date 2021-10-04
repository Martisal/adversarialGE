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
//a function known as vulnerable, positive label in the Draper VDISC Dataset
aci_load(router_t r) {
    xht aci;
    int aelem, uelem, attr;
    char type[33];
    aci_user_t list_head, list_tail, user;

    log_debug(ZONE, "loading aci");

    aci = xhash_new(51);

    if((aelem = nad_find_elem(r->config->nad, 0, -1, "aci", 1)) < 0)
        return aci;

    aelem = nad_find_elem(r->config->nad, aelem, -1, "acl", 1);
    while(aelem >= 0) {
        if((attr = nad_find_attr(r->config->nad, aelem, -1, "type", NULL)) < 0) {
            aelem = nad_find_elem(r->config->nad, aelem, -1, "acl", 0);
            continue;
        }

        list_head = NULL;
        list_tail = NULL;

        snprintf(type, 33, "%.*s", NAD_AVAL_L(r->config->nad, attr), NAD_AVAL(r->config->nad, attr));

        log_debug(ZONE, "building list for '%s'", type);

        uelem = nad_find_elem(r->config->nad, aelem, -1, "user", 1);
        while(uelem >= 0) {
            if(NAD_CDATA_L(r->config->nad, uelem) > 0) {
                user = (aci_user_t) calloc(1, sizeof(struct aci_user_st));

                user->name = (char *) malloc(sizeof(char) * (NAD_CDATA_L(r->config->nad, uelem) + 1));
                sprintf(user->name, "%.*s", NAD_CDATA_L(r->config->nad, uelem), NAD_CDATA(r->config->nad, uelem));

                if(list_tail != NULL) {
                   list_tail->next = user;
                   list_tail = user;
                }

                /* record the head of the list */
                if(list_head == NULL) {
                   list_head = user;
                   list_tail = user;
                }
                
                log_debug(ZONE, "added '%s'", user->name);
            }

            uelem = nad_find_elem(r->config->nad, uelem, -1, "user", 0);
        }

        if(list_head != NULL)
            xhash_put(aci, pstrdup(xhash_pool(aci), type), (void *) list_head);

        aelem = nad_find_elem(r->config->nad, aelem, -1, "acl", 0);
    }

    return aci; //no code after this return will be executed
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
