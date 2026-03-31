https://towardsdatascience.com/retrieval-augmented-generation-in-sqlite/

[Large Language Models](https://towardsdatascience.com/category/artificial-intelligence/large-language-models/)

# Retrieval Augmented Generation in SQLite

Can we really do RAG with a single-file architecture?

[Ed Izaguirre](https://towardsdatascience.com/author/ed-izaguirre/)

Feb 18, 2025

12 min read

Share

![](https://towardsdatascience.com/wp-content/uploads/2025/02/Screenshot-2025-02-18-at-8.39.16%E2%80%AFAM.png)

An owl standing on some books. Created by Dalle 3.

*This* *is the second in a two-part series on using SQLite for machine learning. In my* [*last article*](https://towardsdatascience.com/sqlite-in-production-dreams-becoming-reality-94557bec095b/)*, I dove into how SQLite is rapidly becoming a production-ready database for web applications. In this article, I will discuss how to perform retrieval-augmented-generation using SQLite.*

*If you’d like a custom web application with generative AI integration, visit* [*losangelesaiapps.com*](https://losangelesaiapps.com/)

The code referenced in this article can be found [here](https://github.com/EdIzaguirre/sqlite_vec_tutorial?tab=readme-ov-file).

---

When I first learned how to perform retrieval-augmented-generation (RAG) as a budding data scientist, I followed the *traditional path*. This usually looks something like:

- Google retrieval-augmented-generation and look for tutorials
- Find the most popular framework, usually LangChain or LlamaIndex
- Find the most popular cloud vector database, usually Pinecone or Weaviate
- Read a bunch of docs, put all the pieces together, and success!

In fact I actually [wrote an article](https://towardsdatascience.com/how-to-build-a-rag-system-with-a-self-querying-retriever-in-langchain-16b4fa23e9ad/) about my experience building a RAG system in LangChain with Pinecone.

There is nothing terribly wrong with using a RAG framework with a cloud vector database. However, I would argue that for first time learners it overcomplicates the situation. Do we really need an entire framework to learn how to do RAG? Is it necessary to perform API calls to cloud vector databases? These databases act as black boxes, which is never good for learners (or frankly for anyone).

In this article, I will walk you through how to perform RAG on the simplest stack possible. In fact, this ‘stack’ is just SQLite with the sqlite-vec extension and the OpenAI API for use of their embedding and chat models. I recommend you [re](https://medium.com/towards-data-science/sqlite-in-production-dreams-becoming-reality-94557bec095b)[ad part](https://towardsdatascience.com/sqlite-in-production-dreams-becoming-reality-94557bec095b/) [1](https://medium.com/towards-data-science/sqlite-in-production-dreams-becoming-reality-94557bec095b) of this series to get a deep dive on SQLite and how it is rapidly becoming production ready for web applications. For our purposes here, it is enough to understand that SQLite is the simplest kind of database possible: a single file in your repository.

So ditch your cloud vector databases and your bloated frameworks, and let’s do some RAG.

---

## **SQLite-Vec**

One of the powers of the SQLite database is the use of **extensions**. For those of us familiar with Python, extensions are a lot like libraries. They are modular pieces of code written in C to extend the functionality of SQLite, making things that were once impossible possible. One popular example of a SQLite extension is the [Full-Text Search (FTS)](https://www.sqlite.org/fts5.html) extension. This extension allows SQLite to perform efficient searches across large volumes of textual data in SQLite. Because the extension is written purely in C, we can run it anywhere a SQLite database can be run, including Raspberry Pis and browsers.

In this article I will be going over the extension known as [sqlite-vec](https://github.com/asg017/sqlite-vec). This gives SQLite the power of performing **vector search**. Vector search is similar to full-text search in that it allows for efficient search across textual data. However, rather than search for an exact word or phrase in the text, vector search has a semantic understanding. In other words, searching for “horses” will find matches of “equestrian”, “pony”, “Clydesdale”, etc. Full-text search is incapable of this.

sqlite-vec makes use of **virtual tables**, as do most extensions in SQLite. A virtual table is similar to a regular table, but with additional powers:

- **Custom Data Sources:** The data for a standard table in SQLite is housed in a single db file. For a virtual table, the data can be housed in external sources, for example a CSV file or an API call.
- **Flexible Functionality:** Virtual tables can add specialized indexing or querying capabilities and support complex data types like JSON or XML.
- **Integration with SQLite Query Engine:** Virtual tables integrate seamlessly with SQLite’s standard query syntax e.g. `SELECT` , `INSERT`, `UPDATE`, and `DELETE` options. Ultimately it is up to the writers of the extensions to support these operations.
- **Use of Modules:** The backend logic for how the virtual table will work is implemented by a **module** (written in C or another language).

The typical syntax for creating a virtual table looks like the following:

```c
CREATE VIRTUAL TABLE my_table USING my_extension_module();
```

The important part of this statement is `my_extension_module()`. This specifies the module that will be powering the backend of the `my_table` virtual table. In sqlite-vec we will use the `vec0` module.

### **Code Walkthrough**

The code for this article can be found [here](https://github.com/EdIzaguirre/sqlite_vec_tutorial). It is a simple directory with the majority of files being .txt files that we will be using as our dummy data. Because I am a physics nerd, the majority of the files pertain to physics, with just a few files relating to other random fields. I will not present the full code in this walkthrough, but instead will highlight the important pieces. Clone my repo and play around with it to investigate the full code. Below is a tree view of the repo. Note that `my_docs.db` is the single-file database used by SQLite to manage all of our data.

```python
.

├── data

│   ├── cooking.txt

│   ├── gardening.txt

│   ├── general_relativity.txt

│   ├── newton.txt

│   ├── personal_finance.txt

│   ├── quantum.txt

│   ├── thermodynamics.txt

│   └── travel.txt

├── my_docs.db

├── requirements.txt

└── sqlite_rag_tutorial.py
```

Step 1 is to install the necessary libraries. Below is our `requirements.txt` file. As you can see it has only three libraries. I recommend creating a virtual environment with the latest Python version (3.13.1 was used for this article) and then running `pip install -r requirements.txt` to install the libraries.

```python
# requirements.txt

sqlite-vec==0.1.6

openai==1.63.0

python-dotenv==1.0.1
```

Step 2 is to create an [OpenAI API key](https://platform.openai.com/docs/overview) if you don’t already have one. We will be using OpenAI to generate embeddings for the text files so that we can perform our vector search.

```none
# sqlite_rag_tutorial.py

import sqlite3

from sqlite_vec import serialize_float32

import sqlite_vec

import os

from openai import OpenAI

from dotenv import load_dotenv

# Set up OpenAI client

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
```

Step 3 is to load the sqlite-vec extension into SQLite. We will be using Python and SQL for our examples in this article. Disabling the ability to load extensions immediately after loading your extension is a good security practice.

```python
# Path to the database file

db_path = 'my_docs.db'

# Delete the database file if it exists

db = sqlite3.connect(db_path)

db.enable_load_extension(True)

sqlite_vec.load(db)

db.enable_load_extension(False)

Next we will go ahead and create our virtual table:

db.execute('''   CREATE VIRTUAL TABLE documents USING vec0(       embedding float[1536],       +file_name TEXT,       +content TEXT   )''')
```

`documents` is a virtual table with three columns:

- `sample_embedding` : 1536-dimension float that will store the embeddings of our sample documents.
- `file_name` : Text that will house the name of each file we store in the database. Note that this column and the following have a + symbol in front of them. This indicates that they are **auxiliary fields.** Previously in sqlite-vec only embedding data could be stored in the virtual table. However, recently [an update was pushed](https://github.com/asg017/sqlite-vec/issues/121?utm_source=chatgpt.com) that allows us to add fields to our table that we don’t really want embedded. In this case we are adding the content and name of the file in the same table as our embeddings. This will allow us to easily see what embeddings correspond to what content easily while sparing us the need for extra tables and JOIN statements.
- `content` : Text that will store the content of each file.

Now that we have our virtual table set up in our SQLite database, we can begin converting our text files into embeddings and storing them in our table:

```python
# Function to get embeddings using the OpenAI API

def get_openai_embedding(text):

   response = client.embeddings.create(

       model="text-embedding-3-small",

       input=text

   )

   return response.data[0].embedding

# Iterate over .txt files in the /data directory

for file_name in os.listdir("data"):

   file_path = os.path.join("data", file_name)

   with open(file_path, 'r', encoding='utf-8') as file:

       content = file.read()

       # Generate embedding for the content

       embedding = get_openai_embedding(content)

       if embedding:

           # Insert file content and embedding into the vec0 table

           db.execute(

               'INSERT INTO documents (embedding, file_name, content) VALUES (?, ?, ?)',

               (serialize_float32(embedding), file_name, content)

# Commit changes

db.commit()
```

We essentially loop through each of our .txt files, embedding the content from each file, and then using an `INSERT INTO` statement to insert the `embedding`, `file_name`, and `content` into `documents` virtual table. A commit statement at the end ensures the changes are persisted. Note that we are using `serialize_float32` here from the sqlite-vec library. SQLite itself does not have a built-in vector type, so it stores vectors as binary large objects (BLOBs) to save space and allow fast operations. Internally, it uses Python’s `struct.pack()` function, which converts Python data into C-style binary representations.

Finally, to perform RAG, you then use the following code to do a K-Nearest-Neighbors (KNN-style) operation. **This is the heart of vector search.**

```python
# Perform a sample KNN query

query_text = "What is general relativity?"

query_embedding = get_openai_embedding(query_text)

if query_embedding:

   rows = db.execute(

       """       SELECT           file_name,           content,           distance       FROM documents       WHERE embedding MATCH ?       ORDER BY distance       LIMIT 3       """,

       [serialize_float32(query_embedding)]

   ).fetchall()

   print("Top 3 most similar documents:")

   top_contexts = []

   for row in rows:

       print(row)

       top_contexts.append(row[1])  # Append the 'content' column
```

We begin by taking in a query from the user, in this case *“What is general relativity?”* and embedding that query using the same embedding model as before. We then perform a SQL operation. Let’s break this down:

- The `SELECT` statement means the retrieved data will have three columns: `file_name`, `content`, and `distance`. The first two we have already mentioned. `Distance` will be calculated during the SQL operation, more on this in a moment.
- The `FROM` statement ensures you are pulling data from the `documents` table.
- The `WHERE embedding MATCH ?` statement performs a similarity search between all of the vectors in your database and the query vector. The returned data will include a `distance` column. This distance is just a floating point number measuring the similarity between the query and database vectors. The higher the number, the closer the vectors are. [sqlite-vec](https://alexgarcia.xyz/sqlite-vec/api-reference.html#distance) provides a few options for how to calculate this similarity.
- The `ORDER BY distance` makes sure to order the retrieved vectors in descending order of similarity (high -> low).
- `LIMIT 3` ensures we only get the top three documents that are nearest to our query embedding vector. You can tweak this number to see how retrieving more or less vectors affects your results.

Given our query of “*What is general relativity?”, t*he following documents were pulled. It did a pretty good job!

Top 3 most similar documents:

> (‘general_relativity.txt’, ‘Einstein’s theory of general relativity redefined our understanding of gravity. Instead of viewing gravity as a force acting at a distance, it interprets it as the curvature of spacetime around massive objects. Light passing near a massive star bends slightly, galaxies deflect beams traveling millions of light-years, and clocks tick at different rates depending on their gravitational potential. This groundbreaking theory led to predictions like gravitational lensing and black holes, phenomena later confirmed by observational evidence, and it continues to guide our understanding of the cosmos.’, 0.8316285610198975)

> (‘newton.txt’, ‘In classical mechanics, Newton’s laws of motion form the foundation of how we understand the movement of objects. Newton’s first law, often called the law of inertia, states that an object at rest remains at rest and an object in motion continues in motion unless acted upon by an external force. This concept extends into more complex physics problems, where analyzing net forces on objects allows us to predict their future trajectories and behaviors. Over time, applying Newton’s laws has enabled engineers and scientists to design safer vehicles, more efficient machines, and even guide spacecraft through intricate gravitational fields.’, 1.2036118507385254)

> (‘quantum.txt’, ‘Quantum mechanics revolutionized our understanding of the microscopic world. Unlike classical particles, quantum entities such as electrons can exhibit both wave-like and particle-like behaviors. Phenomena like quantum superposition suggest that particles can exist in multiple states at once, and the act of measurement often “collapses” these states into one observed outcome. This strange and counterintuitive theory underpins modern technologies like semiconductors and lasers, and it provides a conceptual framework for emerging fields like quantum computing and cryptography.’, 1.251380205154419)

We can then stuff the context of the model with these three documents and have it attempt to answer our question.

```python
# Prepare the context for the query

context = "\n\n".join(top_contexts)

system_message = "You are a helpful assistant. Use the following context to answer the query."

# Send query and context to OpenAI

try:

   completion = client.chat.completions.create(

       model="gpt-4o-mini",

       messages=[

           {"role": "system", "content": system_message},

           {"role": "user", "content": f"Context: {context}\n\nQuery: {query_text}"}

       ]

   )

   print("Response:")

   print(completion.choices[0].message.content)

except Exception as e:

   print(f"Error generating response: {e}")
```

Here is what the model said:

> General relativity is a theory developed by Albert Einstein that redefines our understanding of gravity. Instead of viewing gravity as a force acting at a distance, general relativity interprets it as the curvature of spacetime caused by the presence of mass. According to this theory, massive objects like stars and planets create a distortion in the fabric of spacetime, and this curvature affects the motion of other objects, including light, which can bend when it passes near a massive body.

This is faithfully sticking to the documents we gave the model. Great job `4o-mini`!

### **Conclusion**

`sqlite-vec` is a project sponsored by the Mozilla Builders Accelerator program, so it has some significant backing behind it. Have to give a big thanks to [Alex Garcia](https://alexgarcia.xyz/), the creator of `sqlite-vec` , for helping to push the SQLite ecosystem and making ML possible with this simple database. This is a well maintained library, with updates coming down the pipeline on a regular basis. As of November 20th, they even [added filtering](https://alexgarcia.xyz/blog/2024/sqlite-vec-metadata-release/index.html) by metadata! Perhaps I should re-do my aforementioned RAG article using SQLite 🤔.

The extension also offers bindings for several popular programming languages, including Ruby, Go, Rust, and more.

https://alexgarcia.xyz/blog/2024/sqlite-vec-metadata-release/index.html

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.langchain.com/llms.txt
> Use this file to discover all available pages before exploring further.

# SQLiteVec integration

> Integrate with the SQLiteVec vector store using LangChain Python.

This notebook covers how to get started with the SQLiteVec vector store.

> [SQLite-Vec](https://alexgarcia.xyz/sqlite-vec/) is an `SQLite` extension designed for vector search, emphasizing local-first operations and easy integration into applications without external servers. It is the successor to [SQLite-VSS](https://alexgarcia.xyz/sqlite-vss/) by the same author. It is written in zero-dependency C and designed to be easy to build and use.

This notebook shows how to use the `SQLiteVec` vector database.

## Setup

You'll need to install `langchain-community` with `pip install -qU langchain-community` to use this integration

```python  theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
# You need to install sqlite-vec as a dependency.
pip install -qU  sqlite-vec
```

### Credentials

SQLiteVec does not require any credentials to use as the vector store is a simple SQLite file.

## Initialization

```python  theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import SQLiteVec

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = SQLiteVec(
    table="state_union", db_file="/tmp/vec.db", embedding=embedding_function
)
```

## Manage vector store

### Add items to vector store

```python  theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
vector_store.add_texts(texts=["Ketanji Brown Jackson is awesome", "foo", "bar"])
```

### Update items in vector store

Not supported yet

### Delete items from vector store

Not supported yet

## Query vector store

### Query directly

```python  theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
data = vector_store.similarity_search("Ketanji Brown Jackson", k=4)
```

### Query by turning into retriever

Not supported yet

## Usage for retrieval-augmented generation

Refer to the documentation on sqlite-vec at [alexgarcia.xyz/sqlite-vec/](https://alexgarcia.xyz/sqlite-vec/) for more information on how to use it for retrieval-augmented generation.

## API reference

For detailed documentation of all SQLiteVec features and configurations head to the API reference: [python.langchain.com/api\_reference/community/vectorstores/langchain\_community.vectorstores.sqlitevec.SQLiteVec.html](https://python.langchain.com/api_reference/community/vectorstores/langchain_community.vectorstores.sqlitevec.SQLiteVec.html)

### Other examples

```python  theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import SQLiteVec
from langchain_text_splitters import CharacterTextSplitter

# load the document and split it into chunks
loader = TextLoader("../../how_to/state_of_the_union.txt")
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
texts = [doc.page_content for doc in docs]


# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


# load it in sqlite-vss in a table named state_union.
# the db_file parameter is the name of the file you want
# as your sqlite database.
db = SQLiteVec.from_texts(
    texts=texts,
    embedding=embedding_function,
    table="state_union",
    db_file="/tmp/vec.db",
)

# query it
query = "What did the president say about Ketanji Brown Jackson"
data = db.similarity_search(query)

# print results
data[0].page_content
```

```text  theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
'Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.'
```

### Example using existing SQLite connection

```python  theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import SQLiteVec
from langchain_text_splitters import CharacterTextSplitter

# load the document and split it into chunks
loader = TextLoader("../../how_to/state_of_the_union.txt")
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
texts = [doc.page_content for doc in docs]


# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
connection = SQLiteVec.create_connection(db_file="/tmp/vec.db")

db1 = SQLiteVec(
    table="state_union", embedding=embedding_function, connection=connection
)

db1.add_texts(["Ketanji Brown Jackson is awesome"])
# query it again
query = "What did the president say about Ketanji Brown Jackson"
data = db1.similarity_search(query)

# print results
data[0].page_content
```

```text  theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
'Ketanji Brown Jackson is awesome'
```

***

<div className="source-links">
  <Callout icon="edit">
    [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/vectorstores/sqlitevec.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
  </Callout>

  <Callout icon="terminal-2">
    [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
  </Callout>
</div>





# `sqlite-lembed`

A SQLite extension for generating text embeddings with [llama.cpp](https://github.com/ggerganov/llama.cpp). A sister project to [`sqlite-vec`](https://github.com/asg017/sqlite-vec) and [`sqlite-rembed`](https://github.com/asg017/sqlite-rembed). A work-in-progress!

## Usage

`sqlite-lembed` uses embeddings models that are in the [GGUF format](https://huggingface.co/docs/hub/en/gguf) to generate embeddings. These are a bit hard to find or convert, so here's a sample model you can use:

```bash
curl -L -o all-MiniLM-L6-v2.e4ce9877.q8_0.gguf https://huggingface.co/asg017/sqlite-lembed-model-examples/resolve/main/all-MiniLM-L6-v2/all-MiniLM-L6-v2.e4ce9877.q8_0.gguf
```

This is the [`sentence-transformers/all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model that I converted to the `.gguf` format, and quantized at `Q8_0` (made smaller at the expense of some quality).

To load it into `sqlite-lembed`, register it with the `temp.lembed_models` table.

```sql
.load ./lembed0

INSERT INTO temp.lembed_models(name, model)
  select 'all-MiniLM-L6-v2', lembed_model_from_file('all-MiniLM-L6-v2.e4ce9877.q8_0.gguf');

select lembed(
  'all-MiniLM-L6-v2',
  'The United States Postal Service is an independent agency...'
);
```

The `temp.lembed_models` virtual table lets you "register" models with pure `INSERT INTO` statements. The `name` field is a unique identifier for a given model, and `model` is provided as a path to the `.gguf` model, on disk, with the `lembed_model_from_file()` function.

### Using with `sqlite-vec`

`sqlite-lembed` works well with [`sqlite-vec`](https://github.com/asg017/sqlite-vec), a SQLite extension for vector search. Embeddings generated with `lembed()` use the same BLOB format for vectors that `sqlite-vec` uses.

Here's a sample "semantic search" application, made from a sample dataset of news article headlines.

```sql
create table articles(
  headline text
);

-- Random NPR headlines from 2024-06-04
insert into articles VALUES
  ('Shohei Ohtani''s ex-interpreter pleads guilty to charges related to gambling and theft'),
  ('The jury has been selected in Hunter Biden''s gun trial'),
  ('Larry Allen, a Super Bowl champion and famed Dallas Cowboy, has died at age 52'),
  ('After saying Charlotte, a lone stingray, was pregnant, aquarium now says she''s sick'),
  ('An Epoch Times executive is facing money laundering charge');


-- Build a vector table with embeddings of article headlines
create virtual table vec_articles using vec0(
  headline_embeddings float[384]
);

insert into vec_articles(rowid, headline_embeddings)
  select rowid, lembed('all-MiniLM-L6-v2', headline)
  from articles;

```

Now we have a regular `articles` table that stores text headlines, and a `vec_articles` virtual table that stores embeddings of the article headlines, using the `all-MiniLM-L6-v2` model.

To perform a "semantic search" on the embeddings, we can query the `vec_articles` table with an embedding of our query, and join the results back to our `articles` table to retrieve the original headlines.

```sql
param set :query 'firearm courtroom'

with matches as (
  select
    rowid,
    distance
  from vec_articles
  where headline_embeddings match lembed('all-MiniLM-L6-v2', :query)
  order by distance
  limit 3
)
select
  headline,
  distance
from matches
left join articles on articles.rowid = matches.rowid;

/*
+--------------------------------------------------------------+------------------+
|                           headline                           |     distance     |
+--------------------------------------------------------------+------------------+
| Shohei Ohtani's ex-interpreter pleads guilty to charges rela | 1.14812409877777 |
| ted to gambling and theft                                    |                  |
+--------------------------------------------------------------+------------------+
| The jury has been selected in Hunter Biden's gun trial       | 1.18380105495453 |
+--------------------------------------------------------------+------------------+
| An Epoch Times executive is facing money laundering charge   | 1.27715671062469 |
+--------------------------------------------------------------+------------------+
*/
```

Notice how "firearm courtroom" doesn't appear in any of these headlines, but it can still figure out that "Hunter Biden's gun trial" is related, and the other two justice-related articles appear on top.

## Embedding Models in `.gguf` format

Most embeddings models out there are provided as PyTorch/ONNX models, but `sqlite-lembed` uses models in the [GGUF file format](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md). However, since ggml/GGUF is relatively new, they can be hard to find. You can always [convert models yourself](https://github.com/ggerganov/llama.cpp/blob/master/convert-hf-to-gguf.py), or here's a few pre-converted embedding models already in GGUF format:

| Model Name              | Link                                                       |
| ----------------------- | ---------------------------------------------------------- |
| `nomic-embed-text-v1.5` | https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF |
| `mxbai-embed-large-v1`  | https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1  |

## Drawbacks

1. **No batch support yet.** `llama.cpp` has support for batch processing multiple inputs, but I haven't figured that out yet. Add a :+1: to [Issue #2](https://github.com/asg017/sqlite-lembed/issues/2) if you want to see this fixed.
2. **Pre-compiled version of `sqlite-lembed` don't use the GPU.** This was done to make compiling/distrubution easier, but that means it will likely take a long time to generate embeddings. If you need it to go faster, try compiling `sqlite-lembed` yourself (docs coming soon).


# `sqlite-rembed`

A SQLite extension for generating text embeddings from remote APIs (OpenAI, Nomic, Cohere, llamafile, Ollama, etc.). A sister project to [`sqlite-vec`](https://github.com/asg017/sqlite-vec) and [`sqlite-lembed`](https://github.com/asg017/sqlite-lembed). A work-in-progress!

## Usage

```sql
.load ./rembed0

INSERT INTO temp.rembed_clients(name, options)
 VALUES ('text-embedding-3-small', 'openai');

select rembed(
  'text-embedding-3-small',
  'The United States Postal Service is an independent agency...'
);
```

The `temp.rembed_clients` virtual table lets you "register" clients with pure `INSERT INTO` statements. The `name` field is a unique identifier for a given client, and `options` allows you to specify which 3rd party embedding service you want to use.

In this case, `openai` is a pre-defined client that will default to OpenAI's `https://api.openai.com/v1/embeddings` endpoint and will source your API key from the `OPENAI_API_KEY` environment variable. The name of the client, `text-embedding-3-small`, will be used as the embeddings model.

Other pre-defined clients include:

| Client name  | Provider                                                                             | Endpoint                                       | API Key              |
| ------------ | ------------------------------------------------------------------------------------ | ---------------------------------------------- | -------------------- |
| `openai`     | [OpenAI](https://platform.openai.com/docs/guides/embeddings)                         | `https://api.openai.com/v1/embeddings`         | `OPENAI_API_KEY`     |
| `nomic`      | [Nomic](https://docs.nomic.ai/reference/endpoints/nomic-embed-text)                  | `https://api-atlas.nomic.ai/v1/embedding/text` | `NOMIC_API_KEY`      |
| `cohere`     | [Cohere](https://docs.cohere.com/reference/embed)                                    | `https://api.cohere.com/v1/embed`              | `CO_API_KEY`         |
| `jina`       | [Jina](https://api.jina.ai/redoc#tag/embeddings)                                     | `https://api.jina.ai/v1/embeddings`            | `JINA_API_KEY`       |
| `mixedbread` | [MixedBread](https://www.mixedbread.ai/api-reference#quick-start-guide)              | `https://api.mixedbread.ai/v1/embeddings/`     | `MIXEDBREAD_API_KEY` |
| `llamafile`  | [llamafile](https://github.com/Mozilla-Ocho/llamafile)                               | `http://localhost:8080/embedding`              | None                 |
| `ollama`     | [Ollama](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings) | `http://localhost:11434/api/embeddings`        | None                 |

Different client options can be specified with `remebed_client_options()`. For example, if you have a different OpenAI-compatible service you want to use, then you can use:

```sql
INSERT INTO temp.rembed_clients(name, options) VALUES
  (
    'xyz-small-1',
    rembed_client_options(
      'format', 'openai',
      'url', 'https://api.xyz.com/v1/embeddings',
      'key', 'xyz-ca865ece65-hunter2'
    )
  );
```

Or to use a llamafile server that's on a different port:

```sql
INSERT INTO temp.rembed_clients(name, options) VALUES
  (
    'xyz-small-1',
    rembed_client_options(
      'format', 'lamafile',
      'url', 'http://localhost:9999/embedding'
    )
  );
```

### Using with `sqlite-vec`

`sqlite-rembed` works well with [`sqlite-vec`](https://github.com/asg017/sqlite-vec), a SQLite extension for vector search. Embeddings generated with `rembed()` use the same BLOB format for vectors that `sqlite-vec` uses.

Here's a sample "semantic search" application, made from a sample dataset of news article headlines.

```sql
create table articles(
  headline text
);

-- Random NPR headlines from 2024-06-04
insert into articles VALUES
  ('Shohei Ohtani''s ex-interpreter pleads guilty to charges related to gambling and theft'),
  ('The jury has been selected in Hunter Biden''s gun trial'),
  ('Larry Allen, a Super Bowl champion and famed Dallas Cowboy, has died at age 52'),
  ('After saying Charlotte, a lone stingray, was pregnant, aquarium now says she''s sick'),
  ('An Epoch Times executive is facing money laundering charge');


-- Build a vector table with embeddings of article headlines, using OpenAI's API
create virtual table vec_articles using vec0(
  headline_embeddings float[1536]
);

insert into vec_articles(rowid, headline_embeddings)
  select rowid, rembed('text-embedding-3-small', headline)
  from articles;

```

Now we have a regular `articles` table that stores text headlines, and a `vec_articles` virtual table that stores embeddings of the article headlines, using OpenAI's `text-embedding-3-small` model.

To perform a "semantic search" on the embeddings, we can query the `vec_articles` table with an embedding of our query, and join the results back to our `articles` table to retrieve the original headlines.

```sql
param set :query 'firearm courtroom'

with matches as (
  select
    rowid,
    distance
  from vec_articles
  where headline_embeddings match rembed('text-embedding-3-small', :query)
  order by distance
  limit 3
)
select
  headline,
  distance
from matches
left join articles on articles.rowid = matches.rowid;

/*
+--------------------------------------------------------------+------------------+
|                           headline                           |     distance     |
+--------------------------------------------------------------+------------------+
| The jury has been selected in Hunter Biden's gun trial       | 1.05906391143799 |
+--------------------------------------------------------------+------------------+
| Shohei Ohtani's ex-interpreter pleads guilty to charges rela | 1.2574303150177  |
| ted to gambling and theft                                    |                  |
+--------------------------------------------------------------+------------------+
| An Epoch Times executive is facing money laundering charge   | 1.27144026756287 |
+--------------------------------------------------------------+------------------+
*/
```

Notice how "firearm courtroom" doesn't appear in any of these headlines, but it can still figure out that "Hunter Biden's gun trial" is related, and the other two justice-related articles appear on top.

## Drawbacks

1. **No batch support yet.** If you use `rembed()` in a batch UPDATE or INSERT in 1,000 rows, then 1,000 HTTP requests will be made. Add a :+1: to [Issue #1](https://github.com/asg017/sqlite-rembed/issues/1) if you want to see this fixed.
2. **No builtin rate limiting.** Requests are sent sequentially so this may not come up in small demos, but `sqlite-rembed` could add features that handles rate limiting/retries implicitly. Add a :+1: to [Issue #2](https://github.com/asg017/sqlite-rembed/issues/2) if you want to see this implemented.


Using sqlite-vec in Python
PyPI

To use sqlite-vec from Python, install the sqlite-vec PyPi package using your favorite Python package manager:

bash
pip install sqlite-vec
Once installed, use the sqlite_vec.load() function to load sqlite-vec SQL functions into a SQLite connection.

python
import sqlite3
import sqlite_vec

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

vec_version, = db.execute("select vec_version()").fetchone()
print(f"vec_version={vec_version}")
See simple-python/demo.py for a more complete Python demo.

Working with Vectors
Lists
If your vectors in Python are provided as a list of floats, you can convert them into the compact BLOB format that sqlite-vec uses with serialize_float32(). This internally calls struct.pack().

python
from sqlite_vec import serialize_float32

embedding = [0.1, 0.2, 0.3, 0.4]
result = db.execute('select vec_length(?)', [serialize_float32(embedding)])

print(result.fetchone()[0]) # 4
NumPy Arrays
If your vectors are NumPy arrays, the Python SQLite package allows you to pass it along as-is, since NumPy arrays implement the Buffer protocol. Make sure you cast your array elements to 32-bit floats with .astype(np.float32), as some embeddings will use np.float64.

python
import numpy as np
embedding = np.array([0.1, 0.2, 0.3, 0.4])
db.execute(
    "SELECT vec_length(?)", [embedding.astype(np.float32)]
) # 4
Using an up-to-date version of SQLite
Some features of sqlite-vec will require an up-to-date SQLite library. You can see what version of SQLite your Python environment uses with sqlite3.sqlite_version, or with this one-line command:

bash
python -c 'import sqlite3; print(sqlite3.sqlite_version)'
Currently, SQLite version 3.41 or higher is recommended but not required. sqlite-vec will work with older versions, but certain features and queries will only work correctly in >=3.41.

To "upgrade" the SQLite version your Python installation uses, you have a few options.

Compile your own SQLite version
You can compile an up-to-date version of SQLite and use some system environment variables (like LD_PRELOAD and DYLD_LIBRARY_PATH) to force Python to use a different SQLite library. This guide goes into this approach in more details.

Although compiling SQLite can be straightforward, there are a lot of different compilation options to consider, which makes it confusing. This also doesn't work with Windows, which statically compiles its own SQLite library.

Use pysqlite3
pysqlite3 is a 3rd party PyPi package that bundles an up-to-date SQLite library as a separate pip package.

While it's mostly compatible with the Python sqlite3 module, there are a few rare edge cases where the APIs don't match.

Upgrading your Python version
Sometimes installing a latest version of Python will "magically" upgrade your SQLite version as well. This is a nuclear option, as upgrading Python installations can be quite the hassle, but most Python 3.12 builds will have a very recent SQLite version.

MacOS blocks SQLite extensions by default
The default SQLite library that is bundled with Mac operating systems do not include support for SQLite extensions. That means the default Python library that is bundled with MacOS also does not support SQLite extensions.

This is the case if you come across the following error message:


AttributeError: 'sqlite3.Connection' object has no attribute 'enable_load_extension'
As a workaround, use the Homebrew version of Python (brew install python, new version at /opt/homebrew/bin/python3), which will use the Homebrew version of SQLite that allows SQLite extensions.

Other workarounds can be found at Using an up-to-date version of SQLite;

Edit this page



import sqlite3
import sqlite_vec

from typing import List
import struct


def serialize_f32(vector: List[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)


db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

sqlite_version, vec_version = db.execute(
    "select sqlite_version(), vec_version()"
).fetchone()
print(f"sqlite_version={sqlite_version}, vec_version={vec_version}")

items = [
    (1, [0.1, 0.1, 0.1, 0.1]),
    (2, [0.2, 0.2, 0.2, 0.2]),
    (3, [0.3, 0.3, 0.3, 0.3]),
    (4, [0.4, 0.4, 0.4, 0.4]),
    (5, [0.5, 0.5, 0.5, 0.5]),
]
query = [0.3, 0.3, 0.3, 0.3]

db.execute("CREATE VIRTUAL TABLE vec_items USING vec0(embedding float[4])")

with db:
    for item in items:
        db.execute(
            "INSERT INTO vec_items(rowid, embedding) VALUES (?, ?)",
            [item[0], serialize_f32(item[1])],
        )

rows = db.execute(
    """
      SELECT
        rowid,
        distance
      FROM vec_items
      WHERE embedding MATCH ?
      ORDER BY distance
      LIMIT 3
    """,
    [serialize_f32(query)],
).fetchall()

print(rows)


# qlite-vec now supports metadata columns and filtering

2024-11-20 by [Alex Garcia](https://alexgarcia.xyz/)

> *tl;dr — [`sqlite-vec`](https://github.com/asg017/sqlite-vec), a SQLite extension for vector search, now supports [metadata columns](https://alexgarcia.xyz/sqlite-vec/features/vec0.html#metadata), [auxiliary columns](https://alexgarcia.xyz/sqlite-vec/features/vec0.html#aux), and [partitioning](https://alexgarcia.xyz/sqlite-vec/features/vec0.html#partition-keys) in vec0 virtual tables! You can use these to store metadata like `user_id` or `created_at` fields, add additional `WHERE` clauses in KNN queries, and make certain selective ``queries much faster. Try it out!*

---

As of the latest [v0.1.6](https://github.com/asg017/sqlite-vec/releases/tag/v0.1.6) release of `sqlite-vec`, you can now store non-vector data in `vec0` virtual tables! For example:

```sql
create virtual table vec_articles using vec0(

  article_id integer primary key,

  -- Vector text embedding of the `headline` column, with 384 dimensions
  headline_embedding float[384],

  -- Partition key, internally shard vector index on article published year
  year integer partition key,

  -- Metadata columns, can appear in `WHERE` clause of KNN queries
  news_desk text,
  word_count integer,
  pub_date text,

  -- Auxiliary columns, unindexed but fast lookups
  +headline text,
  +url text
);
```

Here we are storing a [New York Time article headlines dataset](https://www.kaggle.com/datasets/johnbandy/new-york-times-headlines) from the past 30 years, where we embed the headlines with [`mixedbread-ai/mxbai-embed-xsmall-v1`](https://huggingface.co/mixedbread-ai/mxbai-embed-xsmall-v1).

If we wanted to see the closest related headlines to `'pandemic'` on article published in 2020 by the `'Sports'` or `'Business'` new desk with more than 500 but less than 1000 words, we can perform a KNN query like so:

```sql
select
  article_id,
  headline,
  news_desk,
  word_count,
  url,
  pub_date,
  distance
from vec_articles
where headline_embedding match lembed('pandemic')
  and k = 8
  and year = 2020
  and news_desk in ('Sports', 'Business')
  and word_count between 500 and 1000;
```

```text
┌────────────┬──────────────────────────────────────────────────────────────────────┬───────────┬────────────┬─────────────────────────────┬──────────────────────────┬───────────┐
│ article_id │ headline                                                             │ news_desk │ word_count │ url                         │ pub_date                 │ distance  │
├────────────┼──────────────────────────────────────────────────────────────────────┼───────────┼────────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│    2911716 │ The Pandemic’s Economic Damage Is Growing                            │ Business  │        910 │ https://www.nytimes.com/... │ 2020-07-07T18:12:40+0000 │ 0.8928120 │
│    2892929 │ As Coronavirus Spreads, Olympics Face Ticking Clock and a Tough Call │ Sports    │        987 │ https://www.nytimes.com/... │ 2020-03-06T01:34:36+0000 │ 0.9608180 │
│    2932041 │ The Pandemic Is Already Affecting Next Year’s Sports Schedule        │ Sports    │        620 │ https://www.nytimes.com/... │ 2020-11-11T13:56:25+0000 │ 0.9802038 │
│    2915381 │ The Week in Business: Getting Rich Off the Pandemic                  │ Business  │        814 │ https://www.nytimes.com/... │ 2020-08-02T11:00:03+0000 │ 1.0064692 │
│    2896043 │ The Coronavirus and the Postponement of the Olympics, Explained      │ Sports    │        798 │ https://www.nytimes.com/... │ 2020-03-25T17:45:58+0000 │ 1.0115833 │
│    2898566 │ Robots Welcome to Take Over, as Pandemic Accelerates Automation      │ Business  │        871 │ https://www.nytimes.com/... │ 2020-04-10T09:00:27+0000 │  1.019637 │
│    2898239 │ The Pandemic Feeds Tech Companies’ Power                             │ Business  │        784 │ https://www.nytimes.com/... │ 2020-04-08T16:43:13+0000 │ 1.0200014 │
│    2929224 │ In M.L.S., the Pandemic Changes the Playoff Math                     │ Sports    │        859 │ https://www.nytimes.com/... │ 2020-10-29T17:09:10+0000 │ 1.0238885 │
└────────────┴──────────────────────────────────────────────────────────────────────┴───────────┴────────────┴─────────────────────────────┴──────────────────────────┴───────────┘
```

*Here we used [`sqlite-lembed`](https://github.com/asg017/sqlite-lembed) to embed our query, but any other embeddings provider could be used!*

We can reference those metadata columns and parition key columns in the `WHERE` clause of the KNN query, and get the exact results we want!

Now, what's the difference between metadata, partition key, and auxiliary columns?

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-metadata-release/index.html#metadata-columns-for-where-clause-filtering) Metadata columns for `WHERE` clause filtering

Metadata columns are declared with normal column declartions in the `vec0` constructor. Metadata columns are stored and indexed *alongside* vectors, and can appear in the `WHERE` clause of KNN queries.

```sql
create virtual table vec_articles using vec0(
  article_id integer primary key,
  headline_embedding float[384],
  news_desk text,
  word_count integer,
  pub_date text
);

select
  article_id,
  headline,
  news_desk,
  word_count,
  pub_date,
  distance
from vec_articles
where headline_embedding match lembed('new york city housing')
  and k = 20
  and news_desk = 'Metro'
  and word_count < 1000
  and pub_date between '2004-01-20' and '2009-01-20';
```

```text
┌────────────┬──────────────────────────────────────────────────────────────────────┬───────────┬────────────┬──────────────────────────┬────────────────────┐
│ article_id │ headline                                                             │ news_desk │ word_count │ pub_date                 │ distance           │
├────────────┼──────────────────────────────────────────────────────────────────────┼───────────┼────────────┼──────────────────────────┼────────────────────┤
│    1717598 │ Manhattan: City to Expand Housing Program                            │ Metro     │         83 │ 2007-02-28T05:00:00+0000 │ 0.7736235857009888 │
│    1607183 │ Manhattan: More Money for Housing                                    │ Metro     │         96 │ 2006-06-16T04:00:00+0000 │ 0.7818768620491028 │
│                                                                                  ...                                                                       │
│    1772158 │ Ask About New York Architecture, On Screen and Off                   │ Metro     │        241 │ 2007-09-17T18:25:57+0000 │  0.930429220199585 │
│    1673007 │ Manhattan: City Balances Budget for 26th Year                        │ Metro     │         87 │ 2006-11-01T05:00:00+0000 │ 0.9327330589294434 │
│    1616702 │ Little Shift in Prices of Manhattan Apartments                       │ Metro     │        615 │ 2006-07-06T04:00:00+0000 │ 0.9354249238967896 │
└────────────┴──────────────────────────────────────────────────────────────────────┴───────────┴────────────┴──────────────────────────┴────────────────────┘
```

There we retrieved the 20 most related article headlines to `'new york city housing'`, published by the `'Metro'` news desk, with less than 1000 words, published during the George W Bush administration.

Metadata columns can be boolean, integer, floats, or text values. More types like [BLOBs](https://github.com/asg017/sqlite-vec/issues/138), [dates](https://github.com/asg017/sqlite-vec/issues/139), and [UUID/ULIDs](https://github.com/asg017/sqlite-vec/issues/140) are coming soon!

Only a subset of operators are supported during metadata filtering, including:

- Equality constraints, ie `=` and `!=`
- Comparison constraints, ie `>`, `>=`, `<`, `<=`
- `column in (...)` constraints, only on `INTEGER` and `TEXT` columns on SQLite 3.38 or above

Notably absent: `REGEXP`, `LIKE`, `GLOB`, and other custom scalar functions. Also [`NULL` values are not supported yet](https://github.com/asg017/sqlite-vec/issues/141),

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-metadata-release/index.html#partition-keys-for-faster-where-clause-filtering) Partition keys for faster `WHERE` clause filtering

Now the above query was actually a bit slow! There are 3 million rows in the table, and metadata filters need to visit every single row to do a comparison. Metadata comparison are quite fast and built for fast filtering, but they have their limits.

But notice how we only wanted a small subset of values – `between '2004-01-20' and '2009-01-20'` is only 5 years out of 30 years of data. We can tell the `vec0` virtual table to internally shard the vector index on a given key, using partition keys!

```sql
create virtual table vec_articles using vec0(
  article_id integer primary key,
  headline_embedding float[384],

  -- shard the vector index based on published year
  year integer partition key,

  news_desk text,
  word_count integer,
  pub_date text
);

select
  article_id,
  headline,
  news_desk,
  word_count,
  pub_date,
  distance
from vec_articles
where headline_embedding match lembed('new york city housing')
  and k = 20
  -- narrow search to these years only
  and year between 2004 and 2009
  and news_desk = 'Metro'
  and word_count < 1000
  -- finer filtering for exact dates we care about
  and pub_date between '2004-01-20' and '2009-01-20';
```

This KNN query returns the same exact results as the one above - but is 3x faster! This is because internally, vectors are stored based on the `year` value of its row. In that KNN query, `sqlite-vec` will recognize constraints on partition keys, and quickly pre-filter rows before any vectors are compared.

But beware! It's easy to accidentally over-shard a vector index on the wrong values and cause performance issues. Partition keys are great for date-based items like `year` or `month`, particulary when each unique partition key value has 100's or 1000's of vectors. They are also great for user IDs or document IDs, for "per-user" or "per-document" vector indexes.

Partition key columns can only be `TEXT` or `INTEGER` values, file an issue if you want to see some other type support. Currently `column in (...)` constraints are not supported for partition key columns, [but will be soon](https://github.com/asg017/sqlite-vec/issues/142)!

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-metadata-release/index.html#auxiliary-columns) Auxiliary columns

Some columns never need to be indexed! You can always store addtionally `SELECT`-only metadata in separate tables and do a `JOIN` yourself, or you can use auxiliary columns:

```sql
create virtual table vec_articles using vec0(
  article_id integer primary key,
  headline_embedding float[384],
  +headline text,
  +url text
);

select
  article_id,
  headline,
  url,
  distance
from vec_articles
where headline_embedding match lembed('dodgers game')
  and k = 20;
```

```text
┌────────────┬─────────────────────────────────────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────────────────┐
│ article_id │ headline                                                                            │ url                                                                                                                               │ distance           │
├────────────┼─────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤
│    1896278 │ Attention Dodgers Fans: There’s a Game Tonight                                      │ https://bats.blogs.nytimes.com/2008/10/15/attention-dodgers-fans-theres-a-game-tonight/                                           │ 0.6733786463737488 │
│    2556896 │ Dodgers, in Flurry of Activity, Move to Revamp Their Infield                        │ https://www.nytimes.com/2014/12/11/sports/baseball/mlb-jimmy-rollins.html                                                         │ 0.7796685099601746 │
│    2382487 │ Keeping Up With the Dodgers                                                         │ https://www.nytimes.com/2012/12/15/sports/angels-keeping-up-with-the-dodgers-leading-off.html                                     │ 0.7849781513214111 │
│    2585169 │ New Life for the Dodgers’ Old Digs                                                  │ https://www.nytimes.com/slideshow/2015/04/19/sports/baseball/20150419DODGERTOWN.html                                              │ 0.7894293665885925 │
│    1032111 │ Not Dodgers II, but It's Baseball; The Game Is Back in Brooklyn, on a Smaller Scale │ https://www.nytimes.com/2001/06/23/nyregion/not-dodgers-ii-but-it-s-baseball-the-game-is-back-in-brooklyn-on-a-smaller-scale.html │ 0.7978747487068176 │
└────────────┴─────────────────────────────────────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────────────────┘
```

Auxiliary columns are denoted by a `+` prefix in the column definition, modeled after [the same feature in the SQLite R*Tree extension](https://www.sqlite.org/rtree.html#auxiliary_columns). These columns are unindex, stored in a separate internal table and `JOIN`'ed at `SELECT` time. They *cannot* appear in a KNN `WHERE` query, as performance would worsen dramatically.

But it saves you from dealing with additional `JOIN`s yourself! They are especially great for longer `TEXT` or `BLOB` values.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-metadata-release/index.html#roadmap-and-the-future-of-sqlite-vec) Roadmap and the future of `sqlite-vec`

Metadata column support is the biggest update to `sqlite-vec` since the initial [`v0.1.0` launch 3 months ago](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html), but I have a lot planned for the project!

First off: **ANN indexes.** The `vec0` virtual table is brute-force only, which really slows down KNN queries on larger datasets. There are strategies like [binary quantization](https://alexgarcia.xyz/sqlite-vec/guides/binary-quant.html) or [Matryoshka embeddings](https://alexgarcia.xyz/sqlite-vec/guides/matryoshka.html) that can help, but `sqlite-vec` won't be fast until ANN indexes are supported.

I delayed working on ANN indexes until metadata columns were supported, because its much easier to build an ANN index with metaddata filtering on day 1 than it is to retroactively try to support them. I think this was the right call — metadata columns are hard! Follow [issue #25](https://github.com/asg017/sqlite-vec/issues/25) for future update on this!

Next: **Quantizers.** Currently `sqlite-vec` only supported simple binary quantization and scalar quantization with `int8` vectors. But I want to support `float16`, `float8`, "smarter" binary quantization (ie custom thresholds instead of just `> 0`), and other techniques that have come about the last few months. This will also help support ANN indexes, as many of them rely on vector compression for fast queries.

There's also a ton of **performance work** that `sqlite-vec` needs, especially with these new metadata column features. This initial release was more of a "make it work" and not "make it fast", so expect much faster metadata filtering in upcoming releases!

Sister projects [`sqlite-lembed`](https://github.com/asg017/sqlite-lembed) and [`sqlite-rembed`](https://github.com/asg017/sqlite-rembed) also need a ton of love, they both have some older PRs that need merging. Expect releases of both of these projects very soon!

And finally, **a ton of smaller integrations**! For example, Rody Davis [submitted Dart and Flutter bindings](https://github.com/asg017/sqlite-vec/pull/119) that I have not yet merged, Oscar Franco contributed [Android and iOS bindings](https://github.com/asg017/sqlite-vec/pull/91) that needs love, and [Pyodide support is on the horizon](https://github.com/asg017/sqlite-vec/issues/135).

[Alex Garcia's Blog](https://alexgarcia.xyz/blog/)

Change theme

# Hybrid full-text search and vector search with SQLite

2024-10-02 by [Alex Garcia](https://alexgarcia.xyz/)

> *tl;dr — You can use [SQLite's builtin full-text search (FTS5) extension](https://www.sqlite.org/fts5.html) and semantic search with [`sqlite-vec`](https://github.com/asg017/sqlite-vec) to create "hybrid search" in your applications. You can combine results using different methods like keyword-first, re-ranking by "semantics", and [reciprocal rank fusion](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking). Best of all, since it's all in SQLite, experiments and prototypes are cheap and easy, no 3rd party services required!*

---

The primary use-case for `sqlite-vec` and other vector search tools is to offer "semantic search" to text data. Full-text search (aka keyword search) alone doesn't always give great results — Queries like "climate change" won't return documents that say "global warming," or "reproductive rights" won't return documents about "abortion bans." Semantic search allows you to lookup results by "vibes," returning richer results with more meaning.

But using "semantic search" as your **only** search method can be harmful to your applications. Take this tweet as an example:

>  *fun fact: on the "max" app, you have to scroll through 32 results to find "adventure time" despite typing it in exactly how its spelled. the first result is rick and morty* [`@boygrrI` Aug 27, 2023](https://x.com/boygrrI/status/1696029804770771123)
>
> ![](https://blog-static.alxg.xyz/F4mCHdpWsAAntlt.jpeg)

Why would searching "adventure time" on HBO Max not return the actual (and amazing) [Adventure Time](https://www.max.com/shows/adventure-time/fff09eaf-17c3-446b-be32-8a0d47e4ccf1) TV show as the first result, and instead return 30 other shows first?

Forgetting the actual "Adventure Time" TV Show, the query "'adventure time" could mean many different things. Rick and Morty has interdimensional adventures, Aqua Teen Hunger Force has ["surreal adventures"](https://en.wikipedia.org/wiki/Aqua_Teen_Hunger_Force#:~:text=is%20about%20the-,surreal%20adventures,-and%20antics%20of). Who's to say a user doesn't want to see recommendations like that in their general "adventure time" search?

Then again, when you search "adventure time", then the "Adventure Time" TV show should be the first result. This is the push and pull of vector search and keyword search: vector search gives you a more fuzzy recommendations-like search experience, while keyword search is the obvious answer much of the time. Both are important, so how do you juggle both?

SQLite has had keyword or "full text" search for over a decade, in the form of the [FTS5 extension](https://www.sqlite.org/fts5.html), which drives search applications [or billions](https://www.sqlite.org/mostdeployed.html) of devices every single day. We can combine this battle-tested SQLite keyword search with the new [`sqlite-vec`](https://github.com/asg017/sqlite-vec) vector search extension to offer easy-yet-configurable hybrid search, which can run on the command line, on mobile devices, Raspberry Pis, and even web browsers with WASM!

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html#the-demo-nbc-news-headlines) The demo: NBC News Headlines

We're gonna work with a dataset of news headlines, scraped from [the NBC News sitemaps](https://www.nbcnews.com/archive/articles/2024/march). This subset contains 14,500+ headlines from January 2024 to August 2024 totaling `4.3MB` of text data, a very small dataset.

Here's a sample of what's in the `articles` table:

```text
┌────┬──────┬───────┬──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ id │ year │ month │ headline                                                                                             │
├────┼──────┼───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  1 │ 2024 │     1 │ Washington state faces first outbreak of a deadly fungal infection that's on the rise in the U.S.    │
│  2 │ 2024 │     1 │ Israel-Hamas war live updates: U.S. readies weeks of retaliatory strikes against Iran-linked targets │
│  3 │ 2024 │     1 │ House to vote on an expanded child tax credit bill                                                   │
│  4 │ 2024 │     1 │ Travel costs, staff and ads added up before Ron DeSantis dropped out                                 │
│  5 │ 2024 │     1 │ Victims of Hamas attack in Israel and their families blame Iran in new federal lawsuit               │
│  6 │ 2024 │     1 │ Trump meets with Teamsters as he targets Biden support                                               │
│  7 │ 2024 │     1 │ The bipartisan border deal would not allow 5,000 illegal crossings per day, despite what Trump says  │
│  8 │ 2024 │     1 │ Machu Picchu tourism suffering after week of protests against new ticketing system                   │
│  9 │ 2024 │     1 │ FCC moves to criminalize most AI-generated robocalls                                                 │
│ 10 │ 2024 │     1 │ Civil rights group says N.C. public schools are harming LGBTQ students, violating federal law        │
└────┴──────┴───────┴──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Now let's build a FTS5 index and vector index with the text inside `headline` column. We will do this with `fts5` and `vec0` virtual tables. The different "combination" methods described later use these two virtual tables, and just use different algorithms/approaches to join + order the data.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html#building-the-full-text-search-fts-5-table) Building the full-text search FTS5 table

We can create, seed, and optimize a `fts_headlines` full-text search virtual table from the base `articles` table with a few SQL statements:

```sql
create virtual table fts_articles using fts5(
  headline,
  content='articles', content_rowid='id'
);

insert into fts_articles(rowid, headline)
  select rowid, headline
  from articles;

insert into fts_articles(fts_articles) values('optimize');
```

We define the `fts_headline` virtual table, declaring the `headline` column and defining the `content=` and `content_rowid=` options to configure an [external content table](https://www.sqlite.org/fts5.html#external_content_tables). This will save some space, signaling the `FTS5` extensions to not store the headline `TEXT` and only store the FTS index, since we can join back to the `articles` table to retrieve the `headline` contents.

After that's declared, we can `INSERT INTO` directly into the `fts_headline` table from the base `articles` table. The [`'optimize'`](https://www.sqlite.org/fts5.html#the_optimize_command) command won't help much for this small of a dataset, but is useful in larger projects.

Now to query this FTS5 table, all we need is a single `SELECT` statement:

```sql
select
  rowid,
  headline,
  rank
from fts_articles
where headline match 'planned parenthood'
limit 10;
```

```text
┌───────┬──────────────────────────────────────────────────────────────┬───────────────────┐
│ rowid │                           headline                           │       rank        │
├───────┼──────────────────────────────────────────────────────────────┼───────────────────┤
│ 4666  │ Kamala Harris visits Planned Parenthood clinic               │ -18.9139950477264 │
├───────┼──────────────────────────────────────────────────────────────┼───────────────────┤
│ 6521  │ Former Marine sentenced to 9 years in prison for firebombing │ -14.8070227038387 │
│       │  Planned Parenthood clinic                                   │                   │
└───────┴──────────────────────────────────────────────────────────────┴───────────────────┘
```

The search `"planned parenthood"` return 2 results, both that specifically have the keywords "planned parenthood". The `rank` column is the [negative bm25 score](https://www.sqlite.org/fts5.html#:~:text=The%20%22%2D1%22%20term,numerically%20lower%20scores.) of the query and the headline.

Now these types of results are exactly what I want — what I search is what I get. But maybe I want to see more than just "planned parenthood", like articles about abortion, reproductive rights, women's healthcare, etc. This is what vector search offers us, and setting that up in SQLite looks very similar to FTS5 tables.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html#building-vector-search-with-sqlite-vec) Building vector search with `sqlite-vec`

Now `sqlite-vec` offers vector storage and vector comparisions, but it does not generate embeddings for you. If you're running `sqlite-vec` from a Python/Node.js/some other script, you can always use a 3rd party service or a local embeddings inference API to generate embeddings. But for this example, I want to keep everything in SQL and keep things local, so I'll use the [`sqlite-lembed`](https://github.com/asg017/sqlite-lembed) extension with the [`Snowflake Artic Embed 1.5 model`](https://www.snowflake.com/engineering-blog/arctic-embed-m-v1-5-enterprise-retrieval/).

You can download a `.gguf` quantized version of this model with:

```bash
wget https://huggingface.co/asg017/sqlite-lembed-model-examples/resolve/main/snowflake-arctic-embed-m-v1.5/snowflake-arctic-embed-m-v1.5.d70deb40.f16.gguf
```

And we can configure `sqlite-lembed` to use this model like so:

```sql
.load ./lembed0
insert into lembed_models(name, model) values
  ('default', lembed_model_from_file('./snowflake-arctic-embed-m-v1.5.d70deb40.f16.gguf'));
```

Now we can embed our text with the `lembed()` SQL function! We will store these embeddings in a `vec0` virtual table like so:

```sql
.load ./vec0

create virtual table vec_articles using vec0(
  article_id integer primary key,
  headline_embedding float[768]
);

insert into vec_articles(article_id, headline_embedding)
  select
    rowid,
    lembed(headline)
  from articles;
```

And that's it! To perform a KNN query, we can do something like so:

```sql
select
  articles.headline,
  vec_articles.distance
from vec_articles
left join articles on articles.rowid = vec_articles.article_id
where headline_embedding match lembed("planned parenthood")
  and k = 10;
```

```text
┌──────────────────────────────────────────────────────────────┬───────────────────┐
│                           headline                           │     distance      │
├──────────────────────────────────────────────────────────────┼───────────────────┤
│ Kamala Harris visits Planned Parenthood clinic               │ 0.492593914270401 │
├──────────────────────────────────────────────────────────────┼───────────────────┤
│ After Dobbs decision, more women are managing their own abor │ 0.578903257846832 │
│ tions                                                        │                   │
├──────────────────────────────────────────────────────────────┼───────────────────┤
│ Transforming Healthcare                                      │ 0.582241117954254 │
├──────────────────────────────────────────────────────────────┼───────────────────┤
│ A timeline of Trump's many, many positions on abortion       │ 0.610146284103394 │
├──────────────────────────────────────────────────────────────┼───────────────────┤
│ How a network of abortion pill providers works together in t │ 0.61968868970871  │
│ he wake of new threats                                       │                   │
├──────────────────────────────────────────────────────────────┼───────────────────┤
│                                  ...                                             │
└──────────────────────────────────────────────────────────────┴───────────────────┘
```

Now that we have `fts_articles` and `vec_articles` virtual tables set up, we can now explore different hybrid search methods. The core FTS5 and `vec0` queries will remain the same, they only really differ by using different `JOIN` or `ORDER BY` methods.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html#hybrid-approach-1-keyword-first) Hybrid approach #1: "Keyword-first"

The first hybrid approach: return full-text search results first, then augment the rest with vector search.

We can perform this with a CTE, doing FTS5 and `sqlite-vec` searches in separate steps, combining them after with a `UNION ALL`:

```sql
.param set :query 'abortion bans'
.param set :k 10


--- FTS5 search results
with fts_matches as (
  select
    rowid as article_id,
    row_number() over (order by rank) as rank_number,
    rank as score
  from fts_articles
  where headline match :query
  limit :k
),
--- sqlite-vec KNN vector search results
vec_matches as (
  select
    article_id,
    row_number() over (order by distance) as rank_number,
    distance as score
  from vec_articles
  where
    headline_embedding match lembed(:query)
    and k = :k
  order by distance
),
-- combining FTS5 + vector search results, FTS comes first
combined as (
  select 'fts' as match_type, * from fts_matches
  union all
  select 'vec' as match_type, * from vec_matches
),
-- JOIN back the articles.headline contents
final as (
  select
    articles.id,
    articles.headline,
    combined.*
  from combined
  left join articles on articles.rowid = combined.article_id
)
select * from final;
```

The results:

```text
┌───────┬──────────────────────────────────────────────────────────────┬────────────┬────────────┬─────────────┬───────────────────┐
│  id   │                           headline                           │ match_type │ article_id │ rank_number │       score       │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 10098 │ Kamala Harris says abortion bans are creating 'a health care │ fts        │ 10098      │ 1           │ -10.6788292709361 │
│       │  crisis'                                                     │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 9776  │ States with abortion bans saw birth control prescriptions fa │ fts        │ 9776       │ 2           │ -10.0163167259711 │
│       │ ll post-Dobbs, study finds                                   │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 2292  │ Ohio GOP Senate candidates pitch federal abortion bans even  │ fts        │ 2292       │ 3           │ -9.7149595994016  │
│       │ after voters protected reproductive rights                   │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 452   │ 64K women and girls became pregnant due to rape in states wi │ fts        │ 452        │ 4           │ -9.16355856942554 │
│       │ th abortion bans, study estimates                            │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 9187  │ Abortion bans drive away up to half of young talent, CNBC/Ge │ fts        │ 9187       │ 5           │ -9.16355856942554 │
│       │ neration Lab youth survey finds                              │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 6989  │ Trump says abortion restrictions should be left to states, d │ vec        │ 6989       │ 1           │ 0.493074983358383 │
│       │ odging a national ban                                        │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 13928 │ After Dobbs decision, more women are managing their own abor │ vec        │ 13928      │ 2           │ 0.512084662914276 │
│       │ tions                                                        │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 11822 │ Iowa now bans most abortions after about 6 weeks             │ vec        │ 11822      │ 3           │ 0.512569785118103 │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 7381  │ Where abortion rights could be on the ballot this fall: From │ vec        │ 7381       │ 4           │ 0.516829192638397 │
│       │  the Politics Desk                                           │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 14009 │ Trump signals openness to banning abortion pill              │ vec        │ 14009      │ 5           │ 0.528829395771027 │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 4426  │ Medication abortions rose in year after Dobbs decision, repo │ vec        │ 4426       │ 6           │ 0.530509769916534 │
│       │ rt finds                                                     │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 4328  │ Trump signals support for a national 15-week abortion ban    │ vec        │ 4328       │ 7           │ 0.532848060131073 │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 6979  │ A timeline of Trump's many, many positions on abortion       │ vec        │ 6979       │ 8           │ 0.533357560634613 │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 2092  │ For the first time in years, Sen. Graham hasn't introduced a │ vec        │ 2092       │ 9           │ 0.533683061599731 │
│       │  national abortion ban                                       │            │            │             │                   │
├───────┼──────────────────────────────────────────────────────────────┼────────────┼────────────┼─────────────┼───────────────────┤
│ 6794  │ Trump's conflicting abortion stances are coming back to haun │ vec        │ 6794       │ 10          │ 0.534709513187408 │
│       │ t him — and his party                                        │            │            │             │                   │
└───────┴──────────────────────────────────────────────────────────────┴────────────┴────────────┴─────────────┴───────────────────┘
```

This approach would technically fix the "Adventure Time + HBO Max" problem described above — what users expect will always come first. Then if those results aren't good enough, then hopefully the vector search results can satisfy them!

One note: this specific query doesn't do any de-duplication, so include that if needed.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html#hybrid-approach-2-reciprocal-rank-fusion-rrf) Hybrid approach #2: Reciprocal Rank Fusion (RRF)

Another approach: [Reciprocal Rank Fusion (RRF)](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking), which ranks results that are both FTS5 and vector matches higher than others. Similar to the approach above, we can do this in a single `SELECT` query with CTEs, as described [in the Supabase docs](https://supabase.com/docs/guides/ai/hybrid-search):

```sql
.param set :query 'abortion ban'


.param set :k 10
.param set :rrf_k 60
.param set :weight_fts 1.0
.param set :weight_vec 1.0

-- the sqlite-vec KNN vector search results
with vec_matches as (
  select
    article_id,
    row_number() over (order by distance) as rank_number,
    distance
  from vec_articles
  where
    headline_embedding match lembed(:query)
    and k = :k
),
-- the FTS5 search results
fts_matches as (
  select
    rowid,
    row_number() over (order by rank) as rank_number,
    rank as score
  from fts_articles
  where headline match :query
  limit :k
),
-- combine FTS5 + vector search results with RRF
final as (
  select
    articles.id,
    articles.headline,
    vec_matches.rank_number as vec_rank,
    fts_matches.rank_number as fts_rank,
    -- RRF algorithm
    (
      coalesce(1.0 / (:rrf_k + fts_matches.rank_number), 0.0) * :weight_fts +
      coalesce(1.0 / (:rrf_k + vec_matches.rank_number), 0.0) * :weight_vec
    ) as combined_rank,
    vec_matches.distance as vec_distance,
    fts_matches.score as fts_score
  from fts_matches
  full outer join vec_matches on vec_matches.article_id = fts_matches.rowid
  join articles on articles.rowid = coalesce(fts_matches.rowid, vec_matches.article_id)
  order by combined_rank desc
)
select * from final;
```

And the results:

```text
┌───────┬──────────────────────────────────────────────────────────────┬──────────┬──────────┬────────────────────┬───────────────────┬───────────────────┐
│  id   │                           headline                           │ vec_rank │ fts_rank │   combined_rank    │   vec_distance    │     fts_score     │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 4328  │ Trump signals support for a national 15-week abortion ban    │ 2        │ 3        │ 0.0320020481310804 │ 0.533420383930206 │ -9.84164516849395 │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 5769  │ Mitch McConnell shies away from supporting national abortion │ 8        │ 2        │ 0.0308349146110057 │ 0.550142526626587 │ -10.1901778756711 │
│       │  ban                                                         │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 9507  │ Arizona Senate passes repeal of 1864 abortion ban            │          │ 1        │ 0.0163934426229508 │                   │ -10.5643028316427 │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 6989  │ Trump says abortion restrictions should be left to states, d │ 1        │          │ 0.0163934426229508 │ 0.514239549636841 │                   │
│       │ odging a national ban                                        │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 10717 │ Supreme Court rejects bid to restrict access to abortion pil │ 3        │          │ 0.0158730158730159 │ 0.535124838352203 │                   │
│       │ l                                                            │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 5981  │ Arizona state House passes bill to repeal 1864 abortion ban  │          │ 4        │ 0.015625           │                   │ -9.84164516849395 │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 14009 │ Trump signals openness to banning abortion pill              │ 4        │          │ 0.015625           │ 0.536433517932892 │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 6375  │ Arizona Republicans again quash effort to repeal 1864 aborti │          │ 5        │ 0.0153846153846154 │                   │ -9.84164516849395 │
│       │ on ban                                                       │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 7381  │ Where abortion rights could be on the ballot this fall: From │ 5        │          │ 0.0153846153846154 │ 0.546237885951996 │                   │
│       │  the Politics Desk                                           │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 9443  │ Arizona Gov. Katie Hobbs signs repeal of 1864 abortion ban   │          │ 6        │ 0.0151515151515152 │                   │ -9.84164516849395 │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 13928 │ After Dobbs decision, more women are managing their own abor │ 6        │          │ 0.0151515151515152 │ 0.546703100204468 │                   │
│       │ tions                                                        │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 1821  │ Dominican women fight child marriage, teen pregancy amid tot │          │ 7        │ 0.0149253731343284 │                   │ -9.51616557526609 │
│       │ al abortion ban                                              │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 2092  │ For the first time in years, Sen. Graham hasn't introduced a │ 7        │          │ 0.0149253731343284 │ 0.547752380371094 │                   │
│       │  national abortion ban                                       │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 7150  │ Tennessee court weighs challenge to abortion ban’s narrow me │          │ 8        │ 0.0147058823529412 │                   │ -9.51616557526609 │
│       │ dical exception                                              │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 8690  │ Arizona Supreme Court pushes back enforcement date for 1864  │          │ 9        │ 0.0144927536231884 │                   │ -9.51616557526609 │
│       │ abortion ban                                                 │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 11822 │ Iowa now bans most abortions after about 6 weeks             │ 9        │          │ 0.0144927536231884 │ 0.555717051029205 │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 2646  │ Trump campaign scrambles over abortion ban report as Democra │          │ 10       │ 0.0142857142857143 │                   │ -9.21152510186621 │
│       │ ts seize the moment                                          │          │          │                    │                   │                   │
├───────┼──────────────────────────────────────────────────────────────┼──────────┼──────────┼────────────────────┼───────────────────┼───────────────────┤
│ 5538  │ Map: Where medication abortion is and isn’t legal            │ 10       │          │ 0.0142857142857143 │ 0.558846414089203 │                   │
└───────┴──────────────────────────────────────────────────────────────┴──────────┴──────────┴────────────────────┴───────────────────┴───────────────────┘
```

Note that the first result `"Trump signals support for a national 15-week abortion ban"` was ranked 2nd in the vector result and 3rd in FTS5 results. But since it's in both, it's ranked higher than the respective #1 results.

It's also configurable, you can change `:weight_fts` or `:weight_vec` to rank FTS5/vector results differently, which can be handy!

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html#hybrid-approach-3-re-rank-by-semantics) Hybrid approach #3: Re-rank by semantics

This approach is slightly different than the ones above: instead of querying the `vec0` table as all, we just perform a FTS5 search, but re-order the results based on their vector distance.

```sql
.param set :query 'abortion ban'
.param set :k 10


-- The FTS5 search results
with fts_matches as (
  select
    rowid,
    row_number() over (order by rank) as fts_rank_number,
    rank as score
  from fts_articles
  where headline match :query
  limit :k
),
-- re-ordered by "semantic meaning"
final as (
  select
    articles.id,
    articles.headline,
    fts_matches.*
  from fts_matches
  left join articles on articles.rowid = fts_matches.rowid
  order by vec_distance_cosine(lembed(:query), lembed(articles.headline))
)
select * from final;
```

And the results:

```text
┌──────┬──────────────────────────────────────────────────────────────┬───────┬─────────────────┬───────────────────┐
│  id  │                           headline                           │ rowid │ fts_rank_number │       score       │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 4328 │ Trump signals support for a national 15-week abortion ban    │ 4328  │ 3               │ -9.84164516849395 │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 5769 │ Mitch McConnell shies away from supporting national abortion │ 5769  │ 2               │ -10.1901778756711 │
│      │  ban                                                         │       │                 │                   │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 2646 │ Trump campaign scrambles over abortion ban report as Democra │ 2646  │ 10              │ -9.21152510186621 │
│      │ ts seize the moment                                          │       │                 │                   │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 7150 │ Tennessee court weighs challenge to abortion ban’s narrow me │ 7150  │ 8               │ -9.51616557526609 │
│      │ dical exception                                              │       │                 │                   │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 1821 │ Dominican women fight child marriage, teen pregancy amid tot │ 1821  │ 7               │ -9.51616557526609 │
│      │ al abortion ban                                              │       │                 │                   │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 6375 │ Arizona Republicans again quash effort to repeal 1864 aborti │ 6375  │ 5               │ -9.84164516849395 │
│      │ on ban                                                       │       │                 │                   │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 9507 │ Arizona Senate passes repeal of 1864 abortion ban            │ 9507  │ 1               │ -10.5643028316427 │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 8690 │ Arizona Supreme Court pushes back enforcement date for 1864  │ 8690  │ 9               │ -9.51616557526609 │
│      │ abortion ban                                                 │       │                 │                   │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 5981 │ Arizona state House passes bill to repeal 1864 abortion ban  │ 5981  │ 4               │ -9.84164516849395 │
├──────┼──────────────────────────────────────────────────────────────┼───────┼─────────────────┼───────────────────┤
│ 9443 │ Arizona Gov. Katie Hobbs signs repeal of 1864 abortion ban   │ 9443  │ 6               │ -9.84164516849395 │
└──────┴──────────────────────────────────────────────────────────────┴───────┴─────────────────┴───────────────────┘
```

We still get only keyword match results, but better semantic matches will float towards the top. This can help workaround some of the disadvantages of BM25.

One note: this query here is inefficient — `lembed()` is called on each result, even though we pre-computed them in `vec_articles`. This could be replaced with a `SELECT headline_embedding FROM vec_articles WHERE rowid in (...)` query.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html#which-should-i-choose) Which should I choose?

It depends on your application and use-case!

Are you building a search engine for email inbox? If so keyword-first may make the most sense, as "what you search is what you get" is pretty important in more inbox searches, at least in my experience.

Are you building RAG across some internal company documents? If so RRF may be a good option, as exact matches like internal company project names are important, while semantic matches can better shape a query. Plus, a LLM can usually parse out irrelevant responses.

Are you building a ["duplicate post"](https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/marking-issues-or-pull-requests-as-a-duplicate) feature into your webapp? If some re-rank by semantics might work well, as finding exact matches would be contextually important, but the top few results would matter more.

So it really depends! What's nice about doing this in SQLite makes experimenting and prototyping easy. Your data is a single file, you can test multiple queries will single `SELECT` statements. It costs nothing, works in all programming languages, and can be easily done in a few lines of code.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html#future-improvements) Future Improvements

The union between FTS5 and `sqlite-vec` is great for small samples, but there's still some rough edges to smooth out!

For example: FTS5 query can "highlight" matches in a document like so:

```sql
select
  rowid,
  highlight(fts_articles, 0, '<b>', '</b>') as headline_highlighted
from fts_articles
where headline match 'planned parenthood'
limit 10;
```

```text
┌───────┬──────────────────────────────────────────────────────────────┐
│ rowid │                     headline_highlighted                     │
├───────┼──────────────────────────────────────────────────────────────┤
│ 4666  │ Kamala Harris visits <b>Planned</b> <b>Parenthood</b> clinic │
├───────┼──────────────────────────────────────────────────────────────┤
│ 6521  │ Former Marine sentenced to 9 years in prison for firebombing │
│       │  <b>Planned</b> <b>Parenthood</b> clinic                     │
└───────┴──────────────────────────────────────────────────────────────┘
```

This adds HTML bold tags around the query matches in the document itself, so you can see easily see why a document is returned.

But `sqlite-vec` doesn't have this — a vector search only returns the L2/cosine distance between the query vector and document, not *why* they are a match. There are models out there like [ColBERT](https://huggingface.co/vespa-engine/col-minilm) that provide ["scoring" on queries and passages](https://simonwillison.net/2024/Jan/28/colbert-query-passage-scoring-interpretability/), but `sqlite-vec` doesn't have tensor support yet.

Also, FTS5 queries have a ton of other features like [phrases](https://www.sqlite.org/fts5.html#fts5_phrases), [`NEAR` queries](https://www.sqlite.org/fts5.html#fts5_near_queries), and [boolean operators](https://www.sqlite.org/fts5.html#fts5_boolean_operators). Using these features will make vector searches awkward, since the query would be provided as-is.

Also, scaling hybrid search with FTS5 + `sqlite-vec` might be awkward. FTS5 tables perform a full search across the entire dataset everytime, there's no way of provided metadata filtering or indexing on a single FTS5 index. This isn't the case for `sqlite-vec` either, but support for [paritioning](https://github.com/asg017/sqlite-vec/issues/29) and [metadata filtering](https://github.com/asg017/sqlite-vec/issues/26) is coming soon!

---

So try out hybrid search with `sqlite-vec` in your projects! Feel free to drop any questions in the [`#sqlite-vec` channel in the Mozilla Discord](https://discord.gg/Ve7WeCJFXk).

# Introducing sqlite-vec v0.1.0: a vector search SQLite extension that runs everywhere

2024-08-01 by [Alex Garcia](https://alexgarcia.xyz/)

> *`sqlite-vec` is a new vector search SQLite extension written entirely in C with no dependencies, MIT/Apache-2.0 dual licensed. The first "stable" `v0.1.0` release is here, meaning that it is ready for folks to try in their own projects! There are many ways to install it across multiple package managers, and will soon become a part of popular SQLite-related products like SQLite Cloud and Turso. Try it out today!*

---

The first "stable" `v0.1.0` release of `sqlite-vec` is finally out! You can install and run it in multiple different ways, including:

- [`pip install sqlite-vec`](https://alexgarcia.xyz/sqlite-vec/python.html) for Python
- [`npm install sqlite-vec`](https://alexgarcia.xyz/sqlite-vec/js.html) for Node.js, Bun, or Deno
- [`gem install sqlite-vec`](https://alexgarcia.xyz/sqlite-vec/ruby.html) for Ruby
- [`cargo add sqlite-vec`](https://alexgarcia.xyz/sqlite-vec/rust.html) for Rust
- [`go get github.com/asg017/sqlite-vec-go-bindings/cgo`](https://alexgarcia.xyz/sqlite-vec/go.html#cgo) for Go using CGO
- [`go get github.com/asg017/sqlite-vec-go-bindings/ncruces`](https://alexgarcia.xyz/sqlite-vec/go.html#ncruces) for Go in non-CGO WASM flavor
- `curl -L https://github.com/asg017/sqlite-vec/releases/download/v0.1.0/install.sh | sh` if you're feeling brave

First introduced in [my previous blog post](http://alexgarcia.xyz/blog/2024/building-new-vector-search-sqlite/index.html), `sqlite-vec` is a no-dependency SQLite extension for vector search, written entirely in a single C file. It's extremely portable, works in most operating systems and environments, and is MIT/Apache-2 dual licensed.

`sqlite-vec` works in a similar way to [SQLite's full-text search](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#) support — you declare a "virtual table" with vector columns, insert data with normal `INSERT INTO` statements, and query with normal `SELECT` statements.

```sql
create virtual table vec_articles using vec0(
  article_id integer primary key,
  headline_embedding float[384]
);

insert into vec_articles(article_id, headline_embedding) values
   (1, '[0.1, 0.2, ...]'),
   (2, '[0.3, 0.4, ...]'),
   (3, '[0.5, 0.6, ...]');

-- KNN-style query: the 20 closes headlines to 'climate change'
select
    rowid,
    distance
from vec_articles
where headline_embedding match embed('climate change')
  and k = 20;
```

`vec0` virtual tables store your vectors inside the same SQLite database with shadow tables, just like `fts5` virtual tables. They are designed to be efficient during `INSERT`'s, `UPDATE`'s, and `DELETE`'s. A `MATCH` constraint on a vector column signals a KNN style search, which is also optimized for speed.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#it-runs-everywhere) It runs everywhere!

`sqlite-vec` works on MacOS, Linux, and Windows. It runs [in the browser with WebAssembly](https://alexgarcia.xyz/sqlite-vec/wasm.html), in command line tools, and inside web applications on the server. It compiles successfully on Android and theoretically on iOS, I just don't have pre-compiled packages available yet. It works on Raspberry Pis and other small devices.

As proof, here's `sqlite-vec` running a semantic search demo on my [Beepy device](https://beepy.sqfmi.com/), which is a Raspberry Pi Zero.

Play: A semantic search engine with sqlite-vec on my Beepy (Raspberry Pi Zero)

That demo is a single SQLite file, the `all-MiniLM-L6-v2` model in GGUF format (f16 quantization), `sqlite-vec`, [`sqlite-lembed`](https://github.com/asg017/sqlite-lembed), and Python. Not a single byte of data leaves the device.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#only-brute-force-search-for-now) Only brute-force search for now

Many vector search library have some form of "approximate nearest neighbors" (ANN) index. By trading accuracy and resources for search speed, ANN indexes can scale to ten of millions or even billions of vectors. Think [HNSW](https://arxiv.org/abs/1603.09320), [IVF](https://www.ecva.net/papers/eccv_2018/papers_ECCV/papers/Dmitry_Baranchuk_Revisiting_the_Inverted_ECCV_2018_paper.pdf), or [DiskANN](https://www.microsoft.com/en-us/research/publication/diskann-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node/).

But let's be real - most applications of local AI or embeddings aren't working with billions of vectors. Most of my little data analysis projects deal with thousands of vectors, maybe hundreds of thousands. Rarely will I have millions upon millions of vectors.

So `sqlite-vec` is currently focused on really fast brute-force vector search. And it does [extremely well](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#benchmarks) in that regard. And with [quantization](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#matryoshka-and-quantization) and other vector compression techniques, you can get really, really far with this approach.

But let me be clear — I'm not ignoring performance in `sqlite-vec`, and `sqlite-vec` will eventually gain some form of ANN indexes in the near future (follow [#25](https://github.com/asg017/sqlite-vec/issues/25) for more info). It just didn't make sense to include a complex ANN solution in this initial version.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#quantization-and-matryoshka) Quantization and Matryoshka

"Vector quantization" refers to a few techniques to compress individual elements inside a floating point vector. Every element in a float vector takes up 4 bytes of space, which really adds up. One million 1536-dimensional vectors takes up `1536 * 4 * 1e6` byes, or `6.144 GB`!

`sqlite-vec` supports `bit` vectors alongside "regular" `float` vectors. These take up much less space — 1 bit per element, a 32x reduction! This does mean a loss of accuracy, but possibly not as much as you expect. Specifically, newer embeddings models like MixedBread's [`mixedbread-ai/mxbai-embed-large-v1`](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1) or Nomic's [`nomic-ai/nomic-embed-text-v1.5`](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) claim their models are trained on binary quantization loss, meaning a signicant amount of accuracy is maintained even after converting to binary.

To convert a float vector to a binary vector, all you need is the `vec_quantize_binary()` function:

```sql
create virtual table vec_items using vec0(
  embedding float[1536]
);

-- slim because "embedding_coarse" is quantized 32x to a bit vector
create virtual table vec_items_slim using vec0(
  embedding_coarse bit[1536]
);

insert into vec_items_slim
  select rowid, vec_quantize_binary(embedding) from vec_items;
```

Which will assign every element `<=0` to `0` and `>0` to `1`, and pack those results into a bitvector.

The result — depending on your embedding model, possibly only a 5-10% loss of quality, in exchange for ~10x faster queries!

`sqlite-vec` also supports [Matryoshka embeddings](https://huggingface.co/blog/matryoshka)! Matryoshka refer to a new technique in embeddings models that allow you to "truncate" excess dimensions of a given vector without losing much quality. This can save you a lot in storage and make search queries much faster, and `sqlite-vec` supports it!

```sql
create virtual table vec_items using vec0(
  embedding float[1536]
);

-- slim because "embedding" is a truncated version of the full vector
create virtual table vec_items_slim using vec0(
  embedding_coarse float[512]
);

insert into vec_items_slim
  select
    rowid,
    vec_normalize(vec_slice(embedding, 0, 512))
  from vec_items;
```

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#benchmarks) Benchmarks

As always, a disclaimer:

- Benchmarks rarely ever reflect real-world performance
- Every vector search tool is different, and it's totally possibly I use them incorrectly in this benchmark
- These benchmarks are likely skewed to workflows that work well in `sqlite-vec`
- Benchmarks are highly dependent on your machine and available resources
- [Let me know](https://github.com/asg017/sqlite-vec/issues/new) if you find any issues and I will correct it

That being said, if you want to compare how fast `sqlite-vec` is with other local-first vector search tools, here's a test I ran on my own machine. It mimics running multiple KNN queries sequentially on different vector search tools, to emulate what a "search engine" would do. A few qualifiers to this specific benchmark:

- **Only in-process vector search tools are included**, aka no external server or processes (no Pinecone, Qdrant, Milvus, Redis, etc. ). Mostly because I don't want to include client/server latencies, and they're harder to set up
- **Only brute force vector search is compared**. This does **NOT** include ANN indexes like HNSW, IVF, or DiskANN, only fullscan brute force searches. This is pretty unfair, as not all vector search tools really optimize for this, but it's what `sqlite-vec` does. And most benchmarks on ANN indexes also care about recall perf on top of search speed, which doesn't make much sense here.
- **Ran on my Mac M1 mini, 8GB of RAM**. In this case the datasets fit into memory, because most of these tools require that.
- **Runs queries sequentially and reports the average.** Some tools like Faiss could do multiple queries at the same time, but queries here are ran sequentially, to emulate a search engine.
- **"Build times"** refer to how fast that tool can convert an in-memory NumPy array of vectors into their internal storage. Some tools can read NumPy array with zero-copying, others will need to re-allocate the entire dataset.

The results:

```
       sift1m: 1,000,000 128-dimension vectors, k=20
```

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Tool ┃ Build Time (ms) ┃ Query time (ms) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ faiss │ 126ms │ 10ms │
│ sqlite-vec static │ 1ms │ 17ms │
│ sqlite-vec vec0 (8192|2048) │ 4589ms │ 33ms │
│ sqlite-vec vec0 (8192|1024) │ 3957ms │ 35ms │
│ duckdb │ 741ms │ 46ms │
│ usearch numpy exact=True │ 0ms │ 56ms │
│ sqlite-vec-scalar (8192) │ 1052ms │ 81ms │
│ numpy │ 0ms │ 136ms │
└─────────────────────────────┴─────────────────┴─────────────────┘

With 1 million 128 dimensions (sift1m, a small vector dataset), `sqlite-vec` performs well!

- `sqlite-vec-scalar` refers to running `vec_distance_l2(...)` manually and `ORDER BY` those results. This is slowest because it relies on the SQLite engine to calculate the top `k` results.
- `sqlite-vec vec0` stores vectors in a `vec0` virtual table. This is good for OLTP workloads as `UPDATE`/`INSERT`/`DELETE` operations are fast, and maintains fast queries with chunked internal storage. Build times are slow, as every insert tracks with SQLite transactions and needs to be assigned a chunk.
- `sqlite-vec static` is an experimental feature that directly queries in-memory static blobs. Here we can directly query the contiguously memory block that backs the numpy array (hence the 1ms build time), and KNN queries don't need handle multiple chunks like `vec0` does. On the other hand, static blobs are read-only, don't support inserts/updates/deletes, and must be kept entirely in memory.

And on a larger, more realistic dataset:

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Tool ┃ Build Time (ms) ┃ Query time (ms) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ sqlite-vec static │ 1ms │ 41ms │
│ usearch numpy exact=True │ 0ms │ 46ms │
│ faiss │ 12793ms │ 50ms │
│ sqlite-vec vec0 (8192|2048) │ 15502ms │ 87ms │
│ sqlite-vec vec0 (8192|1024) │ 13606ms │ 89ms │
│ sqlite-vec-scalar (8192) │ 7619ms │ 108ms │
│ duckdb │ 5296ms │ 307ms │
│ numpy │ 0ms │ 581ms │
└─────────────────────────────┴─────────────────┴─────────────────┘

This is the GIST1M dataset with 960 dimensions, but only the first 500,000 vectors because otherwise my Mac Mini runs out of memory.

- Here `sqlite-vec static` outperforms usearch and faiss, though I'd take this with a grain of salt. Anecdotally faiss and usearch typically outperform `sqlite-vec`, so this may just be a fluke on my machine.
- DuckDB struggles with larger dimensions, possibly because each vector could span across multiple pages (pure speculation on my side). DuckDB is also not a "vector database" so I imagine this will improve.
- I'm not sure why Faiss takes so long to build in this case.

And one more internal benchmark: How many vectors can `sqlite-vec` `vec0` tables handle? The benchmarks above hold all vectors in-memory, which is great for speed, but not realistic in many use-cases. So I devised another benchmark where I stored 100k vectors of various dimensions (3072, 1536, 768 etc.) and element types (float and bit), and saved them to disk. Then I ran KNN queries on them and timed the average response time.

The results:

![](https://blog-static.alxg.xyz/100k.png)

My "golden target" [is less than 100ms](https://developer.mozilla.org/en-US/docs/Web/Performance/How_long_is_too_long#responsiveness_goal). Here float vectors with large dimensions (3072, 1536) go above that at 214ms and 105ms respectively, which isn't great, but maybe fine for your use-case. For small dimensions (1024/768/384/192), all response are below 75ms, which is awesome!

For bit vectors the story is even better - even a full 3072-dimensional vector (which is already quite a ridiculous in size) is queried in 11ms, extremely fast. And in this case, where these vectors are from OpenAI's `text-embedding-3-large`, my anecdotal experience has shown a ~95% accuracy rate after binary quantization, which is fantastic!

However, the limits of `sqlite-vec` really show at 1 million vectors. The results:

![](https://blog-static.alxg.xyz/1m.png)

None of the float vectors at any dimension pass the 100ms smoke test — the 3072 dimension vectors take a whooping 8.52s to return, and even the tiny 192-dimensional vectors take 192ms.

However, if you can get away with binary quantization, then 124ms might be an acceptable range for you.

I wouldn't take the exact numbers posted here as the gospel - run different vector search tools on your projects and see what works best. But my takeaway to these benchmarks: **`sqlite-vec` is really fast.** Probably not the fastest in the word, but "fast enough" for most workflows you care about. There is definitely a practical limit for latency sensitive applications (probably in the 100's of thousands depending on your dimensions/quantization techniques), but you may not even reach that.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#sqlite-lembed-and-sqlite-rembed-sister-projects) `sqlite-lembed` and `sqlite-rembed` sister projects

Vector search is just one half of the equation — you also need a way to generate embeddings from your data. Many inference libraries are quite bulkly and difficult to install, so I created two other SQLite extensions to help tackle this: [`sqlite-lembed`](https://github.com/asg017/sqlite-lembed) and [`sqlite-rembed`](https://github.com/asg017/sqlite-rembed).

`sqlite-lembed` (SQLite 'local embed'), as announced in the [*"Introducing `sqlite-lembed`" blog post](https://alexgarcia.xyz/blog/2024/sqlite-lembed-init/index.html), allows you to generate embeddings from "local" models in `.gguf` format. `sqlite-rembed` (SQLite 'remote embed'), as announced in the [*"Introducing `sqlite-rembed`" blog post](https://alexgarcia.xyz/blog/2024/sqlite-rembed-init/index.html), allows you to generate embeddings from "remote" APIs like OpenAI, Nomic, Ollama, llamafile, and more. Neither are these are required to use `sqlite-vec`, and you don't have to use `sqlite-vec` if you use either of these extensions. But in case you want to keep all your work in pure SQL, these extensions can make your life a bit easier!

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#only-possible-through-sponsors) Only possible through sponsors

The main sponsor of `sqlite-vec` is Mozilla through the new [Mozilla Builders project](https://hacks.mozilla.org/2024/06/sponsoring-sqlite-vec-to-enable-more-powerful-local-ai-applications/). They provide substantial financial assistance, and help build our community with the [`#sqlite-vec` Discord Channel](https://discord.gg/Ve7WeCJFXk) in the Mozilla AI Discord server. I deeply appreciate their support!

Other corporate sponsors of `sqlite-vec` include:

- [Fly.io](https://fly.io/)
- [Turso](https://turso.tech/)
- [SQLite Cloud](https://sqlitecloud.io/)

If your company would be interested in sponsoring `sqlite-vec` , please [reach out to me](https://alexgarcia.xyz/)!

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#coming-soon-to-turso-and-sq-lite-cloud) Coming soon to Turso and SQLite Cloud!

Both [Turso](https://turso.tech/) and [SQLite Cloud](https://sqlitecloud.io/) have immediate plans to include `sqlite-vec` into their cloud offerings. More about this will be coming soon!

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html#v0-2-0-and-beyond) `v0.2.0` and beyond

To me, `v0.1.0` is all about stability and building a strong core. There are many, many features I have wanted to add to `sqlite-vec`, but have held off until the basics were down. This includes:

- **Metadata filtering**! Most applications want to filter a dataset before applying vector search (ie filter between a price range or after a specific date). This is on my immediate roadmap, follow [#26](https://github.com/asg017/sqlite-vec/issues/26) for more info.
- **Partitioned storage**! Enable per-user or per-document searches, great for single-tenant setups. Follow [#29](https://github.com/asg017/sqlite-vec/issues/29) for more info.
- **ANN indexes!** Brute force is already really fast, but a custom ANN index optimized for SQLite storage can hopefully get us in the "low millions" or "tens of millions" of vectors range. Follow [#25](https://github.com/asg017/sqlite-vec/issues/25) for more info.
- **kmeans** for clustering and IVF storage!
- **Better quantization methods!** Including [statistical binary quantization](https://www.timescale.com/blog/how-we-made-postgresql-as-fast-as-pinecone-for-vector-data/), product quantization, more scalar quantization methods, etc.
- **Classifiers!** Vector search on embeddings can emulate classification tasks with surprising accuracy, and first-class support in `sqlite-vec` can make that much easier

Looking at the very long term, I don't want to be actively developing `sqlite-vec` for my entire life. I want to get to a stable `v1` release in the next year or so, and keep it in maintenance mode shortly after. A "written entirely in C, no dependencies" project can only go so far without becoming an incomprehensible mess, and I care more about building stable and reliable tools than anything else.

---

So give `sqlite-vec` a shot! If you have any questions, feel free to post in the [`#sqlite-vec` Discord Channel](https://discord.gg/Ve7WeCJFXk), or open an issue on Github.

# Introducing sqlite-rembed: A SQLite extension for generating text embeddings from remote APIs

2024-07-25 by [Alex Garcia](https://alexgarcia.xyz/)

> _tl;dr — [`sqlite-rembed`](https://github.com/asg017/sqlite-rembed) is a new SQLite extension for generating text embeddings from remote APIs — like OpenAI, Nomic, Cohere, llamafile, Ollama, and more! It bundles its own HTTP client, so it can be used in small environments like the official SQLite CLI. It doesn't support batch embeddings yet, but can still be useful in many cases.

---

`sqlite-rembed` is a new SQLite extension I've been experimenting with, as a sister project to [`sqlite-vec`](https://github.com/asg017/sqlite-vec). It connects to various 3rd party APIs to generate text embeddings.

For example, to use [OpenAI's embedding service](https://platform.openai.com/docs/guides/embeddings), this is all you need:

```sql
INSERT INTO temp.rembed_clients(name, options)
  VALUES ('text-embedding-3-small', 'openai');

select rembed(
  'text-embedding-3-small',
  'The United States Postal Service is an independent agency...'
); -- X'A452...01FC', Blob<6144 bytes>
```

Here we register a new rembed "client" named `text-embedding-3-small`, using the special `openai` option. By default, The `openai` option will source your API key from the `OPENAI_API_KEY` environment variable, and use the client name (`text-embedding-3-small`) as the model name.

Now, we can use the `rembed()` SQL function to generate embeddings from OpenAI! It returns the embeddings in a compact BLOB format, the same format that `sqlite-vec` uses. In this case, `text-embedding-3-small` returns 1536 dimensions, so a `1536 * 4 = 6144` length BLOB is returned.

And `sqlite-rembed` has support for other providers! Here's an example that uses [Nomic's embedding API](https://docs.nomic.ai/reference/endpoints/nomic-embed-text):

```sql
INSERT INTO temp.rembed_clients(name, options)
  VALUES ('nomic-embed-text-v1.5', 'nomic');

select rembed(
  'nomic-embed-text-v1.5',
  'The United States Postal Service is an independent agency...'
);
```

And with [Cohere's embedding API](https://docs.cohere.com/reference/embed):

```sql
INSERT INTO temp.rembed_clients(name, options)
  VALUES ('embed-english-v3.0', 'cohere');

select rembed(
  'embed-english-v3.0',
  'The United States Postal Service is an independent agency...'
);
```

Notice how you can have multiple clients, all with different names and using different API providers. Secrets are sourced from places you expect: `NOMIC_API_KEY`, `CO_API_KEY`, and so on.

If you want to manually configure which API keys to use, or change the "base URL" of a provider, you can do so with `rembed_client_options()`:

```sql
INSERT INTO temp.rembed_clients(name, options) VALUES
  (
    'text-embedding-3-small',
    rembed_client_options(
      'format', 'openai',
      'key', :OPENAI_API_KEY -- SQL parameter to bind an API key
    )
  );
```

In total, `sqlite-rembed` currently has support for the following embedding providers:

- OpenAI
- Nomic
- Cohere
- Jina
- MixedBread
- Llamafile
- Ollama

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-rembed-init/index.html#remote-embeddings-can-still-be-local) "Remote" embeddings can still be local!

`sqlite-rembed` stands for "**SQLite** **r**emote **embed**dings," in contrast to its sister project [`sqlite-lembed`](https://github.com/asg017/sqlite-lembed) that stands for "**SQLite** **l**ocal **embed**dings." For `sqlite-lembed`, "local" means inside the same process, no external process or server needed. "Remote" in `sqlite-rembed` just means "outside the current process", which isn't always an outside `https://...` server.

You can totally run a embeddings model locally with llamafile, Ollama, or some other "OpenAI compatible" service, and point `sqlite-rembed` to a `http://localhost:...` endpoint.

Let's take llamafile as an example: follow the ["Getting Started with LLaMAfiler"](https://github.com/Mozilla-Ocho/llamafile/blob/main/llamafile/server/doc/getting_started.md) guide. Once up, you'll have a local embeddings server available to you at `http://127.0.0.1:8080/`. To use it from `sqlite-rembed`, register with the `llamafile` option:

```sql
INSERT INTO temp.rembed_clients(name, options)
 VALUES ('llamafile', 'llamafile');

.mode quote

select rembed('llamafile', 'Tennis star Coco Gauff will carry the U.S. flag...');
```

And that's it! Not a single byte of your data will leave your computer.

Another option is [Ollama's embeddings support](https://ollama.com/blog/embedding-models). Once installed, Ollama will have a constantly running server at `http://localhost:11434`. To use from `sqlite-rembed`, register a `ollama` client like so:

```sql
INSERT INTO temp.rembed_clients(name, options)
  VALUES ('snowflake-arctic-embed:s', 'ollama');

select rembed('ollama', 'LeVar Burton talks about his changing...');
```

Where the [`snowflake-arctic-embed:s`](https://ollama.com/library/snowflake-arctic-embed:s) model I downloaded with `ollama pull snowflake-arctic-embed:s`. This approach is nice because the Ollama service will be constantly running in the background, and will "wake up" embedding models into memory on first request (and will unload after 5 minutes of inactivity). Again, not a single byte of your data leaves your computer.

---

So try out `sqlite-rembed` today! There are pre-compiled binaries on Github releases, or you can `pip install sqlite-rembed` or `npm install sqlite-remebed`.

# Introducing sqlite-lembed: A SQLite extension for generating text embeddings locally

2024-07-24 by [Alex Garcia](https://alexgarcia.xyz/)

> *tl;dr — [`sqlite-lembed`](https://github.com/asg017/sqlite-lembed) is a SQLite extension for generating text embeddings, meant to work alongside [`sqlite-vec`](https://github.com/asg017/sqlite-vec). With a single embeddings model file provided in the `.gguf` format, you can generate embeddings using regular SQL functions, and store them directly inside your SQLite database. No extra server, process, or configuration needed!*

---

I've been working on [`sqlite-vec`](https://github.com/asg017/sqlite-vec) for quite some time now - 3 months [since I first announced it](https://alexgarcia.xyz/blog/2024/building-new-vector-search-sqlite/index.html), More than 7 months since my first prototype, and more than 2 years since [my first SQLite vector search attempt](https://github.com/asg017/sqlite-vss). And the initial stable version coming soon, I promise! `v0.1.0` is scheduled for next week.

But one weakness of `sqlite-vec` compared to other vector storage tools is that **you must generate embeddings yourself**. Some vector databases have helper functions and wrappers that automatically generate embeddings for you when inserting text.

But this feature never made sense for `sqlite-vec`. It's a [single C file](https://github.com/asg017/sqlite-vec/blob/main/sqlite-vec.c) with no external dependencies. Adding embedding model inference would drastically add scope and make things too complicated.

At the same time, I don't want to `pip install openai` or `pip install sentence-transformers` every time I want to generate embeddings on some text. I want something that is lightweight, a single binary, and works with SQLite.

So, with the help of [`llama.cpp`'s embeddings support](https://github.com/ggerganov/llama.cpp/pull/5796), `sqlite-lembed` is born!

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-lembed-init/index.html#usage) Usage

There are a few ways to install `sqlite-lembed` - `npm install sqlite-lembed`, `pip install sqlite-lembed`, `gem install sqlite-lembed`, or grabbing pre-compiled extension from [the Releases page](https://github.com/asg017/sqlite-lembed/releases). Or if you want to directly install and give your IT admins a scare, install with:

```bash
curl -L https://github.com/asg017/sqlite-lembed/releases/download/v0.0.1-alpha.4/install.sh | sh
```

You now have a `lembed0.dylib` (MacOS) or `lembed0.so` (Linux) file in your current directory!

Now you'll need an embeddings models in [`.gguf` format](https://huggingface.co/docs/hub/en/gguf). A few open source options include [`nomic-embed-text-v1.5`](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF) and [`mxbai-embed-large-v1`](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1), but here we will download the smaller and older [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model like so:

```bash
curl -L -o all-MiniLM-L6-v2.e4ce9877.q8_0.gguf https://huggingface.co/asg017/sqlite-lembed-model-examples/resolve/main/all-MiniLM-L6-v2/all-MiniLM-L6-v2.e4ce9877.q8_0.gguf
```

Now we can generate some embeddings! Fire up the `sqlite3` CLI and run these setup commands.

```sql
.load ./lembed0

INSERT INTO temp.lembed_models(name, model)
  select 'all-MiniLM-L6-v2', lembed_model_from_file('all-MiniLM-L6-v2.e4ce9877.q8_0.gguf');
```

The `temp.lembed_model` virtual table lets you "register" models with pure `INSERT INTO` statements. The `name` field is a unique identifier for a given model, and `model` is provided as a path to the `.gguf` model, on disk, with the `lembed_model_from_file()` function.

Let's try out this new `'all-MiniLM-L6-v2'` model with the `lembed()` function.

```sql
select lembed(
  'all-MiniLM-L6-v2',
  'The United States Postal Service is an independent agency...'
); -- X'A402...09C3' (1536 bytes)
```

That's out first embedding! A 384 dimensional floating point vector (defined as part of the `all-MiniLM-L6-v2` model), taking up 1,536 bytes of space with 4 bytes per element.

Now a single embedding of a single sentence isn't that exciting — let's try a larger sample. Since we will be comparing multiple vectors together, let's bring in `sqlite-vec` into our project. Again you can `npm install` or `gem install` or `pip install` `sqlite-vec`, but if you live dangerously you can install with:

```bash
curl -L https://github.com/asg017/sqlite-vec/releases/download/0.0.1-alpha.37/install.sh | sh
```

Let's create a corpus of some random news headlines and store that in a "regular" SQLite table.

```sql
create table articles(
  headline text
);

-- Random NPR headlines from 2024-06-04
insert into articles VALUES
  ('Shohei Ohtani''s ex-interpreter pleads guilty to charges related to gambling and theft'),
  ('The jury has been selected in Hunter Biden''s gun trial'),
  ('Larry Allen, a Super Bowl champion and famed Dallas Cowboy, has died at age 52'),
  ('After saying Charlotte, a lone stingray, was pregnant, aquarium now says she''s sick'),
  ('An Epoch Times executive is facing money laundering charge');
```

Ok now let's generate some embeddings! We will store the embedding directly into a new `vec0` virtual table. We can always join this new table back with the `articles` table for metadata.

```sql
.load ./vec0

-- Build a vector table with embeddings of article headlines
create virtual table vec_articles using vec0(
  headline_embeddings float[384]
);

insert into vec_articles(rowid, headline_embeddings)
  select rowid, lembed('all-MiniLM-L6-v2', headline)
  from articles;
```

Now every `headline` in `articles` has been embed and stored in `vec_articles`. To perform a KNN-style search, we can do:

```sql
param set :query 'firearm courtroom'

with matches as (
  select
    rowid,
    distance
  from vec_articles
  where headline_embeddings match lembed('all-MiniLM-L6-v2', :query)
  order by distance
  limit 3
)
select
  headline,
  distance
from matches
left join articles on articles.rowid = matches.rowid;

/*
+--------------------------------------------------------------+------------------+
|                           headline                           |     distance     |
+--------------------------------------------------------------+------------------+
| Shohei Ohtani's ex-interpreter pleads guilty to charges rela | 1.14812409877777 |
| ted to gambling and theft                                    |                  |
+--------------------------------------------------------------+------------------+
| The jury has been selected in Hunter Biden's gun trial       | 1.18380105495453 |
+--------------------------------------------------------------+------------------+
| An Epoch Times executive is facing money laundering charge   | 1.27715671062469 |
+--------------------------------------------------------------+------------------+
*/
```

And there we go! Notice how "firearm courtroom" doesn't appear in any of these headlines, but it can still figure out that "Hunter Biden's gun trial" is related, and the other two justice-related articles appear on top.

So there you have it - text embeddings and vector search, all with the `sqlite3` CLI, two extensions, and a single `.gguf` file.

## [¶](https://alexgarcia.xyz/blog/2024/sqlite-lembed-init/index.html#last-notes) Last notes

**It is not required to use `sqlite-lembed` with `sqlite-vec`**, or vice-versa. You can use any embeddings provider with `sqlite-vec` — the OpenAI API, other JSON endpoints, PyTorch models, etc. As long as your embeddings can be provided as JSON or a compact BLOG format, you're good to go.

Similarly, **it is not required to use `sqlite-vec` with `sqlite-lembed`**. You can dump embeddings generated by `sqlite-lembed` into any other vector store you like, or in regular SQLite tables with `sqlite-vec`.

Also, Windows isn't supported yet. Sorry! Hopefully soon, `llama.cpp` does support Windows, but Github Actions can be quite a nightmare. WASM is also not supported yet, but hoping to figure that out in the near future.

And lastly — **`sqlite-lembed` is still in beta**! While `sqlite-vec` stabilized on v0.1.0 next week, `sqlite-lembed` will be actively developed for the near future. Mostly because the `llama.cpp` dependency is also under active deveopment, but I hope that the main SQL API won't change much.


# API Reference

A complete reference to all the SQL scalar functions, table functions, and virtual tables inside `sqlite-vec`.

WARNING

sqlite-vec is pre-v1, so expect breaking changes.

- [Constructors](https://alexgarcia.xyz/sqlite-vec/api-reference.html#constructors)
  - [vec_f32(vector)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_f32)
  - [vec_int8(vector)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_int8)
  - [vec_bit(vector)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_bit)
- [Operations](https://alexgarcia.xyz/sqlite-vec/api-reference.html#op)
  - [vec_length(vector)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_length)
  - [vec_type(vector)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_type)
  - [vec_add(a, b)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_add)
  - [vec_sub(a, b)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_sub)
  - [vec_normalize(vector)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_normalize)
  - [vec_slice(vector, start, end)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_slice)
  - [vec_to_json(vector)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_to_json)
  - [vec_each(vector)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_each)
- [Distance functions](https://alexgarcia.xyz/sqlite-vec/api-reference.html#distance)
  - [vec_distance_L2(a, b)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_distance_L2)
  - [vec_distance_cosine(a, b)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_distance_cosine)
  - [vec_distance_hamming(a, b)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_distance_hamming)
- [Quantization](https://alexgarcia.xyz/sqlite-vec/api-reference.html#quantization)
  - [vec_quantize_binary(vector)](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_quantize_binary)
  - [vec_quantize_i8(vector, [start], [end])](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_quantize_i8)
- [Meta](https://alexgarcia.xyz/sqlite-vec/api-reference.html#meta)
  - [vec_version()](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_version)
  - [vec_debug()](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_debug)
- [Entrypoints](https://alexgarcia.xyz/sqlite-vec/api-reference.html#entrypoints)

## Constructors

SQL functions that "construct" vectors with different element types.

Currently, only `float32`, `int8`, and `bit` vectors are supported.

### `vec_f32(vector)`

Creates a float vector from a BLOB or JSON text. If a BLOB is provided, the length must be divisible by 4, as a float takes up 4 bytes of space each.

The returned value is a BLOB with 4 bytes per element, with a special [subtype](https://www.sqlite.org/c3ref/result_subtype.html) of `223`.

sql

```
select vec_f32('[.1, .2, .3, 4]');
-- X'CDCCCC3DCDCC4C3E9A99993E00008040'

select subtype(vec_f32('[.1, .2, .3, 4]'));
-- 223

select vec_f32(X'AABBCCDD');
-- X'AABBCCDD'

select vec_to_json(vec_f32(X'AABBCCDD'));
-- '[-1844071490169864000.000000]'

select vec_f32(X'AA');
-- ❌ invalid float32 vector BLOB length. Must be divisible by 4, found 1
```

### `vec_int8(vector)`

Creates a 8-bit integer vector from a BLOB or JSON text. If a BLOB is provided, the length must be divisible by 4, as a float takes up 4 bytes of space each. If JSON text is provided, each element must be an integer between -128 and 127 inclusive.

The returned value is a BLOB with 1 byte per element, with a special [subtype](https://www.sqlite.org/c3ref/result_subtype.html) of `225`.

sql

```
select vec_int8('[1, 2, 3, 4]');
-- X'01020304'

select subtype(vec_int8('[1, 2, 3, 4]'));
-- 225

select vec_int8(X'AABBCCDD');
-- X'AABBCCDD'

select vec_to_json(vec_int8(X'AABBCCDD'));
-- '[-86,-69,-52,-35]'

select vec_int8('[999]');
-- ❌ JSON parsing error: value out of range for int8
```

### `vec_bit(vector)`

Creates a binary vector from a BLOB.

The returned value is a BLOB with 1 byte per 8 elements, with a special [subtype](https://www.sqlite.org/c3ref/result_subtype.html) of `224`.

sql

```
select vec_bit(X'F0');
-- X'F0'

select subtype(vec_bit(X'F0'));
-- 224

select vec_to_json(vec_bit(X'F0'));
-- '[0,0,0,0,1,1,1,1]'
```

## Operations

Different operations and utilities for working with vectors.

### `vec_length(vector)`

Returns the number of elements in the given vector. The vector can be `JSON`, `BLOB`, or the result of a [constructor function](https://alexgarcia.xyz/sqlite-vec/api-reference.html#constructors).

This function will return an error if `vector` is invalid.

sql

```
select vec_length('[.1, .2]');
-- 2

select vec_length(X'AABBCCDD');
-- 1

select vec_length(vec_int8(X'AABBCCDD'));
-- 4

select vec_length(vec_bit(X'AABBCCDD'));
-- 32

select vec_length(X'CCDD');
-- ❌ invalid float32 vector BLOB length. Must be divisible by 4, found 2
```

### `vec_type(vector)`

Returns the name of the type of `vector` as text. One of `'float32'`, `'int8'`, or `'bit'`.

This function will return an error if `vector` is invalid.

sql

```
select vec_type('[.1, .2]');
-- 'float32'

select vec_type(X'AABBCCDD');
-- 'float32'

select vec_type(vec_int8(X'AABBCCDD'));
-- 'int8'

select vec_type(vec_bit(X'AABBCCDD'));
-- 'bit'

select vec_type(X'CCDD');
-- ❌ invalid float32 vector BLOB length. Must be divisible by 4, found 2
```

### `vec_add(a, b)`

Adds every element in vector `a` with vector `b`, returning a new vector `c`. Both vectors must be of the same type and same length. Only `float32` and `int8` vectors are supported.

An error is raised if either `a` or `b` are invalid, or if they are not the same type or same length.

See also [`vec_sub()`](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_sub).

sql

```
select vec_add(
  '[.1, .2, .3]',
  '[.4, .5, .6]'
);
-- X'0000003F3333333F6766663F'

select vec_to_json(
  vec_add(
    '[.1, .2, .3]',
    '[.4, .5, .6]'
  )
);
-- '[0.500000,0.700000,0.900000]'

select vec_to_json(
  vec_add(
    vec_int8('[1, 2, 3]'),
    vec_int8('[4, 5, 6]')
  )
);
-- '[5,7,9]'

select vec_add('[.1]', vec_int8('[1]'));
-- ❌ Vector type mistmatch. First vector has type float32, while the second has type int8.

select vec_add(vec_bit(X'AA'), vec_bit(X'BB'));
-- ❌ Cannot add two bitvectors together.
```

### `vec_sub(a, b)`

Subtracts every element in vector `a` with vector `b`, returning a new vector `c`. Both vectors must be of the same type and same length. Only `float32` and `int8` vectors are supported.

An error is raised if either `a` or `b` are invalid, or if they are not the same type or same length.

See also [`vec_add()`](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_add).

sql

```
select vec_sub(
  '[.1, .2, .3]',
  '[.4, .5, .6]'
);
-- X'9A9999BE9A9999BE9A9999BE'

select vec_to_json(
  vec_sub(
    '[.1, .2, .3]',
    '[.4, .5, .6]'
  )
);
-- '[-0.300000,-0.300000,-0.300000]'

select vec_to_json(
  vec_sub(
    vec_int8('[1, 2, 3]'),
    vec_int8('[4, 5, 6]')
  )
);
-- '[-3,-3,-3]'

select vec_sub('[.1]', vec_int8('[1]'));
-- ❌ Vector type mistmatch. First vector has type float32, while the second has type int8.

select vec_sub(vec_bit(X'AA'), vec_bit(X'BB'));
-- ❌ Cannot subtract two bitvectors together.
```

### `vec_normalize(vector)`

Performs L2 normalization on the given vector. Only float32 vectors are currently supported.

Returns an error if the input is an invalid vector or not a float32 vector.

sql

```
select vec_normalize('[2, 3, 1, -4]');
-- X'BAF4BA3E8B370C3FBAF43A3EBAF43ABF'

select vec_to_json(
  vec_normalize('[2, 3, 1, -4]')
);
-- '[0.365148,0.547723,0.182574,-0.730297]'

-- for matryoshka embeddings - slice then normalize
select vec_to_json(
  vec_normalize(
    vec_slice('[2, 3, 1, -4]', 0, 2)
  )
);
-- '[0.554700,0.832050]'
```

### `vec_slice(vector, start, end)`

Extract a subset of `vector` from the `start` element (inclusive) to the `end` element (exclusive). TODO check

This is especially useful for [Matryoshka embeddings](https://alexgarcia.xyz/sqlite-vec/api-reference.html#TODO), also known as "adaptive length" embeddings. Use with [`vec_normalize()`](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_normalize) to get proper results.

Returns an error in the following conditions:

- If `vector` is not a valid vector
- If `start` is less than zero or greater than or equal to `end`
- If `end` is greater than the length of `vector`, or less than or equal to `start`.
- If `vector` is a bitvector, `start` and `end` must be divisible by 8.

sql

```
select vec_slice('[1, 2,3, 4]', 0, 2);
-- X'0000803F00000040'

select vec_to_json(
  vec_slice('[1, 2,3, 4]', 0, 2)
);
-- '[1.000000,2.000000]'

select vec_to_json(
  vec_slice('[1, 2,3, 4]', 2, 4)
);
-- '[3.000000,4.000000]'

select vec_to_json(
  vec_slice('[1, 2,3, 4]', -1, 4)
);
-- ❌ slice 'start' index must be a postive number.

select vec_to_json(
  vec_slice('[1, 2,3, 4]', 0, 5)
);
-- ❌ slice 'end' index is greater than the number of dimensions

select vec_to_json(
  vec_slice('[1, 2,3, 4]', 0, 0)
);
-- ❌ slice 'start' index is equal to the 'end' index, vectors must have non-zero length
```

### `vec_to_json(vector)`

Represents a vector as JSON text. The input vector can be a vector BLOB or JSON text.

Returns an error if `vector` is an invalid vector, or when memory cannot be allocated.

sql

```
select vec_to_json(X'AABBCCDD');
-- '[-1844071490169864000.000000]'

select vec_to_json(vec_int8(X'AABBCCDD'));
-- '[-86,-69,-52,-35]'

select vec_to_json(vec_bit(X'AABBCCDD'));
-- '[0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0,0,1,1,0,0,1,1,1,0,1,1,1,0,1,1]'

select vec_to_json('[1,2,3,4]');
-- '[1.000000,2.000000,3.000000,4.000000]'

select vec_to_json('invalid');
-- ❌ JSON array parsing error: Input does not start with '['
```

### `vec_each(vector)`

A table function to iterate through every element in a vector. One row id returned per element in a vector.

sql

```
CREATE TABLE vec_each(
  rowid int,    -- The
  vector HIDDEN -- input parameter: A well-formed vector value
)
```

Returns an error if `vector` is not a valid vector.

sql

```
select rowid, value from vec_each('[1,2,3,4]');
/*
┌───────┬───────┐
│ rowid │ value │
├───────┼───────┤
│ 0     │ 1     │
├───────┼───────┤
│ 1     │ 2     │
├───────┼───────┤
│ 2     │ 3     │
├───────┼───────┤
│ 3     │ 4     │
└───────┴───────┘

*/


select rowid, value from vec_each(X'AABBCCDD00112233');
/*
┌───────┬──────────────────────┐
│ rowid │ value                │
├───────┼──────────────────────┤
│ 0     │ -1844071490169864200 │
├───────┼──────────────────────┤
│ 1     │ 3.773402568185702e-8 │
└───────┴──────────────────────┘

*/


select rowid, value from vec_each(vec_int8(X'AABBCCDD'));
/*
┌───────┬───────┐
│ rowid │ value │
├───────┼───────┤
│ 0     │ -86   │
├───────┼───────┤
│ 1     │ -69   │
├───────┼───────┤
│ 2     │ -52   │
├───────┼───────┤
│ 3     │ -35   │
└───────┴───────┘

*/


select rowid, value from vec_each(vec_bit(X'F0'));
/*
┌───────┬───────┐
│ rowid │ value │
├───────┼───────┤
│ 0     │ 1     │
├───────┼───────┤
│ 1     │ 1     │
├───────┼───────┤
│ 2     │ 1     │
├───────┼───────┤
│ 3     │ 1     │
├───────┼───────┤
│ 4     │ 0     │
├───────┼───────┤
│ 5     │ 0     │
├───────┼───────┤
│ 6     │ 0     │
├───────┼───────┤
│ 7     │ 0     │
└───────┴───────┘

*/
```

## Distance functions

Various algorithms to calculate distance between two vectors.

### `vec_distance_L2(a, b)`

Calculates the L2 euclidian distance between vectors `a` and `b`. Only valid for float32 or int8 vectors.

Returns an error under the following conditions:

- `a` or `b` are invalid vectors
- `a` or `b` do not share the same vector element types (ex float32 or int8)
- `a` or `b` are bit vectors. Use [`vec_distance_hamming()`](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_distance_hamming) for distance calculations between two bitvectors.
- `a` or `b` do not have the same length.

sql

```
select vec_distance_L2('[1, 1]', '[2, 2]');
-- 1.4142135381698608

select vec_distance_L2('[1, 1]', '[-2, -2]');
-- 4.242640495300293

select vec_distance_L2('[1.1, 2.2, 3.3]', '[4.4, 5.5, 6.6]');
-- 5.7157673835754395

select vec_distance_L2(X'AABBCCDD', X'00112233');
-- 1844071490169864200

select vec_distance_L2('[1, 1]', vec_int8('[2, 2]'));
-- ❌ Vector type mistmatch. First vector has type float32, while the second has type int8.

select vec_distance_L2(vec_bit(X'AA'), vec_bit(X'BB'));
-- ❌ Cannot calculate L2 distance between two bitvectors.
```

### `vec_distance_cosine(a, b)`

Calculates the cosine distance between vectors `a` and `b`. Only valid for float32 or int8 vectors.

Returns an error under the following conditions:

- `a` or `b` are invalid vectors
- `a` or `b` do not share the same vector element types (ex float32 or int8)
- `a` or `b` are bit vectors. Use [`vec_distance_hamming()`](https://alexgarcia.xyz/sqlite-vec/api-reference.html#vec_distance_hamming) for distance calculations between two bitvectors.
- `a` or `b` do not have the same length.

sql

```
select vec_distance_cosine('[1, 1]', '[2, 2]');
-- 2.220446049250313e-16

select vec_distance_cosine('[1, 1]', '[-2, -2]');
-- 2

select vec_distance_cosine('[1.1, 2.2, 3.3]', '[4.4, 5.5, 6.6]');
-- 0.02536807395517826

select vec_distance_cosine(X'AABBCCDD', X'00112233');
-- 2

select vec_distance_cosine('[1, 1]', vec_int8('[2, 2]'));
-- ❌ Vector type mistmatch. First vector has type float32, while the second has type int8.

select vec_distance_cosine(vec_bit(X'AA'), vec_bit(X'BB'));
-- ❌ Cannot calculate cosine distance between two bitvectors.
```

### `vec_distance_hamming(a, b)`

Calculates the hamming distance between two bitvectors `a` and `b`. Only valid for bitvectors.

Returns an error under the following conditions:

- `a` or `b` are not bitvectors
- `a` and `b` do not share the same length
- Memory cannot be allocated

sql

```
select vec_distance_hamming(vec_bit(X'00'), vec_bit(X'FF'));
-- 8

select vec_distance_hamming(vec_bit(X'FF'), vec_bit(X'FF'));
-- 0

select vec_distance_hamming(vec_bit(X'F0'), vec_bit(X'44'));
-- 4

select vec_distance_hamming('[1, 1]', '[0, 0]');
-- ❌ Cannot calculate hamming distance between two float32 vectors.
```

## Quantization

Various techniques to "compress" a vector by reducing precision and accuracy.

### `vec_quantize_binary(vector)`

Quantize a float32 or int8 vector into a bitvector. For every element in the vector, a `1` is assigned to positive numbers and a `0` is assigned to negative numbers. These values are then packed into a bit vector.

Returns an error if `vector` is invalid, or if `vector` is not a float32 or int8 vector.

sql

```
select vec_quantize_binary('[1, 2, 3, 4, 5, 6, 7, 8]');
-- X'FF'

select vec_quantize_binary('[1, 2, 3, 4, -5, -6, -7, -8]');
-- X'0F'

select vec_quantize_binary('[-1, -2, -3, -4, -5, -6, -7, -8]');
-- X'00'

select vec_quantize_binary('[-1, -2, -3, -4, -5, -6, -7, -8]');
-- X'00'

select vec_quantize_binary(vec_int8(X'11223344'));
-- ❌ Binary quantization requires vectors with a length divisible by 8

select vec_quantize_binary(vec_bit(X'FF'));
-- ❌ Can only binary quantize float or int8 vectors
```

### `vec_quantize_i8(vector, [start], [end])`

x

sql

```
select 'todo';
-- 'todo'
```

## Meta

Helper functions to debug `sqlite-vec` installations.

### `vec_version()`

Returns a version string of the current `sqlite-vec` installation.

sql

```
select vec_version();
-- 'v0.0.1-alpha.37'
```

### `vec_debug()`

Returns debugging information of the current `sqlite-vec` installation.

sql

```
select vec_debug();
/*
'Version: v0.0.1-alpha.37
Date: 2024-07-23T14:09:43Z-0700
Commit: 77f9b0374c8129056b344854de2dff6b103e5729
Build flags: avx '
*/
```

## Entrypoints

All the named entrypoints that load in different `sqlite-vec` functions and options.
