def evaluate(mdl, word_list):

    if word_list:
        doc = mdl.make_doc(word_list)

        return mdl.infer(doc)

    return None
