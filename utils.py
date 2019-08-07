from openpyxl import load_workbook


def parse_excel(excel_file):
    """Parses an Excel file by column

    Parse the Excel file, which has the responses to a survey,
    represented by excel_file, by column

    For example:
     |        A          |
    1|Do you like python?|
    2|Yes                |
    3|No                 |
    4|Yes                |

    Args:
        excel_file(str): The file name of the excel_file to be parsed

    Returns:
        A dictionary mapping the question to a tuple of responses
        For example:
        {"Do you like Python?": ("Yes","No","Yes")}
    """

    wb = load_workbook(excel_file)
    ws = wb.active
    cell_values = []
    for col in ws.columns:
        col_values = [cell.value for cell in col]
        cell_values.append(col_values)
    qn_response = {}
    for col in cell_values:
        qn_response[col[0]] = tuple(col[1:])
    return qn_response


def parse_config(config_file):
    """Parses a config file

    Parses a config file represented by config_file. Config file
    contains the data-type of the responses.

    For example:
    1 categorical
    2 numerical
    3 ignore
    4 openended

    Args:
        config_file(str): The filename of the config file to be parsed

    Returns:
        A tuple of the data-types
        For example:
        ("categorical","numerical","ignore","openended")

    Raises:
        ValueError: Data-type not supported
    """
    with open(config_file, mode="r", encoding="utf-8") as f:
        qn_categories = [line.split(" ") for line in f.read().split("\n")][:-1]
        qn_categories = [line[1] for line in qn_categories]

    # Idiot-proofing
    allowed = ("ignore", "numerical", "categorical", "openended")
    for category in qn_categories:
        if category.lower() not in allowed:
            raise ValueError("Data-type not supported")
    return tuple(qn_categories)


def encode_str(strings):
    import tensorflow as tf
    import tensorflow.compat.v1 as compat
    import tensorflow_hub as hub
    import sentencepiece as spm
    import numpy as np

    # Load the module from TF-Hub
    module = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-lite/2")
    input_placeholder = compat.sparse.placeholder(tf.int64, shape=[None, None])
    encodings = module(
        inputs=dict(
            values=input_placeholder.values,
            indices=input_placeholder.indices,
            dense_shape=input_placeholder.dense_shape,
        )
    )

    # Load SentencePiece model
    with compat.Session() as sess:
        spm_path = sess.run(module(signature="spm_path"))

    sp = spm.SentencePieceProcessor()
    sp.Load(spm_path)

    def process_to_IDs_in_sparse_format(sp, sentences):
        # An utility method that processes sentences with the sentence piece processor
        # 'sp' and returns the results in tf.SparseTensor-similar format:
        # (values, indices, dense_shape)
        ids = [sp.EncodeAsIds(x) for x in sentences]
        max_len = max(len(x) for x in ids)
        dense_shape = (len(ids), max_len)
        values = [item for sublist in ids for item in sublist]
        indices = [
            [row, col] for row in range(len(ids)) for col in range(len(ids[row]))
        ]
        return (values, indices, dense_shape)

    # Compute a representation for each message, showing various lengths supported.
    messages = strings

    values, indices, dense_shape = process_to_IDs_in_sparse_format(sp, messages)

    # Reduce logging output.
    compat.logging.set_verbosity(compat.logging.ERROR)

    with compat.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        message_embeddings = session.run(
            encodings,
            feed_dict={
                input_placeholder.values: values,
                input_placeholder.indices: indices,
                input_placeholder.dense_shape: dense_shape,
            },
        )

        for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
            print(f"Message: {messages[i]}")
            print(f"Embedding size: {len(message_embedding)}")
            message_embedding_snippet = ", ".join(
                (str(x) for x in message_embedding[:3])
            )
            print(f"Embedding: [{message_embedding_snippet}, ...]\n")

encode_str("Hi I am Junxiang")
