import nltk
from nltk.corpus import stopwords
import IOUtil
import gensim
from gensim.models import Word2Vec
import string
import numpy as np
import sklearn.feature_extraction.text
import scipy
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt



punct_collection = string.punctuation.decode('utf8')

def tokenize(tweets_list):
    tokenized_list = [nltk.word_tokenize(tweet) for tweet in tweets_list]
    return [filter_stop_words(sentence) for sentence in tokenized_list]


def filter_stop_words(sentence):
    return [word.lower() for word in sentence if word not in stopwords.words('english')]


def train_word2vec_model(content_list):
    new_content_list = tokenize(content_list)
    model = Word2Vec(new_content_list, min_count=3, workers=4)
    return model


def save_word2vec_model(model, output_path):
    model.wv.save_word2vec_format(fname=output_path, binary=False)


def read_model(model_path):
    models = IOUtil.read_file(model_path, lambda x: x.split())
    models = models[1:]
    dictionary = [ele[0] for ele in models]
    embedding_vectors = [ele[1:] for ele in models]
    embedding_vectors = [[float(ele) for ele in vector] for vector in embedding_vectors]
    embedding_matrix = np.matrix(embedding_vectors)
    return dictionary, embedding_matrix


def generate_weighting_vectors(content_list, vocabulary):
    tf_idf_vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(
        stop_words='english',
        min_df=1,
    vocabulary=vocabulary)
    features = tf_idf_vectorizer.fit_transform(content_list)
    return features


def test(model_path):
    dictionary, embeddings = read_model(model_path)

    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(embeddings[:150, :])

    plt.scatter(Y[:, 0], Y[:, 1])
    for label, x, y in zip(dictionary, Y[:, 0], Y[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0.01, 0.01), textcoords='offset points')
    plt.show()


def generate_paragraph_vectors():
    input_path = '/Users/zxj/Downloads/algorithm_project/data_7_gen_2_plain.txt'
    model_path = 'genism_word2vec.txt'
    content_list = IOUtil.read_file(input_path, IOUtil.fold_left(IOUtil.regex_list))
    content_list = [tweet.strip(punct_collection) for tweet in content_list]
    #model = train_word2vec_model(content_list)
    #save_word2vec_model(model, model_path)
    dictionary, embeddings = read_model(model_path)
    weight_vectors = generate_weighting_vectors(content_list, dictionary)
    paragraph_vectors = weight_vectors.dot(embeddings)
    dist_vector = scipy.spatial.distance.pdist(paragraph_vectors, metric='euclidean')

if __name__ == '__main__':
    model_path = 'genism_word2vec.txt'
    test(model_path)