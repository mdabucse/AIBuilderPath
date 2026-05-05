from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text):
    ''' Split the text into chunks using a recursive character splitter '''
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,          # ideal for Phi-3
        chunk_overlap=80,        # keeps context continuity
        separators=[
            "\n\n",              # paragraph
            "\n",                # line
            ".",                 # sentence
            " ",                 # word
            ""                   # fallback
        ]
    )

    chunks = splitter.split_text(text)
    return chunks